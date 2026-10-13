#!/usr/bin/env python3
"""Gera a skill `newsletter-<slug>` de um projeto a partir de um config/newsletter.json.

Uso:
  python scaffold_skill.py --config <arquivo.json> --check
  python scaffold_skill.py --config <arquivo.json> --project-root <raiz-do-projeto> [--force | --force-all]

--check      só valida o config e lista erros/avisos.
(sem flag)   cria só o que não existe; nada é sobrescrito.
--force      sobrescreve também a INFRAESTRUTURA (scripts/, assets/partials/ e o config).
             Use para levar melhorias dos scripts a uma skill já gerada.
--force-all  além disso, regenera arquivos de conteúdo (SKILL.md, template, referências,
             catálogos, modelos) — mas SÓ os que ainda contêm `TODO(criador)`.
             Arquivos já preenchidos nunca são sobrescritos.

Tudo que o scaffold não consegue decidir sozinho sai marcado com `TODO(criador)`.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parents[1]
ASSETS = HERE / "assets"
MODULES = HERE / "references" / "modulos"

TYPES = {"curadoria-externa", "rotacao-catalogo", "pool-sem-repeticao", "alternancia",
         "calendario", "fixado", "dados-ao-vivo", "bloco-fixo", "editorial", "kit-catalogo"}
STATEFUL = {"rotacao-catalogo", "pool-sem-repeticao", "alternancia", "fixado", "kit-catalogo"}
SELECTABLE = STATEFUL | {"calendario"}
CATALOG_TYPES = {"rotacao-catalogo", "pool-sem-repeticao", "alternancia"}
TYPE_LABELS = {
    "curadoria-externa": "curadoria de notícias", "rotacao-catalogo": "rotação em ordem",
    "pool-sem-repeticao": "sem repetição recente", "alternancia": "alternância de grupos",
    "calendario": "regra de calendário", "fixado": "campanha fixada", "dados-ao-vivo": "dados ao vivo",
    "bloco-fixo": "bloco fixo", "editorial": "texto da edição", "kit-catalogo": "kit com componentes compatíveis",
}
PLATFORMS = {
    "brevo": {"nome": "Brevo", "modulo": "brevo.md",
              "env": ["BREVO_API_KEY=", "# remetente verificado: o ID OU nome + e-mail", "BREVO_SENDER_ID=",
                      "BREVO_SENDER_NAME=", "BREVO_SENDER_EMAIL=", "# listas de destino, separadas por vírgula",
                      "BREVO_LIST_IDS="]},
    "mailerlite-classic": {"nome": "MailerLite Classic", "modulo": "mailerlite-classic.md",
                           "env": ["MAILERLITE_API_KEY=", "# destino: exatamente UM dos dois", "MAILERLITE_SEGMENT_ID=",
                                   "MAILERLITE_GROUP_ID=", "MAILERLITE_FROM_EMAIL=", "MAILERLITE_FROM_NAME="]},
    "mailerlite": {"nome": "MailerLite", "modulo": "mailerlite.md",
                   "env": ["# token: Integrations → MailerLite API → Generate new token", "MAILERLITE_API_TOKEN=",
                           "# destino: exatamente UM dos dois (IDs separados por vírgula)", "MAILERLITE_GROUP_IDS=",
                           "MAILERLITE_SEGMENT_IDS=", "# remetente verificado no MailerLite",
                           "MAILERLITE_FROM_EMAIL=", "MAILERLITE_FROM_NAME=",
                           "# idioma das páginas de descadastro/versão web (19 = Português do Brasil)",
                           "MAILERLITE_LANGUAGE_ID=19"]},
}
WEEKDAY_NAMES = {"seg": "segunda", "ter": "terça", "qua": "quarta", "qui": "quinta",
                 "sex": "sexta", "sab": "sábado", "dom": "domingo"}
TOKEN = re.compile(r"%%[A-Z0-9_]+%%")
TODO = "TODO(criador)"
DESCRIPTION_MAX = 1024


# ---------------------------------------------------------------- validação

def validate_config(cfg: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not re.fullmatch(r"[a-z0-9-]+", str(cfg.get("slug", ""))):
        errors.append("slug ausente ou inválido (use minúsculas, números e hífen).")
    for key in ("nome", "empresa"):
        if not cfg.get(key):
            errors.append(f"Campo raiz obrigatório ausente: {key}")
    if cfg.get("aprovacao") not in ("sempre", "dispensada-quando-solicitada-ou-agendada"):
        errors.append("aprovacao deve ser 'sempre' ou 'dispensada-quando-solicitada-ou-agendada'.")
    if not cfg.get("nome_campanha"):
        warnings.append("nome_campanha ausente — será usado '<nome> — {AAAA-MM-DD}'.")
    elif "{AAAA-MM-DD}" not in cfg["nome_campanha"] and "{DD/MM/AAAA}" not in cfg["nome_campanha"]:
        warnings.append("nome_campanha sem {AAAA-MM-DD} ou {DD/MM/AAAA} — todas as campanhas terão o mesmo nome.")

    for key in ("ekyte", "arquivo_publico"):
        if cfg.get(key):
            warnings.append(f"'{key}' não é mais suportado e será ignorado.")

    repo = cfg.get("aprovacao_repo") or {}
    if not repo.get("pasta"):
        errors.append("aprovacao_repo.pasta é obrigatório (pasta do cliente em aprovacoes-unid).")
    elif not re.fullmatch(r"[a-z0-9-]+", repo["pasta"]):
        errors.append("aprovacao_repo.pasta deve ter só minúsculas, números e hífen.")

    platform = cfg.get("plataforma") or {}
    ptype = platform.get("tipo")
    if ptype not in PLATFORMS:
        errors.append(f"plataforma.tipo deve ser um de {sorted(PLATFORMS)} (outra plataforma exige escrever um "
                      "adaptador em create_draft.py e registrá-lo aqui).")
    if not platform.get("variaveis_descadastro"):
        warnings.append("Nenhuma variável de descadastro declarada — confirme como a plataforma insere o link.")
    if ptype in ("mailerlite-classic", "mailerlite") and "{$unsubscribe}" not in platform.get("variaveis_html", []):
        errors.append(f"{PLATFORMS[ptype]['nome']} exige {{$unsubscribe}} em variaveis_html.")
    if ptype == "brevo" and "{{ unsubscribe }}" not in platform.get("variaveis_html", []):
        errors.append("Brevo exige {{ unsubscribe }} em variaveis_html.")

    visual = cfg.get("visual") or {}
    for key in ("cor_primaria", "cor_acento", "logo_fundo_escuro"):
        if not visual.get(key):
            warnings.append(f"visual.{key} ausente — o template sairá com {TODO}.")

    sections = cfg.get("secoes") or []
    if not sections:
        errors.append("secoes está vazio.")
    ids: set[str] = set()
    slots: set[str] = set()

    def add_slot(slot: str, owner: str) -> None:
        if not re.fullmatch(r"[A-Z0-9_]+", slot):
            errors.append(f"{owner}: slot '{slot}' deve ser MAIÚSCULAS_COM_UNDERSCORE.")
        if slot in slots:
            errors.append(f"{owner}: slot '{slot}' repetido.")
        slots.add(slot)

    def check_selectable(spec: dict[str, Any], owner: str) -> None:
        tipo = spec.get("tipo")
        if tipo in CATALOG_TYPES and not spec.get("catalogo"):
            errors.append(f"{owner}: tipo {tipo} exige 'catalogo'.")
        if tipo == "kit-catalogo":
            if not spec.get("catalogo"):
                errors.append(f"{owner}: kit-catalogo exige 'catalogo' (itens principais).")
            if not spec.get("componentes"):
                errors.append(f"{owner}: kit-catalogo exige 'componentes'.")
            for comp in spec.get("componentes", []):
                if not comp.get("id") or not comp.get("catalogo"):
                    errors.append(f"{owner}: cada componente precisa de 'id' e 'catalogo'.")
        if tipo == "alternancia" and not spec.get("grupos"):
            errors.append(f"{owner}: alternancia exige 'grupos'.")
        if tipo == "calendario":
            if spec.get("regra") not in ("semana-iso-paridade", "dia-da-semana", "mes"):
                errors.append(f"{owner}: regra de calendário inválida.")
            if not spec.get("opcoes"):
                errors.append(f"{owner}: calendario exige 'opcoes'.")

    for spec in sections:
        sid = spec.get("id")
        owner = f"seção '{sid}'"
        if not sid or not re.fullmatch(r"[a-z0-9-]+", sid):
            errors.append(f"Seção com id ausente/inválido: {sid!r}")
        if sid in ids:
            errors.append(f"{owner}: id repetido.")
        ids.add(sid)
        tipo = spec.get("tipo")
        if tipo not in TYPES:
            errors.append(f"{owner}: tipo desconhecido '{tipo}'.")
            continue
        if not spec.get("titulo"):
            errors.append(f"{owner}: 'titulo' é obrigatório.")

        if tipo == "curadoria-externa":
            if spec.get("slot"):
                warnings.append(f"{owner}: 'slot' no nível da curadoria é ignorado — os slots ficam em cada bloco.")
            if not spec.get("fontes_obrigatorias"):
                errors.append(f"{owner}: curadoria exige pelo menos uma fonte obrigatória.")
            if not spec.get("blocos"):
                errors.append(f"{owner}: curadoria exige 'blocos'.")
            for bloco in spec.get("blocos", []):
                if int(bloco.get("quantidade", 0)) != len(bloco.get("slots", [])):
                    errors.append(f"{owner}: bloco '{bloco.get('id')}' com quantidade diferente do número de slots.")
                for slot in bloco.get("slots", []):
                    add_slot(slot, owner)
            if spec.get("janela_dias") is None:
                errors.append(f"{owner}: 'janela_dias' é obrigatório.")
            continue

        if spec.get("slot"):
            add_slot(spec["slot"], owner)
        elif tipo not in ("bloco-fixo", "editorial"):
            errors.append(f"{owner}: 'slot' é obrigatório para o tipo {tipo}.")

        check_selectable(spec, owner)
        if tipo == "fixado":
            if not (spec.get("item") or spec.get("modelo")):
                errors.append(f"{owner}: fixado exige 'item' (com catalogo) ou 'modelo'.")
            if spec.get("item") and not spec.get("catalogo"):
                errors.append(f"{owner}: fixado com 'item' exige 'catalogo'.")
            senao = spec.get("senao")
            if senao:
                if senao.get("tipo") == "fixado" or senao.get("tipo") not in SELECTABLE:
                    errors.append(f"{owner}: 'senao' deve ser rotacao-catalogo, pool-sem-repeticao, alternancia ou calendario.")
                else:
                    check_selectable(senao, f"{owner} (senao)")
            if spec.get("ate") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", spec["ate"]):
                errors.append(f"{owner}: 'ate' deve ser AAAA-MM-DD.")
        if tipo == "dados-ao-vivo":
            if not spec.get("url"):
                errors.append(f"{owner}: dados-ao-vivo exige 'url'.")
            key = "caminho" if spec.get("fonte") == "json" else "regex"
            for campo in spec.get("campos", []):
                if not campo.get(key):
                    errors.append(f"{owner}: campo '{campo.get('id')}' sem '{key}'.")
            if not spec.get("campos"):
                errors.append(f"{owner}: dados-ao-vivo exige 'campos'.")

    return errors, warnings


# ---------------------------------------------------------------- utilidades

def fill(text: str, tokens: dict[str, str]) -> str:
    for key, value in tokens.items():
        text = text.replace(f"%%{key}%%", value)
    return text


def leftover_tokens(text: str) -> list[str]:
    return sorted(set(TOKEN.findall(text)))


class Writer:
    """Grava arquivos respeitando a política de sobrescrita.

    infra=True    → scripts, parciais e config: sobrescritos com --force ou --force-all.
    infra=False   → conteúdo: sobrescrito só com --force-all e só se ainda tiver TODO(criador).
    """

    def __init__(self, root: Path, force: bool, force_all: bool) -> None:
        self.root = root
        self.force = force or force_all
        self.force_all = force_all
        self.created: list[str] = []
        self.updated: list[str] = []
        self.preserved: list[str] = []

    def rel(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return str(path)

    def _may_overwrite(self, path: Path, infra: bool) -> bool:
        if infra:
            return self.force
        if not self.force_all:
            return False
        try:
            return TODO in path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return False

    def write(self, path: Path, content: str, infra: bool = False) -> None:
        bad = leftover_tokens(content)
        if bad:
            raise SystemExit(f"Bug no scaffold: tokens não substituídos em {path.name}: {bad}")
        if path.exists():
            if not self._may_overwrite(path, infra):
                self.preserved.append(self.rel(path))
                return
            if path.read_text(encoding="utf-8") == content:
                return
            self.updated.append(self.rel(path))
        else:
            self.created.append(self.rel(path))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def copy(self, src: Path, dest: Path) -> None:
        self.write(dest, src.read_text(encoding="utf-8"), infra=True)


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def agenda_text(cfg: dict[str, Any]) -> str:
    agenda = cfg.get("agenda") or {}
    days = [WEEKDAY_NAMES.get(d, d) for d in agenda.get("dias", [])]
    if not days:
        return f"{TODO}: frequência"
    joined = days[0] if len(days) == 1 else ", ".join(days[:-1]) + " e " + days[-1]
    return f"toda {joined}" + (f" às {agenda['hora']}" if agenda.get("hora") else "")


def approval_values(cfg: dict[str, Any]) -> dict[str, str]:
    repo = cfg.get("aprovacao_repo") or {}
    return {
        "local": repo.get("local", "../aprovacoes-unid"),
        "pasta": repo.get("pasta", cfg.get("slug", "")),
        "base": repo.get("base_url", "https://unidcom.github.io/aprovacoes-unid").rstrip("/"),
        "arquivo": repo.get("nome_arquivo", "newsletter-{AAAA-MM-DD}.html").replace("{AAAA-MM-DD}", "AAAA-MM-DD"),
    }


def visual_tokens(cfg: dict[str, Any]) -> dict[str, str]:
    v = cfg.get("visual") or {}
    platform = cfg.get("plataforma") or {}
    rodape = cfg.get("rodape") or {}
    lines = list(rodape.get("linhas", []))
    if rodape.get("site"):
        site_label = re.sub(r"^https?://(www\.)?", "", rodape["site"]).rstrip("/")
        lines.append(f'<a href="{rodape["site"]}" style="color:#FFFFFF;">{site_label}</a>')
    return {
        "COR_PRIMARIA": v.get("cor_primaria", "#333333"),
        "COR_ACENTO": v.get("cor_acento", "#F28A25"),
        "COR_TEXTO": v.get("cor_texto", "#263442"),
        "COR_FUNDO": v.get("cor_fundo", "#F3F6F9"),
        "COR_ESCURA": v.get("cor_escura", "#1D2935"),
        "COR_SUAVE": v.get("cor_suave", "#EEF5FC"),
        "FONTE": v.get("fonte", "Arial,Helvetica,sans-serif"),
        "LOGO_FUNDO_ESCURO": v.get("logo_fundo_escuro") or "https://TODO(criador)/logo-branco.png",
        "EMPRESA": cfg.get("empresa", ""),
        "VAR_ESPELHO": (platform.get("variaveis_espelho") or ["TODO(criador):variavel-espelho"])[0],
        "VAR_DESCADASTRO": (platform.get("variaveis_descadastro") or ["TODO(criador):variavel-descadastro"])[0],
        "RODAPE": "<br>\n          ".join(lines) if lines else f"<!-- {TODO}: endereço e contatos -->",
        "MOTIVO_RECEBIMENTO": rodape.get("motivo") or f"<!-- {TODO}: motivo pelo qual o contato recebe este e-mail -->",
    }


# ---------------------------------------------------------------- template

def section_rows(cfg: dict[str, Any], vt: dict[str, str]) -> str:
    rows: list[str] = []
    font = vt["FONTE"]
    text_color = vt["COR_TEXTO"]
    for spec in cfg.get("secoes", []):
        tipo = spec["tipo"]
        rows.append(f"        <!-- seção: {spec['id']} ({tipo}) -->")
        if tipo == "editorial":
            if spec.get("slot"):
                rows.append(f'        <tr><td style="padding:30px 34px 14px;color:{text_color};font:400 15px/1.7 {font};">'
                            f'<p style="margin:0;">{{{{{spec["slot"]}}}}}</p></td></tr>')
        elif tipo == "curadoria-externa":
            labels = [part.strip() for part in spec.get("titulo", "").split("/")]
            for idx, bloco in enumerate(spec.get("blocos", [])):
                label = (bloco.get("rotulo") or (labels[idx] if idx < len(labels) else bloco["id"])).upper()
                if bloco.get("parcial"):
                    rows.append(f'        <tr><td style="padding:16px 34px 8px;color:{vt["COR_PRIMARIA"]};font:800 12px {font};letter-spacing:1.5px;">{label}</td></tr>')
                    for slot in bloco["slots"]:
                        rows.append(f'        <tr><td style="padding:0 34px 12px;">{{{{{slot}}}}}</td></tr>')
                else:
                    inner = "\n".join(f"          {{{{{slot}}}}}" for slot in bloco["slots"])
                    rows.append(f'        <tr><td bgcolor="{vt["COR_SUAVE"]}" style="padding:24px 34px;background-color:{vt["COR_SUAVE"]};">\n'
                                f'          <p style="margin:0 0 14px;color:{vt["COR_PRIMARIA"]};font:800 12px {font};letter-spacing:1.5px;">{label}</p>\n'
                                f"{inner}\n        </td></tr>")
        elif tipo == "dados-ao-vivo":
            rows.append(f'        <tr><td style="padding:0;">{{{{{spec["slot"]}}}}}</td></tr>')
        elif tipo == "bloco-fixo":
            values = spec.get("valores") or {}
            if values:
                width = max(1, 100 // len(values))
                cells = "".join(
                    f'<td align="center" width="{width}%" style="padding:22px 6px;color:#FFFFFF;font:800 22px {font};">{val}'
                    f'<br><span style="font:500 11px {font};">{TODO}: rótulo de {key}</span></td>'
                    for key, val in values.items())
                rows.append(f'        <tr><td bgcolor="{vt["COR_PRIMARIA"]}" style="background-color:{vt["COR_PRIMARIA"]};padding:0 12px;">'
                            f'<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"><tr>{cells}</tr></table></td></tr>')
            elif spec.get("slot"):
                rows.append(f'        <tr><td style="padding:0 34px 24px;">{{{{{spec["slot"]}}}}}</td></tr>')
            else:
                rows.append(f"        <!-- {TODO}: HTML fixo de '{spec['titulo']}' -->")
        else:
            rows.append(f'        <tr><td style="padding:0 34px 24px;">{{{{{spec["slot"]}}}}}</td></tr>')
    return "\n".join(rows)


def plain_text(cfg: dict[str, Any]) -> str:
    platform = cfg.get("plataforma") or {}
    rodape = cfg.get("rodape") or {}
    text_vars = platform.get("variaveis_texto", [])
    mirror = next((v for v in platform.get("variaveis_espelho", []) if v in text_vars), None)
    unsub = next((v for v in platform.get("variaveis_descadastro", []) if v in text_vars), None)
    out = [f"{cfg['empresa'].upper()} — {{{{EDITION_DATE}}}}", ""]
    if mirror:
        out += [f"Ver no navegador: {mirror}", ""]
    for spec in cfg.get("secoes", []):
        if spec["tipo"] == "editorial":
            if spec.get("slot"):
                out += [f"{{{{{spec['slot']}_PLAIN}}}}", ""]
        elif spec["tipo"] == "curadoria-externa":
            labels = [part.strip() for part in spec.get("titulo", "").split("/")]
            for idx, bloco in enumerate(spec.get("blocos", [])):
                label = bloco.get("rotulo") or (labels[idx] if idx < len(labels) else bloco["id"])
                out += [label.upper(), "", f"{{{{{bloco['id'].upper().replace('-', '_')}_PLAIN}}}}", ""]
        elif spec["tipo"] == "bloco-fixo" and not spec.get("slot"):
            continue
        else:
            out += [spec["titulo"].upper(), f"{{{{{spec.get('slot', spec['id'].upper())}_PLAIN}}}}", ""]
    out += [cfg["empresa"], *[re.sub(r"<[^>]+>", "", line) for line in rodape.get("linhas", [])]]
    if rodape.get("site"):
        out.append(rodape["site"])
    out += ["", rodape.get("motivo") or f"{TODO}: motivo pelo qual o contato recebe este e-mail."]
    if unsub:
        out.append(f"Cancelar inscrição: {unsub}")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- SKILL.md

def how_it_pulls(spec: dict[str, Any]) -> str:
    tipo = spec["tipo"]
    if tipo == "curadoria-externa":
        blocks = " + ".join(f"{b['quantidade']} {b['id']}" for b in spec.get("blocos", []))
        return f"busca em {len(spec.get('fontes_obrigatorias', []))} fontes obrigatórias, últimos {spec.get('janela_dias')} dias → {blocks}"
    if tipo == "rotacao-catalogo":
        return f"próximo item de `{spec['catalogo']}`, ordem circular"
    if tipo == "kit-catalogo":
        comps = " + ".join(c["id"] + (" (opcional)" if c.get("opcional") else "") for c in spec.get("componentes", []))
        return f"próximo de `{spec['catalogo']}` em ordem circular + {comps} compatíveis, o usado há mais tempo"
    if tipo == "pool-sem-repeticao":
        return f"item de `{spec['catalogo']}` fora dos últimos {spec.get('janela_itens', 10)} usados"
    if tipo == "alternancia":
        return f"alterna {' ↔ '.join(spec.get('grupos', []))}; circular dentro do grupo"
    if tipo == "calendario":
        return f"regra `{spec.get('regra')}` → " + ", ".join(f"{k}: {v.get('id', k)}" for k, v in spec.get("opcoes", {}).items())
    if tipo == "fixado":
        base = f"sempre `{spec.get('item') or spec.get('modelo')}`" + (f" até {spec['ate']}" if spec.get("ate") else "")
        return base + (f"; depois: {how_it_pulls({**spec['senao'], 'id': spec['id']})}" if spec.get("senao") else "")
    if tipo == "dados-ao-vivo":
        return f"captura ao vivo em {spec.get('url')} ({', '.join(c.get('rotulo') or c['id'] for c in spec.get('campos', []))})"
    if tipo == "bloco-fixo":
        return "fixo" + (": " + ", ".join(spec["valores"].values()) if spec.get("valores") else " (no template)")
    return "escrito a cada edição a partir do conteúdo selecionado"


def advances_when(spec: dict[str, Any]) -> str:
    return "`mark-used` após o `campaign_id` do rascunho" if spec["tipo"] in STATEFUL else "—"


def section_details(spec: dict[str, Any]) -> str:
    tipo = spec["tipo"]
    if tipo == "curadoria-externa":
        lines = [f"- **Janela:** últimos {spec.get('janela_dias')} dias (máximo {spec.get('janela_max_dias', spec.get('janela_dias'))} se faltar material, registrando a exceção)."]
        lines.append("- **Fontes obrigatórias:**\n" + "\n".join(f"  - {f['nome']}: {f['url']}" for f in spec.get("fontes_obrigatorias", [])))
        if spec.get("fontes_complementares"):
            lines.append("- **Fontes complementares:**\n" + "\n".join(f"  - {f['nome']}: {f['url']}" for f in spec["fontes_complementares"]))
        if spec.get("evitar"):
            lines.append("- **Evitar:** " + "; ".join(spec["evitar"]) + ".")
        lines.append("\n| Bloco | Quantidade | Slots | Campos |\n|---|---:|---|---|")
        for b in spec.get("blocos", []):
            campos = "; ".join(f"`{k}`: {v}" for k, v in (b.get("campos") or {}).items())
            parcial = f" (parcial `{b['parcial']}`)" if b.get("parcial") else " (parcial `assets/partials/quick-item.html`)"
            lines.append(f"| {b['id']}{parcial} | {b['quantidade']} (exato) | {', '.join('`{{' + s + '}}`' for s in b['slots'])} | {campos} |")
        return "\n".join(lines)
    if tipo == "calendario":
        rows = "\n".join(f"| `{k}` | {v.get('id', k)} | `{v.get('modelo', '—')}` |" for k, v in spec.get("opcoes", {}).items())
        return f"| Chave | Opção | Modelo |\n|---|---|---|\n{rows}"
    if tipo == "fixado":
        lines = [f"- **Item fixado:** `{spec.get('item') or spec.get('modelo')}`" + (f" do catálogo `{spec['catalogo']}`" if spec.get("catalogo") else "")]
        lines.append(f"- **Vale até:** {spec['ate']}" if spec.get("ate") else "- **Vale até:** sem data — enquanto a campanha estiver ativa (desativar no catálogo para encerrar).")
        if spec.get("senao"):
            lines.append(f"- **Depois (regra `senao`):** {how_it_pulls({**spec['senao'], 'id': spec['id']})}")
        if spec.get("substituicao_pontual"):
            lines.append(f"- **Substituição pontual:** {spec['substituicao_pontual']}")
        return "\n".join(lines)
    if tipo == "dados-ao-vivo":
        rows = "\n".join(f"| `{c['id']}` | {c.get('rotulo', '')} | {c.get('formato', '')} |" for c in spec.get("campos", []))
        return (f"- **Fonte:** `{spec.get('metodo', 'GET')} {spec.get('url')}` ({spec.get('fonte', 'html')}), até {spec.get('tentativas', 2)} tentativas.\n\n"
                f"| Campo | Rótulo | Formato |\n|---|---|---|\n{rows}")
    if tipo == "bloco-fixo":
        if spec.get("valores"):
            return "Valores aprovados (exibir exatamente):\n" + bullet_list([f"`{k}`: **{v}**" for k, v in spec["valores"].items()])
        return "Conteúdo definido no próprio `assets/template.html`."
    if tipo == "editorial":
        return bullet_list([f"`{k}`: {v}" for k, v in (spec.get("campos") or {}).items()]) or f"{TODO}: regras de redação."
    return ""


def section_fragment(spec: dict[str, Any], tokens: dict[str, str]) -> str:
    text = (ASSETS / "passos" / "secao" / f"{spec['tipo']}.md").read_text(encoding="utf-8")
    local = {
        **tokens,
        "ID": spec["id"],
        "TITULO": spec["titulo"],
        "SLOT": spec.get("slot", ""),
        "CATALOGO": spec.get("catalogo", ""),
        "JANELA_ITENS": str(spec.get("janela_itens", 10)),
        "GRUPOS": " ↔ ".join(f"`{g}`" for g in spec.get("grupos", [])),
        "REGRA": spec.get("regra", ""),
        "ATE": f" até {spec['ate']}" if spec.get("ate") else "",
        "DETALHES": section_details(spec),
    }
    return fill(text, local).strip()


def flow_fragment(name: str, tokens: dict[str, str]) -> tuple[str, str]:
    text = fill((ASSETS / "passos" / "fluxo" / f"{name}.md").read_text(encoding="utf-8"), tokens).strip()
    title, _, body = text.partition("\n")
    return title.lstrip("# ").strip(), body.strip()


def build_description(cfg: dict[str, Any], warnings: list[str]) -> str:
    platform_name = PLATFORMS[cfg["plataforma"]["tipo"]]["nome"]
    sections = [s for s in cfg["secoes"] if s["tipo"] not in ("editorial", "bloco-fixo")]
    head = f"Gera a {cfg['nome']} da {cfg['empresa']} ({agenda_text(cfg)})"
    tail = (f". Monta HTML e plain text, publica para aprovação em aprovacoes-unid e cria o rascunho na {platform_name} "
            f"pela API (sem disparar). Use quando o usuário pedir para montar, gerar, preparar ou enviar a newsletter da "
            f"{cfg['empresa']}, pedir a edição do dia/da semana ou mencionar '$newsletter-{cfg['slug']}'.")

    def summary(full: bool) -> str:
        if full:
            return "; ".join(f"{s['titulo']} ({TYPE_LABELS[s['tipo']]})" for s in sections)
        return "; ".join(s["titulo"] for s in sections)

    for full in (True, False):
        text = f"{head}: {summary(full)}{tail}" if sections else f"{head}{tail}"
        if len(text) <= DESCRIPTION_MAX:
            return text.replace('"', "'")
    warnings.append(f"description gerada passou de {DESCRIPTION_MAX} caracteres e foi encurtada — revisar.")
    return f"{head}{tail}"[:DESCRIPTION_MAX].replace('"', "'")


def build_skill_md(cfg: dict[str, Any], tokens: dict[str, str], warnings: list[str]) -> str:
    sections = cfg["secoes"]
    ptype = cfg["plataforma"]["tipo"]
    has = lambda kinds: any(s["tipo"] in kinds for s in sections)  # noqa: E731

    steps: list[tuple[str, str]] = [flow_fragment("data-pasta", tokens)]
    if has({"dados-ao-vivo"}):
        steps.append(flow_fragment("dados-ao-vivo", tokens))
    if has(SELECTABLE):
        steps.append(flow_fragment("selecao", tokens))
    title, intro = flow_fragment("conteudo", tokens)
    parts = [intro]
    for spec in sections:
        if spec["tipo"] != "editorial":
            parts.append(f"#### {spec['titulo']} (`{spec['id']}`)\n\n{section_fragment(spec, tokens)}")
    steps.append((title, "\n\n".join(parts)))
    editoriais = "\n\n".join(f"#### {s['titulo']} (`{s['id']}`)\n\n{section_fragment(s, tokens)}"
                             for s in sections if s["tipo"] == "editorial")
    steps.append(flow_fragment("redacao", {**tokens, "EDITORIAIS": editoriais}))
    steps.append(flow_fragment("montagem", tokens))
    steps.append(flow_fragment("salvar-validar", tokens))
    # Aprovação vem antes de qualquer chamada à plataforma de e-mail.
    steps.append(flow_fragment("aprovacao-repo", tokens))
    steps.append(flow_fragment("criar-rascunho", tokens))
    if has(STATEFUL):
        steps.append(flow_fragment("confirmar-rotacao", tokens))
    flow = "\n\n".join(f"### Passo {i} — {title}\n\n{body}" for i, (title, body) in enumerate(steps))

    table = ["| # | Seção | Tipo | Como puxa | Slot | Estado avança |", "|---:|---|---|---|---|---|"]
    for i, s in enumerate(sections, 1):
        slot = (", ".join(f"`{{{{{x}}}}}`" for b in s.get("blocos", []) for x in b["slots"]) if s["tipo"] == "curadoria-externa"
                else (f"`{{{{{s['slot']}}}}}`" if s.get("slot") else "—"))
        table.append(f"| {i} | {s['titulo']} (`{s['id']}`) | {TYPE_LABELS[s['tipo']]} (`{s['tipo']}`) | {how_it_pulls(s)} | {slot} | {advances_when(s)} |")

    rules = fill((ASSETS / "passos" / "regras.md").read_text(encoding="utf-8"), tokens).strip()

    refs = ["- `config/newsletter.json` — fonte de verdade das seções, plataforma e aprovação.",
            "- `references/empresa-e-ofertas.md` — posicionamento, público, provas, ofertas e rodapé.",
            "- `references/identidade-visual.md` — marca e regras de HTML para e-mail."]
    if has({"curadoria-externa"}):
        refs.append("- `references/curadoria-editorial.md` — escopo, fontes e critérios das notícias.")
    refs.append("- `references/aprovacao.md` — publicação em aprovacoes-unid, link e falhas.")
    refs.append(f"- `references/{PLATFORMS[ptype]['modulo']}` — API da {PLATFORMS[ptype]['nome']}, credenciais e rascunho.")

    return f"""---
