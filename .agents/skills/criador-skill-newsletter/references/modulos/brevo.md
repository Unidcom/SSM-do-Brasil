# Brevo (API v3) — %%NOME%%

`scripts/create_draft.py` cria ou atualiza a campanha **em rascunho** direto na API da Brevo. Não há n8n no caminho e o script não tem operação de envio, agendamento nem teste.

## Credenciais — `%%CREDENCIAIS%%`

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
