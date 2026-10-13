#!/usr/bin/env python3
"""Seleção e confirmação das seções com rotação da newsletter.

Uso:
  python rotation.py select [--date AAAA-MM-DD] [--secao ID]
  python rotation.py mark-used --secao ID --item ITEM --confirmacao REF [--date AAAA-MM-DD]
  python rotation.py status

`select` nunca grava. O estado só avança com `mark-used`, que deve ser chamado
somente depois que create_draft.py devolver o campaign_id do rascunho
(`--confirmacao <campaign_id>`).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from typing import Any

from _newsletter_common import (
    NewsletterError,
    load_config,
    parse_date,
    project_root,
    read_json,
    section_by_id,
    skill_path,
    write_json,
)

STATEFUL = {"rotacao-catalogo", "pool-sem-repeticao", "alternancia", "fixado", "kit-catalogo"}
SELECTABLE = STATEFUL | {"calendario"}
WEEKDAYS = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]


def load_catalog(spec: dict[str, Any]) -> list[dict[str, Any]]:
    path = spec.get("catalogo")
    if not path:
        raise NewsletterError("Seção sem 'catalogo'.")
    items = read_json(skill_path(path), default=[])
    if isinstance(items, dict):
        items = items.get("itens", [])
    if not items:
        raise NewsletterError(f"Catálogo vazio: {path}")
    return items


def is_active(item: dict[str, Any]) -> bool:
    return item.get("ativo", True) is not False


def next_circular(items: list[dict[str, Any]], last_id: str | None) -> dict[str, Any] | None:
    ids = [item["id"] for item in items]
    start = ids.index(last_id) + 1 if last_id in ids else 0
    for offset in range(len(items)):
        candidate = items[(start + offset) % len(items)]
        if is_active(candidate):
            return candidate
    return None


def choose_kit(spec: dict[str, Any], history: list[dict[str, Any]]) -> dict[str, Any]:
    """Kit = 1 item principal (circular) + 1 item de cada componente compatível com ele.

    Em cada componente, escolhe entre os itens compatíveis (lista `campo_compat` do item principal)
    o usado há mais tempo no histórico; empate → ordem do catálogo do componente. Componente
    `opcional` sem item compatível fica de fora do kit (kit menor), em vez de travar a edição.
    """
    products = load_catalog(spec)
    last = history[-1]["item"] if history else None
    product = next_circular(products, last)
    if not product:
        return {"item": None, "motivo": "nenhum item principal ativo"}
    chosen: dict[str, Any] = {}
    notes: list[str] = []
    for comp in spec.get("componentes", []):
        cid = comp["id"]
        items = [i for i in load_catalog(comp) if is_active(i)]
        compat = set(product.get(comp.get("campo_compat", cid), []) or [])
        candidates = [i for i in items if i["id"] in compat]
        if not candidates:
            if comp.get("opcional"):
                notes.append(f"{cid}: nenhum compatível com {product['id']} (omitido)")
                chosen[cid] = None
                continue
            return {"item": None, "motivo": f"{cid}: nenhum item compatível com {product['id']}"}
        last_use: dict[str, int] = {}
        for idx, entry in enumerate(history):
            used = (entry.get("componentes") or {}).get(cid)
            if used:
                last_use[used] = idx
        order = {i["id"]: n for n, i in enumerate(items)}
        pick = min(candidates, key=lambda i: (last_use.get(i["id"], -1), order[i["id"]]))
        chosen[cid] = pick
        notes.append(f"{cid}: {pick['id']} (compatível usado há mais tempo)")
    item = dict(product)
    item["componentes"] = chosen
    motivo = (f"principal: próximo após {last!r}" if last else "principal: primeiro ativo") + "; " + "; ".join(notes)
    return {"item": item, "motivo": motivo}


def choose(spec: dict[str, Any], history: list[dict[str, Any]], day: date) -> dict[str, Any]:
    tipo = spec.get("tipo")

    if tipo == "rotacao-catalogo":
        items = load_catalog(spec)
        last = history[-1]["item"] if history else None
        item = next_circular(items, last)
        return {"item": item, "motivo": f"próximo após {last!r} em ordem circular" if last else "primeiro ativo (sem histórico)"}

    if tipo == "kit-catalogo":
        return choose_kit(spec, history)

    if tipo == "pool-sem-repeticao":
        items = load_catalog(spec)
        window = int(spec.get("janela_itens", 10))
        recent: list[str] = []
        for entry in reversed(history):
            if entry["item"] not in recent:
                recent.append(entry["item"])
            if len(recent) >= window:
                break
        for item in items:
            if is_active(item) and item["id"] not in recent:
                return {"item": item, "motivo": f"primeiro ativo fora dos últimos {window} usados"}
        last_use = {entry["item"]: idx for idx, entry in enumerate(history)}
        active = [item for item in items if is_active(item)]
        if not active:
            return {"item": None, "motivo": "nenhum item ativo"}
        oldest = min(active, key=lambda item: last_use.get(item["id"], -1))
        return {"item": oldest, "motivo": "todos usados recentemente; escolhido o usado há mais tempo"}

    if tipo == "alternancia":
        items = load_catalog(spec)
        groups = spec.get("grupos") or []
        if not groups:
            raise NewsletterError("Seção 'alternancia' sem 'grupos'.")
        last_group = history[-1].get("grupo") if history else None
        start = groups.index(last_group) + 1 if last_group in groups else 0
        for offset in range(len(groups)):
            group = groups[(start + offset) % len(groups)]
            group_items = [item for item in items if item.get("grupo") == group]
            group_history = [entry for entry in history if entry.get("grupo") == group]
            last = group_history[-1]["item"] if group_history else None
            item = next_circular(group_items, last) if group_items else None
            if item:
                return {"item": item, "grupo": group, "motivo": f"grupo '{group}' (último grupo: {last_group!r})"}
        return {"item": None, "motivo": "nenhum item ativo em nenhum grupo"}

    if tipo == "calendario":
        regra = spec.get("regra")
        opcoes = spec.get("opcoes", {})
        if regra == "semana-iso-paridade":
            week = day.isocalendar()[1]
            key = "impar" if week % 2 else "par"
            motivo = f"semana ISO {week} ({key})"
        elif regra == "dia-da-semana":
            key = WEEKDAYS[day.weekday()]
            motivo = f"dia da semana {key}"
        elif regra == "mes":
            key = f"{day.month:02d}"
            motivo = f"mês {key}"
        else:
            raise NewsletterError(f"Regra de calendário desconhecida: {regra}")
        option = opcoes.get(key) or opcoes.get("padrao")
        if option is None:
            return {"item": None, "motivo": f"{motivo}: sem opção nem 'padrao'"}
        item = dict(option)
        item.setdefault("id", key)
        return {"item": item, "motivo": motivo}

    if tipo == "fixado":
        until = spec.get("ate")
        if until and day > date.fromisoformat(until):
            fallback = spec.get("senao")
            if not fallback:
                return {"item": None, "motivo": f"fixação expirou em {until} e não há 'senao'"}
            result = choose(fallback, history, day)
            result["motivo"] = f"fixação expirou em {until}; aplicada regra 'senao': {result['motivo']}"
            result["via"] = "senao"
            return result
        if spec.get("catalogo"):
            items = load_catalog(spec)
            match = next((item for item in items if item["id"] == spec.get("item")), None)
            if match and is_active(match):
                return {"item": match, "motivo": "item fixado pela campanha ativa"}
            if spec.get("senao"):
                result = choose(spec["senao"], history, day)
                result["motivo"] = f"item fixado inativo/ausente; regra 'senao': {result['motivo']}"
                result["via"] = "senao"
                return result
            return {"item": None, "motivo": "item fixado inativo ou ausente"}
        return {"item": {"id": spec.get("item", "fixo"), "modelo": spec.get("modelo")}, "motivo": "modelo fixado"}

    raise NewsletterError(f"Tipo sem seleção automática: {tipo}")


def enrich(section_id: str, spec: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    item = result.get("item")
    out: dict[str, Any] = {
        "secao": section_id,
        "tipo": spec.get("tipo"),
        "com_estado": spec.get("tipo") in STATEFUL,
        "motivo": result.get("motivo"),
        "grupo": result.get("grupo"),
        "via": result.get("via"),
        "item": item,
    }
    if not item:
        out["erro"] = "nenhum item selecionável"
        return out
    if item.get("modelo"):
        model_path = skill_path(item["modelo"])
        out["modelo_path"] = str(model_path)
        out["modelo_existe"] = model_path.exists()
    if item.get("imagem_local"):
        out["imagem_local_existe"] = (project_root() / item["imagem_local"]).exists()
    if "imagem_publica" in item or "imagem_local" in item:
        out["imagem_src"] = item.get("imagem_publica") or item.get("preview_src") or item.get("imagem_local")
        out["pronto_para_envio"] = bool(item.get("imagem_publica"))
    else:
        out["pronto_para_envio"] = True
    if spec.get("tipo") == "kit-catalogo":
        comps = item.get("componentes") or {}
        out["componentes_ids"] = {k: (v or {}).get("id") for k, v in comps.items()}
        missing = [k for k, v in comps.items() if v and not v.get("imagem_publica")]
        if missing:
            out["pronto_para_envio"] = False
            out["sem_imagem_publica"] = missing
        out["comando_mark_used"] = ("--componentes " + ",".join(f"{k}={v}" for k, v in out["componentes_ids"].items() if v))
    return out


def state_path(config: dict[str, Any]):
    return project_root() / config.get("estado", "newsletter/.rotation-state.json")


def load_state(config: dict[str, Any]) -> dict[str, Any]:
    state = read_json(state_path(config), default={"versao": 1, "secoes": {}})
    state.setdefault("secoes", {})
    return state


def history_for(state: dict[str, Any], section_id: str) -> list[dict[str, Any]]:
    return state["secoes"].get(section_id, {}).get("historico", [])


def cmd_select(config: dict[str, Any], args: argparse.Namespace) -> int:
    day = parse_date(args.date, config)
    state = load_state(config)
    sections = [section_by_id(config, args.secao)] if args.secao else [
        s for s in config.get("secoes", []) if s.get("tipo") in SELECTABLE
    ]
    results = []
    for spec in sections:
        if spec.get("tipo") not in SELECTABLE:
            raise NewsletterError(f"Seção '{spec['id']}' ({spec.get('tipo')}) não tem seleção automática.")
        results.append(enrich(spec["id"], spec, choose(spec, history_for(state, spec["id"]), day)))
    print(json.dumps({"data": day.isoformat(), "estado": str(state_path(config)), "selecoes": results},
                     ensure_ascii=False, indent=2))
    return 1 if any("erro" in r for r in results) else 0


def cmd_mark_used(config: dict[str, Any], args: argparse.Namespace) -> int:
    spec = section_by_id(config, args.secao)
    if spec.get("tipo") not in STATEFUL:
        raise NewsletterError(f"Seção '{args.secao}' ({spec.get('tipo')}) não tem estado para avançar.")

    # A confirmação é o campaign_id devolvido por create_draft.py (numérico nas plataformas suportadas).
    if not re.fullmatch(r"[0-9]+", args.confirmacao or ""):
        raise NewsletterError("Confirmação inválida: informe o campaign_id numérico retornado por create_draft.py. "
                              "Rotação NÃO avançada.")

    day = parse_date(args.date, config)
    state = load_state(config)
    history = history_for(state, args.secao)

    duplicates = [entry for entry in history if entry.get("confirmacao") == args.confirmacao]
    if duplicates:
        if any(entry["item"] != args.item for entry in duplicates):
            raise NewsletterError("Esta confirmação já está associada a outro item nesta seção.")
        print(json.dumps({"atualizado": False, "duplicado": True, "secao": args.secao, "item": args.item}, ensure_ascii=False))
        return 0

    expected = choose(spec, history, day)
    expected_item = (expected.get("item") or {}).get("id")
    group = args.grupo or expected.get("grupo")
    warning = None
    if expected_item and expected_item != args.item:
        warning = f"Item diferente do selecionado hoje ({expected_item}); registrando substituição pontual."

    entry = {"data": day.isoformat(), "item": args.item, "grupo": group, "confirmacao": args.confirmacao}
    if spec.get("tipo") == "kit-catalogo":
        if args.componentes:
            comps = dict(pair.split("=", 1) for pair in args.componentes.split(",") if "=" in pair)
        else:
            comps = {k: (v or {}).get("id") for k, v in ((expected.get("item") or {}).get("componentes") or {}).items()}
        entry["componentes"] = {k: v for k, v in comps.items() if v}
    if warning:
        entry["observacao"] = "substituição pontual"
    state["secoes"].setdefault(args.secao, {}).setdefault("historico", []).append(entry)
    write_json(state_path(config), state)
    print(json.dumps({"atualizado": True, "secao": args.secao, "item": args.item, "grupo": group,
                      "componentes": entry.get("componentes"), "aviso": warning,
                      "estado": str(state_path(config))}, ensure_ascii=False))
    return 0


def cmd_status(config: dict[str, Any], _args: argparse.Namespace) -> int:
    state = load_state(config)
    summary = {}
    for spec in config.get("secoes", []):
        if spec.get("tipo") in STATEFUL:
            history = history_for(state, spec["id"])
            summary[spec["id"]] = {"usos": len(history), "ultimo": history[-1] if history else None}
    print(json.dumps({"estado": str(state_path(config)), "secoes": summary}, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sel = sub.add_parser("select")
    sel.add_argument("--date")
    sel.add_argument("--secao")
    mark = sub.add_parser("mark-used")
    mark.add_argument("--secao", required=True)
    mark.add_argument("--item", required=True)
    mark.add_argument("--confirmacao", required=True)
    mark.add_argument("--grupo")
    mark.add_argument("--componentes", help="kit-catalogo: componente=id,... (padrão: o selecionado hoje)")
    mark.add_argument("--date")
    sub.add_parser("status")
    args = parser.parse_args()

    try:
        config = load_config()
        return {"select": cmd_select, "mark-used": cmd_mark_used, "status": cmd_status}[args.cmd](config, args)
    except NewsletterError as exc:
        print(json.dumps({"erro": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
