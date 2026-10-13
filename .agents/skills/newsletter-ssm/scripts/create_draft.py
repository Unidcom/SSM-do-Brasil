#!/usr/bin/env python3
"""Cria ou atualiza a campanha da edição EM RASCUNHO, direto pela API da plataforma.

Uso:
  python create_draft.py create <pasta-da-edicao> [--dry-run]
  python create_draft.py update <pasta-da-edicao> --campaign-id ID [--dry-run]

A plataforma vem de `plataforma.tipo` no config (`brevo`, `mailerlite-classic` ou `mailerlite`).
Credenciais: `private/<plataforma>.env` (ou o caminho em `plataforma.credenciais`);
variáveis de ambiente têm prioridade. Nenhum valor de credencial é impresso.

Este script NÃO envia, NÃO agenda e NÃO dispara testes — só rascunho.
Faz uma única tentativa. Grava `<plataforma>-response.json` na edição e se recusa
a criar uma segunda campanha para a mesma edição (use `update`).

Para adicionar outra plataforma: escrever uma classe com `create(payload)`,
`update(id, payload)` e `link(id)` no mesmo contrato e registrá-la em ADAPTERS.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib import parse, request
from urllib.error import HTTPError, URLError

from _newsletter_common import (
    Credentials,
    NewsletterError,
    approval_settings,
    load_config,
    load_env,
    read_json,
    resolve_edition,
    write_json,
)
from validate_edition import validate


def http(method: str, url: str, headers: dict[str, str], body: dict[str, Any] | None = None) -> tuple[int, Any]:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = request.Request(url, data=data, method=method, headers={
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "newsletter-skill/2.0",
        **headers,
    })
    try:
        with request.urlopen(req, timeout=60) as response:
            status, text = response.status, response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        raise NewsletterError(f"{method} {url} → HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')[:800]}") from exc
    except (URLError, TimeoutError) as exc:
        raise NewsletterError(f"Sem conexão com {url}: {exc}") from exc
    if not text.strip():
        return status, None
    try:
        return status, json.loads(text)
    except json.JSONDecodeError:
        return status, text


class Brevo:
    """API v3 — https://developers.brevo.com/reference/create-email-campaign"""

    base = "https://api.brevo.com/v3"

    def __init__(self, creds: Credentials, dry_run: bool) -> None:
        self.creds = creds
        self.dry_run = dry_run

    def _headers(self) -> dict[str, str]:
        return {"api-key": self.creds.require("BREVO_API_KEY")}

    def body(self, payload: dict[str, Any]) -> dict[str, Any]:
        sender_id = self.creds.get("BREVO_SENDER_ID")
        if sender_id:
            sender: dict[str, Any] = {"id": int(sender_id)}
        else:
            sender = {"name": self.creds.require("BREVO_SENDER_NAME"), "email": self.creds.require("BREVO_SENDER_EMAIL")}
        list_ids = [int(x) for x in self.creds.require("BREVO_LIST_IDS").replace(";", ",").split(",") if x.strip()]
        if not list_ids:
            raise NewsletterError("BREVO_LIST_IDS vazio.")
        body = {
            "name": payload["nome_campanha"],
            "subject": payload["assunto"],
            "sender": sender,
            "htmlContent": payload["html"],
            "recipients": {"listIds": list_ids},
            "mirrorActive": True,
            "inlineImageActivation": False,
        }
        if payload.get("pre_header"):
            body["previewText"] = payload["pre_header"]
        # Não enviar "tag": contas sem esse recurso respondem HTTP 405.
        return body

    def create(self, payload: dict[str, Any]) -> int:
        _, response = http("POST", f"{self.base}/emailCampaigns", self._headers(), self.body(payload))
        try:
            return int(response["id"])
        except (TypeError, KeyError, ValueError) as exc:
            raise NewsletterError("A Brevo respondeu sem o id da campanha.") from exc

    def update(self, campaign_id: int, payload: dict[str, Any]) -> None:
        _, campaign = http("GET", f"{self.base}/emailCampaigns/{campaign_id}", self._headers())
        status = (campaign or {}).get("status") if isinstance(campaign, dict) else None
        if status not in ("draft", None):
            raise NewsletterError(f"Campanha {campaign_id} está '{status}', não em rascunho — não pode ser alterada.")
        http("PUT", f"{self.base}/emailCampaigns/{campaign_id}", self._headers(), self.body(payload))

    def write_content(self, campaign_id: int, payload: dict[str, Any]) -> None:
        """Na Brevo o conteúdo vai junto da criação; nada a fazer."""

    @staticmethod
    def link(campaign_id: int) -> str:
        return f"https://app.brevo.com/marketing-campaign/edit/{campaign_id}"

    def preview(self, payload: dict[str, Any]) -> dict[str, Any]:
        body = self.body(payload)
        body["htmlContent"] = f"<{len(body['htmlContent'])} caracteres>"
        return {"POST": f"{self.base}/emailCampaigns", "corpo": body}


