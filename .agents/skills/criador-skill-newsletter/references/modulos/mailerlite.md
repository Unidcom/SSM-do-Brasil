# MailerLite (API atual, connect) — %%NOME%%

`scripts/create_draft.py` cria ou atualiza a campanha **em rascunho** direto na API atual do MailerLite (`https://connect.mailerlite.com/api`). O script não tem operação de envio, agendamento nem teste.

> **Plano:** HTML próprio via API (`emails[].content`) só é aceito no plano **Advanced**. Em plano inferior a criação falha (HTTP 422) — não contornar colando o HTML à mão sem avisar o usuário.

## Credenciais — `%%CREDENCIAIS%%`

```dotenv
MAILERLITE_API_TOKEN=
# destino: exatamente UM dos dois (IDs separados por vírgula)
MAILERLITE_GROUP_IDS=
MAILERLITE_SEGMENT_IDS=
# remetente verificado no MailerLite
MAILERLITE_FROM_EMAIL=
MAILERLITE_FROM_NAME=
# idioma das páginas de descadastro/versão web (19 = Português do Brasil; sem ele, inglês)
MAILERLITE_LANGUAGE_ID=19
```

Token: painel → Integrations → MailerLite API → Generate new token. O arquivo fica fora do Git (`private/` no `.gitignore`). Variáveis de ambiente com o mesmo nome têm prioridade.

## O que o script faz

| Comando | Chamadas | Resultado |
|---|---|---|
| `create <edição>` | `POST /campaigns` (nome, assunto, remetente, HTML, grupos/segmentos) | grava `mailerlite-response.json` com `campaign_id` (`data.id`) |
| `update <edição> --campaign-id ID` | `GET /campaigns/{id}` (exige `status: draft`) → `PUT /campaigns/{id}` | conteúdo substituído |
| `--dry-run` | nenhuma | mostra o corpo que seria enviado |

- Uma única tentativa; nunca repetir `create` para a mesma edição — usar `update`.
- Plain text é gerado pelo MailerLite a partir do HTML (o `texto` da edição serve só de conferência).
- Rascunhos ficam em `https://dashboard.mailerlite.com/campaigns/status/draft` (painel autenticado).
- `campaign_id` = confirmação usada no `rotation.py mark-used`.

## Variáveis e rodapé

- HTML: `{$unsubscribe}` (descadastro, obrigatório) e `{$url}` (ver no navegador) — literais.
- O rodapé precisa ter **link de descadastro, nome da conta, endereço e país**; sem isso o MailerLite acrescenta o rodapé padrão dele.
- Não usar tags de nome (`{$name}`): saudação com texto fixo.

## Documentação

- Campanhas: https://developers.mailerlite.com/docs/campaigns.html
- Autenticação: https://developers.mailerlite.com/docs/#authentication
