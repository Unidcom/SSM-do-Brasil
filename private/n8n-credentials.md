# Credenciais n8n — Unidcom

> Duplicado de `tempo-funeral/private/n8n-credentials.md` para uso neste projeto (automação Kommo → Lusha → Kommo).

⚠️ **ARQUIVO SENSÍVEL — NÃO COMPARTILHAR, NÃO SUBIR PARA REPOSITÓRIO PÚBLICO.**
Se este token vazar, qualquer pessoa consegue ler/editar/executar TODOS os workflows deste n8n (inclusive credenciais de terceiros — Kommo, Piperun, Google Sheets, MailerLite etc. — referenciadas neles). Se suspeitar de vazamento, revogue e gere um novo em Settings > n8n API.

- **URL da instância**: https://n8n.unidcom.com.br
- **API Key (n8n)**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiZmE4OTUxOC00M2M0LTQyOGQtYmZlYy03NGQ0M2E4Nzk0YTgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiMWU1NDQ2NTEtOTk1NC00NGE5LThmYTgtN2MzNWQwMWVjN2JkIiwiaWF0IjoxNzg2MTExMDAwfQ.zyaZc66vroHwwgd_5rafGfO6UiNn4X285iAvEvKUVio
```

Essa chave é da instância n8n inteira da Unidcom (não é de um workflow específico) — serve pra qualquer workflow que essa conta tenha acesso.

## Uso

Header de autenticação: `X-N8N-API-KEY: <token acima>`

Endpoints úteis:
- `GET  /api/v1/workflows/{id}` — ler workflow (nodes, connections, settings completos)
- `PUT  /api/v1/workflows/{id}` — atualizar workflow. Precisa enviar **só** `name`, `nodes`, `connections`, `settings` no body — qualquer outro campo do GET (ex: `active`, `tags`, `id`) causa erro 400. E `settings` só aceita um subconjunto de chaves conhecidas pela API pública (mesmo que o GET retorne mais campos que o editor web usa internamente):
  ```
  executionOrder, timezone, saveDataErrorExecution, saveDataSuccessExecution,
  saveExecutionProgress, saveManualExecutions, errorWorkflow, executionTimeout
  ```
  Filtre para só essas chaves antes do PUT, senão dá `"settings must NOT have additional properties"`.
- `GET  /api/v1/executions/{id}?includeData=true` — ler uma execução específica com o payload completo de cada node (inclusive o erro exato de quem falhou)
- `GET  /api/v1/executions?workflowId={id}&status=error` — listar execuções com erro de um workflow
- `POST /api/v1/executions/{id}/retry` — **CUIDADO**: só reexecuta a partir do node que falhou, reaproveitando a saída antiga dos nodes anteriores. Não serve pra reprocessar do zero.
- Pra reprocessar de verdade: extrair o `body` original do node de trigger (webhook) da execução via `GET /api/v1/executions/{id}?includeData=true` e reenviar via POST direto pra URL do webhook (`https://n8n.unidcom.com.br/webhook/<path>`). Isso dispara uma execução nova do zero.

## Política de alterações estruturais

Antes de qualquer alteração estrutural num workflow (adicionar/remover node, mudar lógica), salvar backup local com `GET /api/v1/workflows/{id}` antes de aplicar o `PUT` — fora de qualquer pasta de cliente, só pra rollback se precisar.

## Dicas técnicas (ambiente Windows / Git Bash)

- **SSL**: `curl` no Git Bash desse ambiente dá `SSL certificate problem: unable to get local issuer certificate` pro domínio `n8n.unidcom.com.br` (falta uma CA intermediária no bundle local). Usar `curl -k` (só pra esse host interno conhecido).
- **Escaping**: montar JSON grande (workflow completo) direto em linha de comando quebra fácil com aspas/parênteses/acentos. Prefira escrever um script `.js` (Node) em arquivo com a tool de escrita de arquivos e rodar com `node script.js arg1 arg2` — bem mais confiável do que heredoc/`node -e` inline.
- **Node + paths com barra Unix**: `fs.readFileSync(path)` aceita path estilo `/c/Users/...` (Git Bash) numa boa, mas `require(path)` para carregar JSON não — dá `MODULE_NOT_FOUND`. Sempre usar `fs.readFileSync` + `JSON.parse`, nunca `require()` pra ler os JSONs de workflow.
- **Caracteres de controle em JSON Body do node HTTP Request**: se um valor interpolado via `{{ }}` pode conter TAB/quebra de linha/aspas (ex: nome de campanha colado de outro sistema), nunca interpole direto dentro de uma string JSON escrita à mão — quebra o parse ("Bad control character..."). Usar `{{ JSON.stringify(valor).slice(1, -1) }}` dentro das aspas já existentes do template, ou construir o body inteiro num node de Code com `JSON.stringify()`.

## Workflows já mapeados (referência)

- `5qG2N2JikqaAmyYr` — `[UNIDCOM] Relatório diário - Enriquecimento de leads por campanha` (criado 06/10/2026). Todo dia 08h (America/Sao_Paulo): lê no Kommo os eventos `entity_tag_added` do dia anterior com tag `Perfil-*` (= leads que passaram pela skill perfil-lead via DAG `comercial-unidcom-leads-cursor`), agrupa por `utm_campaign` (field 922548), manda no Discord `#leads-aquisição-unid` + DM do Luiz (`luizmauricio`) e grava uma linha por campanha na planilha "Enriquecimento de Leads por Campanha" (`1r8b4mS9vHA7FfXJ7QwBxGuPXw4T8WCV0ziqysVUr4LQ`, aba `Diario`). Erros caem no `ERRO WORKFLOW` (#erro-leads). Conta **toda** tag `Perfil-*` do dia, inclusive aplicada à mão no Kommo ou por rodada manual da skill (decisão do Pedro em 06/10/2026 — ex.: 02/10 deu 251 porque o Luiz tagueou 117 em massa). Planilha preenchida retroativamente de 01/09 a 05/10/2026. Reprocessar um dia: `GET https://n8n.unidcom.com.br/webhook/relatorio-enriquecimento-d9e07cc7ae3b370c?data=AAAA-MM-DD` (+ `&sem_discord=1` pra só gravar na planilha) — **reprocessar um dia já gravado duplica as linhas dele na planilha**. Gerador do workflow e backup em `.private/n8n-backups/5qG2N2JikqaAmyYr/` (`node gerar-workflow.js update 5qG2N2JikqaAmyYr` reaplica). Atenção: o Kommo responde `application/hal+json` — os nodes HTTP precisam de `responseFormat: json`, senão o n8n trata como texto e a paginação para na 1ª página.
- `k7kvRn1AsT5yOXB8` — `[UNIDCOM] SNOV + RESEND → Kommo + MailerLite` (automação interna de leads Unidcom, Snov.io + Resend → Kommo + MailerLite)
- `3bs4AFTHkemi2u3Q` — `Resend -> Google Sheets -> Piperun` (cliente SP< Uniformes, ver `docs/automacoes/automacao-resend-n8n/n8n-credentials.md` no repo `sp-uniformes` pra detalhes específicos desse workflow)
- `RaVWyH9rzZfsKRtd` — `[TEMPO FUNERAL] Webhook -> Excecoes do Bot` (ver `tempo-funeral/private/n8n-credentials.md` e `tempo-funeral/private/kommo-tempo-credentials.md`)
