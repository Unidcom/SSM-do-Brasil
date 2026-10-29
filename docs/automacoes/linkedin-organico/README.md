# LinkedIn orgânico (SSM) → n8n

Coleta diária de métricas da Página da SSM do Brasil no LinkedIn, por data e por publicação, gravadas em BigQuery (ou Google Sheets).

Plano completo e fatos da API: ver "Plano: LinkedIn orgânico" (aprovado em 22/10/2026). Versão da API usada: `Linkedin-Version: 202610`.

> Segredos (Client ID/Secret, tokens, API key do n8n) ficam **só** em `private/` (ignorado pelo git). Nada disso entra neste arquivo.

## Métricas

| Métrica | Origem |
|---|---|
| Impressões, cliques, curtidas, comentários, compartilhamentos | `organizationalEntityShareStatistics` (`impressionCount`, `clickCount`, `likeCount`, `commentCount`, `shareCount`) |
| Engajamentos | soma de cliques + curtidas + comentários + compartilhamentos |
| Taxa de engajamento | campo `engagement` da API (conferir com engajamentos ÷ impressões) |
| Seguidores (novos) | `organizationalEntityFollowerStatistics` com `timeIntervals` (DAY). Defasagem de 2 dias |
| Seguidores (total) | `networkSizes/urn:li:organization:{id}?edgeType=COMPANY_FOLLOWED_BY_MEMBER` (`firstDegreeSize`), snapshot diário |

**Por data:** série diária da Página (janela de 12 meses).
**Por publicação:** a API só entrega o acumulado de cada post. O workflow grava um snapshot diário e a variação do dia é a diferença entre snapshots. O histórico por post começa no dia em que o workflow entrar no ar.

## Checklist: criar o app no LinkedIn (manual)

- [ ] Um administrador da **Página da Unidcom** está disponível para verificar o app.
- [ ] Em developer.linkedin.com, criar um **app novo** (sem outros produtos) associado à Página da Unidcom.
- [ ] Verificar o app pela Página (o admin da Página aprova o link de verificação).
- [ ] Em *Products*, pedir **Community Management API** (Development tier). Usar e-mail corporativo e o site/domínio da Unidcom. Descrever o caso de uso: relatórios de desempenho orgânico da Página de um cliente (SSM do Brasil), somente leitura.
- [ ] Em *Auth*, cadastrar o redirect URI: `https://n8n.unidcom.com.br/rest/oauth2-credential/callback`.
- [ ] Guardar Client ID e Client Secret em `private/` (por exemplo `private/linkedin-app.env`).
- [ ] Identificar o **ADMINISTRATOR** da Página da SSM, que vai autorizar o OAuth.
- [ ] Obter o ID da organização da SSM (`urn:li:organization:...`).

Se o LinkedIn rejeitar, não dá para reaplicar com o mesmo app: criar outro. Plano B: app criado e verificado pela Página da SSM.

## Credencial OAuth2 no n8n

- Tipo: *OAuth2 API* (genérico).
- Authorization URL: `https://www.linkedin.com/oauth/v2/authorization`
- Access Token URL: `https://www.linkedin.com/oauth/v2/accessToken`
- Escopos: `rw_organization_admin r_organization_social`
- Client credentials enviados no corpo (*Body*).
- Autorizar com a conta ADMINISTRATOR da SSM e conferir se o n8n recebe um `refresh_token`. O access token dura 60 dias; sem refresh token, é preciso reautorizar a cada ciclo.

## Destino dos dados

- **BigQuery** se a Unidcom tiver projeto GCP com faturamento ativado (o volume cabe no free tier). O sandbox sem faturamento expira tabelas em 60 dias e não serve para histórico.
- **Google Sheets** caso contrário, com as mesmas colunas.

Tabelas: `linkedin_diario`, `linkedin_posts`, `linkedin_post_snapshot` (e a visão `linkedin_post_diario`). Esquema no plano.

## Próximos passos

1. Concluir o checklist acima e passar o ID da organização e o destino.
2. Teste de fumaça das chamadas (campos de seguidores, lote de posts, tipo de URN).
3. Gerador de workflows (`gerar-workflow.js`) para WF1 ingestão diária, WF2 backfill e WF3 alerta de token, criados **inativos** no n8n.
