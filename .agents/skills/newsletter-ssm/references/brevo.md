# Brevo (API v3) — Radar Estrutural SSM

`scripts/create_draft.py` cria ou atualiza a campanha **em rascunho** direto na API da Brevo. Não há n8n no caminho e o script não tem operação de envio, agendamento nem teste.

## Credenciais — `private/brevo.env`

```dotenv
BREVO_API_KEY=
# remetente verificado: o ID OU nome + e-mail
BREVO_SENDER_ID=
BREVO_SENDER_NAME=
BREVO_SENDER_EMAIL=
# listas de destino, separadas por vírgula
BREVO_LIST_IDS=
```

O arquivo fica fora do Git (`private/` no `.gitignore`). Variáveis de ambiente com o mesmo nome têm prioridade. Para descobrir IDs: painel da Brevo → Remetentes e Contatos → Listas (ou `GET /v3/senders` e `GET /v3/contacts/lists`).

### Preenchido para esta conta (2026-10-13)

- **Conta:** SSM do Brasil (`ssm.unidcom@gmail.com`) — chave em `private/brevo-ssm.env` e já copiada para `private/brevo.env`.
- **Whitelist de IP ativa:** a conta exige IPs autorizados em https://app.brevo.com/security/authorised_ips — sem isso a API responde `unauthorized` ("unrecognised IP address").
- **Remetentes verificados (ativos):** `[1] SSM do Brasil <marketing@ssmdobrasil.com.br>` · `[2] SSM do Brasil <gestaocomercial@ssmdobrasil.com.br>` — a newsletter usa o **1**.
- **Listas existentes:** `[21] CLIENTES INTERSOLAR (1.092)` · `[5] DIA 1 | 2º Lista de Clientes (275)` · `[4] DIA 2 | 1º Lista de Clientes (297)` · `[22] Pesquisa de satisfação 2026 (115)` · `[15]/[14] Equipes SSM` · `[12] Campanhas de Captação de Leads (0)`. O `.env` usa **21** por padrão — ajustar `BREVO_LIST_IDS` quando a base da newsletter for definida.
- Acesso programático sem MCP: a conta **não usa servidor MCP** — todas as operações vão pela API v3 direto (`https://api.brevo.com/v3`, header `api-key`). Scripts desta skill já encapsulam o que o fluxo precisa (`create_draft.py`); para consultas pontuais, `curl -H "api-key: $KEY" https://api.brevo.com/v3/...`.

## O que o script faz

| Comando | Chamada | Resultado |
|---|---|---|
| `create <edição>` | `POST /v3/emailCampaigns` | HTTP 201 com `id` → grava `brevo-response.json` |
| `update <edição> --campaign-id ID` | `GET /v3/emailCampaigns/{id}` (confere `status: draft`) → `PUT /v3/emailCampaigns/{id}` | conteúdo substituído |
| `--dry-run` | nenhuma | mostra o corpo que seria enviado (HTML resumido, sem a chave) |

Corpo enviado (montado a partir do `payload.json` + `.env`):

```json
{"name": "<nome_campanha>", "subject": "<assunto>", "previewText": "<pre_header>",
 "sender": {"id": 1}, "htmlContent": "<html>", "recipients": {"listIds": [2]},
 "mirrorActive": true, "inlineImageActivation": false}
```

- Não enviar `tag`: contas sem esse recurso respondem HTTP 405.
- Link do rascunho no painel: `https://app.brevo.com/marketing-campaign/edit/{id}`.
- `campaign_id` = confirmação usada no `rotation.py mark-used`.

## Variáveis de sistema

```html
<a href="{{ mirror }}">Ver no navegador</a>
<a href="{{ unsubscribe }}">Cancelar inscrição</a>
```

Ficam literalmente no HTML; a Brevo as substitui no processamento. `mirrorActive: true` ativa o espelho. Sem `unsubscriptionPageId`, vale a página padrão de descadastro. Como o HTML já tem os dois links, não adicionar cabeçalho/rodapé padrão com a mesma função. No preview e na cópia de aprovação esses links não funcionam — é esperado.

## Referências oficiais

- Criar campanha: https://developers.brevo.com/reference/create-email-campaign
- Atualizar campanha: https://developers.brevo.com/reference/update-email-campaign
- Consultar campanha: https://developers.brevo.com/reference/get-email-campaign
- Link espelho: https://help.brevo.com/hc/pt/articles/5316043391122