class MailerLiteClassic:
    """API v2 Classic — https://developers-classic.mailerlite.com/"""

    base = "https://api.mailerlite.com/api/v2"

    def __init__(self, creds: Credentials, dry_run: bool) -> None:
        self.creds = creds
        self.dry_run = dry_run

    def _headers(self) -> dict[str, str]:
        return {"X-MailerLite-ApiKey": self.creds.require("MAILERLITE_API_KEY")}

    def campaign(self, payload: dict[str, Any]) -> dict[str, Any]:
        group_id = self.creds.get("MAILERLITE_GROUP_ID")
        segment_id = self.creds.get("MAILERLITE_SEGMENT_ID")
        if bool(group_id) == bool(segment_id):
            raise NewsletterError("Configure exatamente um destino: MAILERLITE_GROUP_ID ou MAILERLITE_SEGMENT_ID.")
        body: dict[str, Any] = {"type": "regular", "name": payload["nome_campanha"], "subject": payload["assunto"],
                                ("groups" if group_id else "segments"): [int(group_id or segment_id)]}
        if sender := self.creds.get("MAILERLITE_FROM_EMAIL"):
            body["from"] = sender
        if sender_name := self.creds.get("MAILERLITE_FROM_NAME"):
            body["from_name"] = sender_name
        return body

    @staticmethod
    def content(payload: dict[str, Any]) -> dict[str, Any]:
        return {"html": payload["html"], "plain": payload["texto"], "auto_inline": False}

    def create(self, payload: dict[str, Any]) -> int:
        _, response = http("POST", f"{self.base}/campaigns", self._headers(), self.campaign(payload))
        candidates: list[Any] = []
        if isinstance(response, dict):
            candidates += [response.get("id"), response.get("campaign_id")]
            if isinstance(response.get("data"), dict):
                candidates += [response["data"].get("id"), response["data"].get("campaign_id")]
        for candidate in candidates:
            try:
                return int(candidate)
            except (TypeError, ValueError):
                continue
        raise NewsletterError("O MailerLite criou a campanha mas não devolveu o id.")

    def write_content(self, campaign_id: int, payload: dict[str, Any]) -> None:
        http("PUT", f"{self.base}/campaigns/{campaign_id}/content", self._headers(), self.content(payload))

    def update(self, campaign_id: int, payload: dict[str, Any]) -> None:
        offset = 0
        while True:
            query = parse.urlencode({"limit": 100, "offset": offset})
            _, response = http("GET", f"{self.base}/campaigns/draft?{query}", self._headers())
            items = response if isinstance(response, list) else (response or {}).get("data", [])
            if any(str(c.get("id")) == str(campaign_id) for c in items):
                break
            if len(items) < 100:
                raise NewsletterError(f"Rascunho {campaign_id} não encontrado no MailerLite.")
            offset += 100
        self.write_content(campaign_id, payload)

    @staticmethod
    def link(campaign_id: int) -> str:
        return f"https://app.mailerlite.com/emails/view/{campaign_id}"

    def preview(self, payload: dict[str, Any]) -> dict[str, Any]:
        content = self.content(payload)
        content["html"] = f"<{len(content['html'])} caracteres>"
        content["plain"] = f"<{len(content['plain'])} caracteres>"
        return {"POST": f"{self.base}/campaigns", "corpo": self.campaign(payload),
                "PUT": f"{self.base}/campaigns/<id>/content", "conteudo": content}


