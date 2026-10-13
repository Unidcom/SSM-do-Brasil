#!/usr/bin/env python3
"""Busca os valores das seções `dados-ao-vivo` declaradas em config/newsletter.json.

Uso:
  python fetch_live_data.py [--secao ID] [--tentativas N]

Imprime JSON com o valor bruto de cada campo. Sai com código 1 se qualquer campo
não puder ser confirmado — nesse caso a edição deve parar (nunca reaproveitar
valores de edições anteriores nem estimar).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from typing import Any
from urllib import request
from urllib.error import HTTPError, URLError

from _newsletter_common import NewsletterError, load_config, section_by_id

USER_AGENT = "Mozilla/5.0 (newsletter-skill live-data)"
PATH_TOKEN = re.compile(r"^([^\[\]]*)((?:\[[^\]]+\])*)$")


def fetch(spec: dict[str, Any]) -> str:
    method = spec.get("metodo", "GET").upper()
    body = None
    headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    if method != "GET":
        body = json.dumps(spec.get("corpo", {})).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = request.Request(spec["url"], data=body, method=method, headers=headers)
    with request.urlopen(req, timeout=int(spec.get("timeout", 30))) as response:
        return response.read().decode("utf-8", errors="replace")


def walk(data: Any, path: str) -> Any:
    """Caminho simples: `a.b[0].c` ou `data[title=_active-subscribers].total`."""
    current = data
    for part in path.split("."):
        match = PATH_TOKEN.match(part)
        if not match:
            raise NewsletterError(f"Caminho inválido: {path}")
        key, filters = match.groups()
        if key:
            if not isinstance(current, dict) or key not in current:
                raise NewsletterError(f"Chave ausente: {key}")
            current = current[key]
        for flt in re.findall(r"\[([^\]]+)\]", filters):
            if flt.isdigit():
                current = current[int(flt)]
                continue
            fkey, _, fval = flt.partition("=")
            if not isinstance(current, list):
                raise NewsletterError(f"Filtro [{flt}] aplicado a algo que não é lista")
            matches = [item for item in current if isinstance(item, dict) and str(item.get(fkey)) == fval]
            if len(matches) != 1:
                raise NewsletterError(f"Filtro [{flt}] encontrou {len(matches)} itens (esperado exatamente 1)")
            current = matches[0]
    return current


def extract(spec: dict[str, Any], raw: str) -> dict[str, Any]:
    values: dict[str, Any] = {}
    parsed = None
    if spec.get("fonte") == "json":
        parsed = json.loads(raw)
    for field in spec.get("campos", []):
        if spec.get("fonte") == "json":
            value = walk(parsed, field["caminho"])
        else:
            match = re.search(field["regex"], raw, re.S)
            if not match:
                raise NewsletterError(f"Campo '{field['id']}' não encontrado no HTML")
            value = match.group(1).strip()
        if value in (None, ""):
            raise NewsletterError(f"Campo '{field['id']}' veio vazio")
        values[field["id"]] = {"bruto": value, "rotulo": field.get("rotulo"), "formato": field.get("formato")}
    return values


def run_section(spec: dict[str, Any], attempts: int) -> dict[str, Any]:
    last_error = ""
    for attempt in range(1, attempts + 1):
        try:
            return {"ok": True, "tentativas": attempt, "url": spec["url"], "campos": extract(spec, fetch(spec))}
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, NewsletterError, KeyError, IndexError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt < attempts:
                time.sleep(3)
    return {"ok": False, "tentativas": attempts, "url": spec["url"], "erro": last_error}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--secao")
    parser.add_argument("--tentativas", type=int, help="sobrepõe 'tentativas' do config (máx. 2 recomendado)")
    args = parser.parse_args()
    try:
        config = load_config()
        specs = [section_by_id(config, args.secao)] if args.secao else [
            s for s in config.get("secoes", []) if s.get("tipo") == "dados-ao-vivo"
        ]
    except NewsletterError as exc:
        print(json.dumps({"erro": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    results = {spec["id"]: run_section(spec, args.tentativas or int(spec.get("tentativas", 2))) for spec in specs}
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if all(r["ok"] for r in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