name: newsletter-{cfg['slug']}
description: {build_description(cfg, warnings)}
---

# {cfg['nome']}

{TODO}: um parágrafo com o propósito da newsletter, o público e o objetivo (relacionamento, geração de oportunidades…), a partir do briefing em `docs/briefing-newsletter-{cfg['slug']}.md`.

**Agendamento de referência:** {agenda_text(cfg)} (`{cfg.get('fuso', 'America/Sao_Paulo')}`). O agendamento em si é configurado à parte (skill `schedule`); esta skill não se agenda sozinha.

## Regras operacionais

{rules}

## Seções da newsletter

A ordem abaixo é a ordem no e-mail. A especificação completa de cada seção está em `config/newsletter.json` — se uma seção mudar, atualizar o config, o template e o passo correspondente.

{chr(10).join(table)}

## Fluxo

{flow}

## Referências

{chr(10).join(refs)}
"""


# ---------------------------------------------------------------- stubs

def catalog_specs(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    for spec in cfg["secoes"]:
        for candidate in (spec, spec.get("senao") or {}):
            if candidate.get("catalogo"):
                entry = found.setdefault(candidate["catalogo"], {"catalogo": candidate["catalogo"], "grupos": set(), "itens": set()})
                entry["grupos"].update(candidate.get("grupos", []))
                if candidate.get("item"):
                    entry["itens"].add(candidate["item"])
    return list(found.values())


def model_stub(name: str) -> str:
    return (f"<!-- {TODO}: modelo HTML do item '{name}'. Use tabelas e CSS inline; pode partir de "
            f"assets/partials/catalog-card.html. -->\n")


def build_tokens(cfg: dict[str, Any], skill_rel: str) -> dict[str, str]:
    platform = cfg["plataforma"]
    ptype = platform["tipo"]
    pasta = cfg.get("edicoes", {}).get("pasta", "newsletter")
    aprov = approval_values(cfg)
    stateful = []
    for s in cfg["secoes"]:
        if s["tipo"] in STATEFUL:
            grupo = " --grupo <GRUPO>" if s["tipo"] == "alternancia" or (s.get("senao") or {}).get("tipo") == "alternancia" else ""
            stateful.append(f"python {skill_rel}/scripts/rotation.py mark-used --secao {s['id']} --item <ITEM> "
                            f"--confirmacao <CAMPAIGN_ID>{grupo} --date AAAA-MM-DD")
    approval = {
        "sempre": "**sempre parar aqui**, mandar o link de aprovação e esperar o OK do usuário antes de criar o rascunho na plataforma.",
        "dispensada-quando-solicitada-ou-agendada": "em execução explicitamente solicitada ou agendada, mandar o link e seguir **sem** esperar aprovação. Em teste, dúvida ou pedido de preview, mandar o link e parar.",
    }[cfg["aprovacao"]]
    return {
        "SLUG": cfg["slug"],
        "NOME": cfg["nome"],
        "EMPRESA": cfg["empresa"],
        "FUSO": cfg.get("fuso", "America/Sao_Paulo"),
        # Com edicoes.subpastas ("{AAAA}/{MM}"), os passos mostram Newsletter/AAAA/MM/AAAA-MM-DD/.
        "PASTA": pasta + ("/" + cfg["edicoes"]["subpastas"].replace("{", "").replace("}", "")
                          if cfg.get("edicoes", {}).get("subpastas") else ""),
        "ESTADO": cfg.get("estado", f"{pasta}/.rotation-state.json"),
        "SKILL_REL": skill_rel,
        "ASSUNTO_MAX": str(cfg.get("assunto_max", 70)),
        "NOME_CAMPANHA": cfg.get("nome_campanha") or f"{cfg['nome']} — {{AAAA-MM-DD}}",
        "VARS_HTML": ", ".join(f"`{v}`" for v in platform.get("variaveis_html", [])) or "(nenhuma)",
        "VARS_TEXTO": ", ".join(f"`{v}`" for v in platform.get("variaveis_texto", [])) or "(nenhuma)",
        "PROIBIDO": (" Nunca usar: " + ", ".join(f"`{v}`" for v in platform.get("proibido", [])) + ".") if platform.get("proibido") else "",
        "PLATAFORMA": ptype,
        "PLATAFORMA_NOME": PLATFORMS[ptype]["nome"],
        "PLATAFORMA_REF": PLATFORMS[ptype]["modulo"],
        "CREDENCIAIS": platform.get("credenciais") or f"private/{ptype}.env",
        "COMANDOS_MARK_USED": "\n".join(stateful),
        "REGRA_APROVACAO": approval,
        "APROV_LOCAL": aprov["local"],
        "APROV_PASTA": aprov["pasta"],
        "APROV_BASE": aprov["base"],
        "APROV_ARQUIVO": aprov["arquivo"],
    }


def ensure_gitignore(project: Path, entries: list[str]) -> list[str]:
    path = project / ".gitignore"
    current = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    normalized = {line.strip().rstrip("/") for line in current}
    missing = [e for e in entries if e.rstrip("/") not in normalized]
    if missing:
        block = ([""] if current and current[-1].strip() else []) + ["# newsletter (criador-skill-newsletter)"] + missing
        path.write_text("\n".join(current + block) + "\n", encoding="utf-8")
    return missing


# ---------------------------------------------------------------- main

def scaffold(cfg: dict[str, Any], project: Path, force: bool, force_all: bool, warnings: list[str]) -> dict[str, Any]:
    skill_rel = f".agents/skills/newsletter-{cfg['slug']}"
    skill = project / skill_rel
    w = Writer(project, force, force_all)
    tokens = build_tokens(cfg, skill_rel)
    vt = visual_tokens(cfg)
    ptype = cfg["plataforma"]["tipo"]

    # infraestrutura: config, scripts e parciais
    w.write(skill / "config" / "newsletter.json", json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", infra=True)
    for src in sorted((ASSETS / "skill-base" / "scripts").glob("*.py")):
        if src.name == "fetch_live_data.py" and not any(s["tipo"] == "dados-ao-vivo" for s in cfg["secoes"]):
            continue
        w.copy(src, skill / "scripts" / src.name)
    for src in sorted((ASSETS / "email" / "partials").glob("*.html")):
        w.write(skill / "assets" / "partials" / src.name, fill(src.read_text(encoding="utf-8"), vt), infra=True)

    # conteúdo: template e texto
    base = (ASSETS / "email" / "base.html").read_text(encoding="utf-8")
    w.write(skill / "assets" / "template.html", fill(base, {**vt, "SECOES": section_rows(cfg, vt)}))
    w.write(skill / "assets" / "plain-text-template.txt", plain_text(cfg))

    # catálogos e modelos
    for entry in catalog_specs(cfg):
        folder = Path(entry["catalogo"]).parent.as_posix()

        def stub_item(item_id: str, group: str | None = None) -> dict[str, Any]:
            item = {"id": item_id, "ativo": True, "modelo": f"{folder}/models/{item_id}.html",
                    "dados": {TODO: "dados reais do item (números, segmento, URL do CTA)"}}
            if group:
                item["grupo"] = group
            return item

        cat_path = skill / entry["catalogo"]
        if cat_path.exists() and not w._may_overwrite(cat_path, infra=False):
            w.preserved.append(w.rel(cat_path))
            continue
        items = [stub_item(name) for name in sorted(entry["itens"])]
        items += [stub_item(f"{group}-1", group) for group in sorted(entry["grupos"])]
        if not items:
            items = [stub_item("item-1"), stub_item("item-2")]
        for item in items:
            w.write(skill / item["modelo"], model_stub(item["id"]))
        w.write(cat_path, json.dumps(items, ensure_ascii=False, indent=2) + "\n")
    for spec in cfg["secoes"]:
        for option in (spec.get("opcoes") or {}).values():
            if option.get("modelo"):
                w.write(skill / option["modelo"], model_stub(option.get("id", "opção")))
        if spec["tipo"] == "fixado" and spec.get("modelo"):
            w.write(skill / spec["modelo"], model_stub(spec["id"]))

    # referências
    refs = skill / "references"
    base_refs = ASSETS / "skill-base" / "references"
    w.write(refs / "empresa-e-ofertas.md", fill((base_refs / "empresa-e-ofertas.md").read_text(encoding="utf-8"), tokens))
    w.write(refs / "identidade-visual.md", fill((base_refs / "identidade-visual.md").read_text(encoding="utf-8"),
                                                {**tokens, **{f"V_{k}": v for k, v in vt.items()}}))
    for spec in cfg["secoes"]:
        if spec["tipo"] == "curadoria-externa":
            w.write(refs / "curadoria-editorial.md",
                    fill((base_refs / "curadoria-editorial.md").read_text(encoding="utf-8"), {**tokens, "DETALHES": section_details(spec)}))
            break
    # Referências técnicas (API, aprovação) não são editadas à mão: atualizam com --force.
    module = PLATFORMS[ptype]["modulo"]
    w.write(refs / module, fill((MODULES / module).read_text(encoding="utf-8"), tokens), infra=True)
    w.write(refs / "aprovacao.md", fill((MODULES / "aprovacao.md").read_text(encoding="utf-8"), tokens), infra=True)

    # agents + SKILL.md
    w.write(skill / "agents" / "openai.yaml", fill((ASSETS / "skill-base" / "agents" / "openai.yaml").read_text(encoding="utf-8"),
                                                    {**tokens, "COR_MARCA": cfg.get("cor_marca", vt["COR_PRIMARIA"])}))
    w.write(skill / "SKILL.md", build_skill_md(cfg, tokens, warnings))

    # credenciais (modelo sem valores) e .gitignore
    # O modelo fica versionado na skill; o arquivo preenchido fica em private/ (ignorado).
    creds_rel = tokens["CREDENCIAIS"]
    w.write(skill / "config" / f"{ptype}.env.exemplo",
            f"# Copie para {creds_rel} (na raiz do projeto) e preencha. Nunca versionar o arquivo preenchido.\n"
            + "\n".join(PLATFORMS[ptype]["env"]) + "\n", infra=True)
    gitignore_added = ensure_gitignore(project, [f"{Path(creds_rel).parent.as_posix()}/"])

    todos = []
    for path in skill.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".html", ".json", ".txt", ".yaml", ".yml"}:
            count = path.read_text(encoding="utf-8").count(TODO)
            if count:
                todos.append({"arquivo": w.rel(path), "todos": count})
    return {"skill": str(skill), "criados": w.created, "atualizados": w.updated, "preservados": w.preserved,
            "gitignore_adicionado": gitignore_added, "pendencias_todo": todos}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--check", action="store_true")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--force", action="store_true")
    mode.add_argument("--force-all", action="store_true")
    args = parser.parse_args()

    try:
        cfg = json.loads(args.config.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "erros": [f"Config ilegível: {exc}"]}, ensure_ascii=False))
        return 1
    errors, warnings = validate_config(cfg)
    if args.check or errors:
        print(json.dumps({"ok": not errors, "erros": errors, "avisos": warnings}, ensure_ascii=False, indent=2))
        return 0 if not errors else 1
    if not args.project_root:
        print(json.dumps({"ok": False, "erros": ["Informe --project-root para gerar a skill."]}, ensure_ascii=False))
        return 1
    for key in ("ekyte", "arquivo_publico"):
        cfg.pop(key, None)
    report = scaffold(cfg, args.project_root.resolve(), args.force, args.force_all, warnings)
    report["avisos"] = warnings
    print(json.dumps({"ok": True, **report}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