class MailerLite:
    """MailerLite atual (connect) — https://developers.mailerlite.com/docs/campaigns.html

    `emails[].content` (HTML próprio) só é aceito no plano Advanced. Plain text é gerado
    pela plataforma a partir do HTML; `payload["texto"]` não é enviado.
    """

    base = "https://connect.mailerlite.com/api"

    def __init__(self, creds: Credentials, dry_run: bool) -> None:
        self.creds = creds
        self.dry_run = dry_run

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.creds.require('MAILERLITE_API_TOKEN')}"}

    def body(self, payload: dict[str, Any]) -> dict[str, Any]:
        group_ids = [x.strip() for x in (self.creds.get("MAILERLITE_GROUP_IDS") or "").replace(";", ",").split(",") if x.strip()]
        segment_ids = [x.strip() for x in (self.creds.get("MAILERLITE_SEGMENT_IDS") or "").replace(";", ",").split(",") if x.strip()]
        if bool(group_ids) == bool(segment_ids):
            raise NewsletterError("Configure exatamente um destino: MAILERLITE_GROUP_IDS ou MAILERLITE_SEGMENT_IDS.")
        email = {
            "subject": payload["assunto"],
            "from_name": self.creds.require("MAILERLITE_FROM_NAME"),
            "from": self.creds.require("MAILERLITE_FROM_EMAIL"),
            "content": payload["html"],
        }
        body: dict[str, Any] = {"name": payload["nome_campanha"], "type": "regular", "emails": [email]}
        # Idioma das páginas do sistema (descadastro, versão web). Sem ele a conta usa o padrão (inglês).
        if language_id := self.creds.get("MAILERLITE_LANGUAGE_ID"):
            body["language_id"] = int(language_id)
        if group_ids:
            body["groups"] = group_ids
        else:
            body["segments"] = segment_ids
        return body

    @staticmethod
    def _data(response: Any) -> dict[str, Any]:
        if isinstance(response, dict) and isinstance(response.get("data"), dict):
            return response["data"]
        return response if isinstance(response, dict) else {}

    def create(self, payload: dict[str, Any]) -> int:
        _, response = http("POST", f"{self.base}/campaigns", self._headers(), self.body(payload))
        try:
            return int(self._data(response)["id"])
        except (KeyError, TypeError, ValueError) as exc:
            raise NewsletterError("O MailerLite respondeu sem o id da campanha.") from exc

    def update(self, campaign_id: int, payload: dict[str, Any]) -> None:
        _, response = http("GET", f"{self.base}/campaigns/{campaign_id}", self._headers())
        status = self._data(response).get("status")
        if status != "draft":
            raise NewsletterError(f"Campanha {campaign_id} está '{status}', não em rascunho — não pode ser alterada.")
        http("PUT", f"{self.base}/campaigns/{campaign_id}", self._headers(), self.body(payload))

    def write_content(self, campaign_id: int, payload: dict[str, Any]) -> None:
        """O HTML vai junto da criação (emails[].content); nada a fazer."""

    @staticmethod
    def link(campaign_id: int) -> str:
        return f"https://dashboard.mailerlite.com/campaigns/status/draft (id {campaign_id})"

    def preview(self, payload: dict[str, Any]) -> dict[str, Any]:
        body = self.body(payload)
        body["emails"][0]["content"] = f"<{len(payload['html'])} caracteres>"
        return {"POST": f"{self.base}/campaigns", "corpo": body}


ADAPTERS = {"brevo": Brevo, "mailerlite-classic": MailerLiteClassic, "mailerlite": MailerLite}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    create = sub.add_parser("create")
    create.add_argument("edicao")
    create.add_argument("--dry-run", action="store_true")
    update = sub.add_parser("update")
    update.add_argument("edicao")
    update.add_argument("--campaign-id", type=int, required=True)
    update.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        config = load_config()
        tipo = config.get("plataforma", {}).get("tipo")
        if tipo not in ADAPTERS:
            raise NewsletterError(f"Plataforma sem adaptador: {tipo!r}. Disponíveis: {', '.join(ADAPTERS)}.")
        edition = resolve_edition(args.edicao, config)
        errors, _ = validate(edition, config)
        if errors:
            raise NewsletterError("Edição inválida: " + "; ".join(errors))
        payload = read_json(edition / "payload.json")
        missing_approval = bool(approval_settings(config)) and not payload.get("link_aprovacao")

        adapter = ADAPTERS[tipo](load_env(config), args.dry_run)
        log_path = edition / f"{tipo}-response.json"
        previous = read_json(log_path, default={}) if log_path.exists() else {}

        if args.dry_run:
            # Dry-run não chama a API: pode rodar antes da aprovação, mas avisa.
            print(json.dumps({"ok": True, "dry_run": True, "plataforma": tipo, "acao": args.cmd,
                              "aviso": "link_aprovacao vazio — create real será recusado" if missing_approval else None,
                              "requisicao": adapter.preview(payload)}, ensure_ascii=False, indent=2))
            return 0
        if missing_approval:
            raise NewsletterError("Edição ainda não publicada para aprovação (link_aprovacao vazio). "
                                  "Rode publish_approval.py antes de criar o rascunho.")

        if args.cmd == "create":
            if previous.get("campaign_id"):
                raise NewsletterError(f"Esta edição já tem a campanha {previous['campaign_id']} "
                                      f"({previous.get('link')}). Use 'update --campaign-id {previous['campaign_id']}'.")
            campaign_id = adapter.create(payload)
            result = {"plataforma": tipo, "campaign_id": campaign_id, "link": adapter.link(campaign_id),
                      "nome": payload["nome_campanha"], "conteudo": "pendente"}
            # Grava o id antes do conteúdo: se o passo seguinte falhar, a retomada usa update.
            write_json(log_path, result)
            adapter.write_content(campaign_id, payload)
        else:
            adapter.update(args.campaign_id, payload)
            result = {"plataforma": tipo, "campaign_id": args.campaign_id, "link": adapter.link(args.campaign_id),
                      "nome": payload["nome_campanha"]}
        result["conteudo"] = "gravado"
        result["status"] = "rascunho — disparo aos contatos é manual no painel"
        write_json(log_path, result)
        print(json.dumps({"ok": True, **result, "log": str(log_path)}, ensure_ascii=False, indent=2))
        return 0
    except NewsletterError as exc:
        print(json.dumps({"ok": False, "erro": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
