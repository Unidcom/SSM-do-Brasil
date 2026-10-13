# MailerLite Classic (API v2) — %%NOME%%

`scripts/create_draft.py` cria ou atualiza a campanha **em rascunho** direto na API Classic (`https://api.mailerlite.com/api/v2`). O script não tem operação de envio, agendamento nem teste.

## Credenciais — `%%CREDENCIAIS%%`

```dotenv
MAILERLITE_API_KEY=
# destino: exatamente UM dos dois
MAILERLITE_SEGMENT_ID=
MAILERLITE_GROUP_ID=
MAILERLITE_FROM_EMAIL=
MAILERLITE_FROM_NAME=
```

O arquivo fica fora do Git (`private/` no `.gitignore`). Variáveis de ambiente com o mesmo nome têm prioridade.

## O que o script faz

| Comando | Chamadas | Resultado |
|---|---|---|
| `create <edição>` | `POST /campaigns` → `PUT /campaigns/{id}/content` (HTML + plain text) | grava `mailerlite-classic-response.json` |
| `update <edição> --campaign-id ID` | confere que o ID está em `GET /campaigns/draft` → `PUT /campaigns/{id}/content` | conteúdo substituído |
| `--dry-run` | nenhuma | mostra os corpos que seriam enviados |

- O `campaign_id` é gravado **antes** do conteúdo. Se o `PUT` falhar, a retomada é `update`, nunca outro `create`.
- Link do rascunho no painel: `https://app.mailerlite.com/emails/view/{id}` (link autenticado, não é URL pública).
- `campaign_id` = confirmação usada no `rotation.py mark-used`.

## Variáveis de sistema

- HTML e texto: `{$url}` (ver no navegador) e `{$unsubscribe}` (descadastro) — obrigatórias e literais.
- **Nunca** usar tags de nome (`{$name}`, `{$name|default:...}`): quebram no MailerLite Classic. Saudação com texto fixo (ex.: "amigo(a)").
