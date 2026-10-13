---
name: newsletter-ssm
description: Gera a Radar Estrutural SSM da SSM do Brasil (toda quarta às 09:00): Radar do setor (curadoria de notícias); Solução em destaque (rotação em ordem); Do blog da SSM (sem repetição recente). Monta HTML e plain text, publica para aprovação em aprovacoes-unid e cria o rascunho na Brevo pela API (sem disparar). Use quando o usuário pedir para montar, gerar, preparar ou enviar a newsletter da SSM do Brasil, pedir a edição do dia/da semana ou mencionar '$newsletter-ssm'.
---

# Radar Estrutural SSM

Newsletter semanal da **SSM do Brasil** (toda quarta, 09:00), indústria brasileira de estruturas em aço e alumínio para energia solar. O propósito é construir autoridade técnica de engenharia e manter a marca no ciclo de recompra de uma base única de **integradores, EPCistas e distribuidores**: o leitor sai de cada edição sabendo o que mudou no setor, o que isso significa para a obra dele e com uma solução ou conteúdo técnico da SSM à mão. A conversão esperada é pedido de orçamento (CTA fixo) e leitura do blog — nunca venda direta no corpo do e-mail. Tom: técnico, direto, de quem entende de campo. Briefing completo e decisões do cliente: `docs/briefing-newsletter-ssm.md`.

**Agendamento de referência:** toda quarta às 09:00 (`America/Sao_Paulo`). O agendamento em si é configurado à parte (skill `schedule`); esta skill não se agenda sozinha.

## Regras operacionais

- **Skill incompleta:** antes de qualquer passo, buscar o marcador de pendência do criador (a palavra `TODO` seguida de `(criador)`, sem espaço) nos arquivos desta skill. Se houver algum, **não gerar a edição**: avisar o usuário que a skill ainda não terminou de ser criada, listar o que falta e oferecer completar agora pela skill `criador-skill-newsletter`.
- **Isolamento:** ao executar esta newsletter, usar somente esta skill. Não acionar skills auxiliares (copywriting, Git, navegador etc.); tudo que a execução precisa está aqui. Ferramentas podem ser usadas diretamente.
- **Data real:** confirmar a data da execução no fuso `America/Sao_Paulo`. Nunca presumir pela data do agendamento.
- **Nada inventado:** não inventar dados, números, resultados, prazos ou condições comerciais. Dados de catálogo e valores ao vivo são usados exatamente como vieram.
- **Reescrita, não tradução:** todo conteúdo externo é reescrito em português brasileiro, com contexto para o público da marca.
- **Contagens exatas:** cada seção entrega exatamente a quantidade declarada. Se faltar material, parar e avisar — nunca completar com conteúdo fora das regras.
- **Aprovação antes da plataforma:** a edição é publicada em `aprovacoes-unid` antes de qualquer chamada à Brevo. Sem link de aprovação, não há rascunho.
- **Só rascunho:** esta skill cria a campanha em rascunho e nunca envia, agenda ou dispara teste. O disparo aos contatos é manual, no painel. `Status: enviado` só quando o usuário confirmar o disparo.
- **Selecionar ≠ usar:** a rotação só avança com `rotation.py mark-used`, depois que o rascunho existir (`campaign_id`). Gerar a edição ou publicar para aprovação não avança nada.
- **Uma tentativa externa por execução:** nunca repetir automaticamente chamadas à API. Se a campanha já foi criada e um passo seguinte falhou, retomar só o passo que falhou (`update`) — nunca criar uma segunda campanha.
- **Artefatos no projeto:** toda edição salva `newsletter.html`, `plain-text.txt`, `payload.json` e `metadata.md` em `newsletter/AAAA-MM-DD/`. Nada fica só em memória ou em pasta temporária.
- **Variáveis da plataforma:** `{{ mirror }}`, `{{ unsubscribe }}` ficam literalmente no HTML; não são placeholders editoriais.
- **Segredos:** credenciais só em `private/brevo.env` (fora do Git) ou variáveis de ambiente — nunca em config, payload, metadata, logs ou commits.

## Seções da newsletter

A ordem abaixo é a ordem no e-mail. A especificação completa de cada seção está em `config/newsletter.json` — se uma seção mudar, atualizar o config, o template e o passo correspondente.

| # | Seção | Tipo | Como puxa | Slot | Estado avança |
|---:|---|---|---|---|---|
| 1 | Assunto, data e introdução (`abertura`) | texto da edição (`editorial`) | escrito a cada edição a partir do conteúdo selecionado | `{{INTRO}}` | — |
| 2 | Radar do setor (`radar-setor`) | curadoria de notícias (`curadoria-externa`) | busca em 6 fontes obrigatórias, últimos 7 dias → 3 destaques + 5 curtas | `{{HIGHLIGHT_1}}`, `{{HIGHLIGHT_2}}`, `{{HIGHLIGHT_3}}`, `{{QUICK_1}}`, `{{QUICK_2}}`, `{{QUICK_3}}`, `{{QUICK_4}}`, `{{QUICK_5}}` | — |
| 3 | Solução em destaque (`solucao-destaque`) | rotação em ordem (`rotacao-catalogo`) | próximo item de `assets/solucoes/catalog.json`, ordem circular | `{{SOLUCAO_BLOCK}}` | `mark-used` após o `campaign_id` do rascunho |
| 4 | Do blog da SSM (`blog-ssm`) | sem repetição recente (`pool-sem-repeticao`) | item de `assets/blog/catalog.json` fora dos últimos 10 usados | `{{BLOG_BLOCK}}` | `mark-used` após o `campaign_id` do rascunho |
| 5 | SSM em números (`numeros`) | bloco fixo (`bloco-fixo`) | fixo: Desde 2010, Até 30 anos de garantia, ISO 9001 e CE | — | — |
| 6 | CTA orçamento (`cta-orcamento`) | bloco fixo (`bloco-fixo`) | fixo (no template): botão com ícone WhatsApp → wa.me/554198418202 | — | — |

## Fluxo

### Passo 0 — Confirmar data e pasta da edição

1. Confirmar a data real da execução no fuso `America/Sao_Paulo` (ex.: `Get-Date` / `date`). Nunca presumir a data pelo agendamento nem reaproveitar a de outra edição.
2. Formato por extenso para o e-mail: `Quarta-feira, 5 de agosto de 2026`.
3. Pasta da edição: `newsletter/AAAA-MM-DD/`. Se já existir, preservar e criar `newsletter/AAAA-MM-DD-2/` (sufixo incremental). Edições de teste usam o sufixo `-teste` e nunca são publicadas.

### Passo 1 — Selecionar as seções com rotação

```powershell
python .agents/skills/newsletter-ssm/scripts/rotation.py select --date AAAA-MM-DD
```

O script lê `config/newsletter.json` e o estado em `newsletter/.rotation-state.json` e devolve, para cada seção com seleção automática, o item escolhido, o motivo, o modelo HTML e se a imagem está pronta para envio.

- **Selecionar não grava nada.** O estado só avança no passo de confirmação, depois do retorno da plataforma.
- Se alguma seção vier com `erro` (catálogo vazio, nenhum item ativo), parar e avisar.
- Registrar a seleção (seção → item, motivo) em `metadata.md`.

### Passo 2 — Preencher o conteúdo de cada seção

Na ordem em que aparecem no e-mail:

#### Radar do setor / Giro rápido (`radar-setor`)

Tipo `curadoria-externa` — notícias de fontes externas. Regras editoriais completas em `references/curadoria-editorial.md`.

- **Janela:** últimos 7 dias (máximo 10 se faltar material, registrando a exceção).
- **Fontes obrigatórias:**
  - Canal Solar: https://canalsolar.com.br/
  - Fotovolt / Aranda: https://www.arandanet.com.br/revista/fotovolt/noticias
  - Giro ABSOLAR: https://www.absolar.org.br/posts/?category_name=giro-absolar
  - Energy Channel: https://www.energychannel.co/
  - Folha — energia solar: https://www1.folha.uol.com.br/folha-topicos/energia-solar/
  - Exame — energia solar: https://exame.com/noticias-sobre/energia-solar/
- **Fontes complementares:**
  - ANEEL: https://www.gov.br/aneel/
  - EPE: https://www.epe.gov.br/pt/imprensa/noticias
  - ONS: https://www.ons.org.br/
  - pv magazine Brasil: https://www.pv-magazine-brasil.com/
  - pv magazine Global: https://www.pv-magazine.com/
  - IEA — Solar PV: https://www.iea.org/news?energySystem%5B0%5D=solar-pv
  - IRENA: https://www.irena.org/News
  - MME: https://www.gov.br/mme/
  - Câmara dos Deputados: https://www.camara.leg.br/noticias
- **Evitar:** especulação apresentada como fato; promessas absolutas de economia; política partidária sem relação operacional; menção espontânea a recuperação judicial de qualquer empresa; falências e demissões sem relação operacional.

| Bloco | Quantidade | Slots | Campos |
|---|---:|---|---|
| destaques (parcial `assets/partials/highlight.html`) | 3 (exato) | `{{HIGHLIGHT_1}}`, `{{HIGHLIGHT_2}}`, `{{HIGHLIGHT_3}}` | `tag`: tema estratégico (ex.: regulação, estruturas, mercado); `titulo`: gancho específico, sem clickbait; `contexto`: 80–130 palavras; `impacto`: 45–80 palavras, rótulo 'O que isso significa para sua obra:'; `url`: fonte |
| curtas (parcial `assets/partials/quick-item.html`) | 5 (exato) | `{{QUICK_1}}`, `{{QUICK_2}}`, `{{QUICK_3}}`, `{{QUICK_4}}`, `{{QUICK_5}}` | `titulo`: uma linha; `url`: fonte |

1. Calcular a janela a partir da data da edição e aceitar somente notícias publicadas dentro dela. Confirmar a data na página original, não no resultado de busca.
2. Verificar **todas** as fontes obrigatórias. Usar as complementares para completar ou para confirmar alegações regulatórias/financeiras em fonte primária.
3. Se faltar material, ampliar até o limite máximo da janela e registrar a exceção em `metadata.md`. Se ainda faltar, **parar** e avisar — nunca entregar menos itens que o exigido nem completar com notícia fora da janela.
4. Uma notícia não aparece em dois blocos da mesma edição.
5. Reescrever tudo em português brasileiro, com contexto local; nunca traduzir literalmente. Distinguir fato, estimativa e opinião. Não inventar números.
6. Preencher cada bloco com o parcial indicado e respeitar as contagens de palavras.

#### Solução em destaque (`solucao-destaque`)

Tipo `rotacao-catalogo` — um item por edição, em ordem circular, do catálogo `assets/solucoes/catalog.json`.

1. Usar o item que `rotation.py select` retornou para `solucao-destaque`. Não escolher outro por conta própria.
2. Partir do modelo HTML do item (`modelo_path`). Não alterar números, segmento ou resultados do item — eles vêm do catálogo.
3. Preview local pode usar `imagem_local`; o HTML de envio exige `imagem_publica` HTTPS (`pronto_para_envio: true`). Sem URL pública, parar antes do envio.
4. Inserir em `{{SOLUCAO_BLOCK}}`. Não avançar o estado aqui — só no passo de confirmação.

#### Do blog da SSM (`blog-ssm`)

Tipo `pool-sem-repeticao` — qualquer item do catálogo `assets/blog/catalog.json` que não esteja entre os últimos 10 usados.

1. **Atualizar o catálogo antes de selecionar:** buscar os posts mais recentes no blog da SSM pela API do WordPress e acrescentar ao catálogo os que ainda não estão nele (não apagar itens existentes; post antigo continua elegível para rotação). Endpoint: `https://ssmdobrasil.com.br/wp-json/wp/v2/posts?per_page=12&_fields=id,date,link,title,excerpt,featured_media` — e, para cada post novo, resolver a imagem em `https://ssmdobrasil.com.br/wp-json/wp/v2/media/<featured_media>?_fields=source_url`. Preencher `id` (slug curto do post), `titulo` (título do post), `texto` (1–2 frases do resumo, reescritas), `cta_url` (link do post) e `imagem_publica` (URL HTTPS da imagem destacada). Se a API falhar, usar o catálogo como está — nunca inventar post.
2. Usar o item que `rotation.py select` retornou para `blog-ssm`.
3. Montar o bloco a partir do modelo do item ou do parcial padrão e inserir em `{{BLOG_BLOCK}}`.
4. Não avançar o estado aqui — só no passo de confirmação.

#### SSM em números (`numeros`)

Tipo `bloco-fixo` — não muda entre edições.

Valores aprovados (exibir exatamente):
- `fundacao`: **Desde 2010**
- `garantia`: **Até 30 anos de garantia**
- `certificacoes`: **ISO 9001 e CE**

1. Manter texto, valores e links exatamente como estão no template/modelo. Alterar somente com nova aprovação do usuário, atualizando também `config/newsletter.json`.

#### CTA orçamento (`cta-orcamento`)

Tipo `bloco-fixo` — não muda entre edições.

Conteúdo definido no próprio `assets/template.html`.

1. Manter texto, valores e links exatamente como estão no template/modelo. Alterar somente com nova aprovação do usuário, atualizando também `config/newsletter.json`.

### Passo 3 — Assunto e textos de abertura

Escrever por último, quando o conteúdo já está definido:

- **Assunto:** até 70 caracteres, sustentado pela notícia/conteúdo principal da edição. Uma única emoção dominante (curiosidade, urgência, contraste, dado surpreendente). Específico — com número, plataforma, regra ou consequência concreta quando houver. O corpo precisa entregar exatamente o que o assunto promete; nada de clickbait vazio nem fórmulas gastas ("você não vai acreditar").
- **Pré-header** (`{{PREHEADER}}`): complementa o assunto, sem repeti-lo, até ~90 caracteres.
- **Data** (`{{EDITION_DATE}}`): por extenso, do passo de data.
- Antes de fechar o assunto, conferir: chama atenção em dois segundos? A edição sustenta a promessa? Está no tom da marca?

#### Assunto, data e introdução (`abertura`)

Tipo `editorial` — escrito a cada edição a partir do conteúdo já selecionado.

- `assunto`: até 70 caracteres, sustentado pela notícia principal, uma emoção dominante, tom de engenharia
- `data_extenso`: data da edição no header
- `intro`: curta; conecta a edição a engenharia aplicada, obra, montagem, prazo ou previsibilidade

### Passo 4 — Montar HTML e plain text

1. Partir de `assets/template.html` — estrutura, cores, espaçamentos e ordem são fixos. Substituir **somente** os placeholders `{{MAIÚSCULAS}}`; parciais em `assets/partials/`.
2. Preservar literalmente as variáveis de sistema da plataforma: `{{ mirror }}`, `{{ unsubscribe }}`. Elas não são placeholders editoriais e só viram links válidos no processamento da plataforma.
3. Regras de compatibilidade e identidade: `references/identidade-visual.md`. Nunca `display:flex`, `grid`, `linear-gradient`, `rgba()`, JavaScript, imagem em base64 ou caminho local.
4. Plain text a partir de `assets/plain-text-template.txt`, com as variáveis `{{ unsubscribe }}`.

### Passo 5 — Salvar artefatos e validar

Salvar **dentro do projeto**, na pasta da edição:

- `newsletter.html` — HTML completo, autossuficiente;
- `plain-text.txt`;
- `metadata.md` — começa com `Status: rascunho local`; registra data, assunto, itens de cada seção (com fontes das notícias), valores ao vivo, exceções de janela e, depois, IDs/links externos;
- `payload.json` — montado pelo validador, em formato fixo: `nome_campanha`, `assunto`, `pre_header`, `html`, `texto`, `link_aprovacao`.

Gravar em UTF-8 sem BOM (no PowerShell, nunca `Set-Content` sem `-Encoding utf8`; preferir a ferramenta de escrita de arquivos).

**Verificar links e imagens** antes de validar (e de novo a cada alteração do HTML):

```powershell
python .agents/skills/newsletter-ssm/scripts/check_links.py newsletter/AAAA-MM-DD --esperado "<URL>=<nome do evento/item>" ...
```

- Abre cada link e imagem do HTML e grava `links-report.json`. Erro: domínio inexistente, HTTP 4xx/5xx, domínio à venda, imagem que não é imagem, página que não menciona o texto `--esperado`.
- Passar `--esperado` para **todo link de conteúdo externo** (notícia, evento): `URL=nome do evento` ou `URL=trecho do título da matéria`. Isso prova que o link é da coisa certa, não só que abre.
- Erro → trocar o link pelo correto (achado na fonte original ou no site oficial) e rodar de novo. Nunca deduzir uma URL pelo nome do evento/site — toda URL vem de uma página aberta nesta execução.
- Aviso de redirecionamento → trocar pela URL final. Aviso de bloqueio (401/403/429) → abrir a página por outro meio (WebFetch/navegador), confirmar e registrar em `metadata.md`.

```powershell
python .agents/skills/newsletter-ssm/scripts/validate_edition.py newsletter/AAAA-MM-DD --sync --assunto "<assunto>" --pre-header "<pré-header>"
```

Com `verificar_links: true` no config, o validador recusa a edição sem `links-report.json` aprovado e do mesmo HTML.

`--sync` grava nome da campanha (`Radar Estrutural SSM — {AAAA-MM-DD}`), assunto, pré-header, HTML e texto no `payload.json`; depois valida placeholders esquecidos, variáveis obrigatórias, CSS proibido, imagens sem HTTPS, mojibake, tamanho do assunto e divergência entre payload e HTML. **Com qualquer erro, corrigir e validar de novo — nunca enviar.** Toda edição posterior do HTML exige novo `--sync`.

Nunca concluir uma edição sem `newsletter.html` salvo no projeto.

### Passo 6 — Publicar para aprovação e aprovar

Detalhes em `references/aprovacao.md`.

```powershell
python .agents/skills/newsletter-ssm/scripts/publish_approval.py newsletter/AAAA-MM-DD
```

- Gera a cópia de aprovação sem as variáveis da plataforma, grava em `aprovacoes-unid/ssm/newsletter-AAAA-MM-DD.html`, faz commit e push **só desse arquivo** e espera o link responder HTTP 200.
- Link: `https://unidcom.github.io/aprovacoes-unid/ssm/newsletter-AAAA-MM-DD.html`. O script grava em `payload.json → link_aprovacao`; registrar também em `metadata.md`.
- Se o script falhar (repositório não clonado, push recusado, link fora do ar): registrar e parar. Não criar rascunho na plataforma sem link de aprovação.

**Aprovação:** em execução explicitamente solicitada ou agendada, mandar o link e seguir **sem** esperar aprovação. Em teste, dúvida ou pedido de preview, mandar o link e parar.

Mostrar o link de aprovação junto com o assunto, o pré-header e o resumo das seções (item escolhido em cada uma). Um pedido de "rascunho" ou "preview" nunca autoriza criar a campanha na plataforma. Se o usuário pedir ajustes, corrigir o HTML, rodar `validate_edition.py --sync` e publicar de novo — o arquivo é substituído no mesmo link.

### Passo 7 — Criar o rascunho na Brevo

Detalhes em `references/brevo.md`.

```powershell
python .agents/skills/newsletter-ssm/scripts/create_draft.py create newsletter/AAAA-MM-DD --dry-run   # confere o corpo, sem chamar a API
python .agents/skills/newsletter-ssm/scripts/create_draft.py create newsletter/AAAA-MM-DD
```

- Chama **direto a API** da Brevo com as credenciais de `private/brevo.env` (nunca imprimir nem registrar os valores).
- Cria a campanha **só em rascunho**. O script não envia, não agenda e não dispara teste: o disparo aos contatos é feito manualmente no painel.
- Exige edição válida e `link_aprovacao` preenchido. Faz **uma única tentativa** e grava `brevo-response.json` com `campaign_id` e link do painel.
- Se a edição já tiver campanha, o `create` é recusado — para trocar o conteúdo use `update newsletter/AAAA-MM-DD --campaign-id ID`. Nunca criar uma segunda campanha para a mesma edição.
- Se o `create` falhar depois de gravar o `campaign_id` (conteúdo `pendente`), retomar com `update`, não com `create`.
- Sucesso: registrar `campaign_id` e link em `metadata.md` com `Status: rascunho na Brevo`. Falha: `Status: falhou` com a mensagem (sem segredos) e parar — sem rotação.

### Passo 8 — Confirmar a rotação

Somente depois que `create_draft.py` devolver o `campaign_id`. Para cada seção com estado usada na edição:

```powershell
python .agents/skills/newsletter-ssm/scripts/rotation.py mark-used --secao blog-ssm --item <ITEM> --confirmacao <CAMPAIGN_ID> --date AAAA-MM-DD
python .agents/skills/newsletter-ssm/scripts/rotation.py mark-used --secao solucao-destaque --item <ITEM> --confirmacao <CAMPAIGN_ID> --date AAAA-MM-DD
```

- `--confirmacao` é o `campaign_id` exato; o script rejeita qualquer valor não numérico e é idempotente (repetir com o mesmo ID não duplica).
- Se o item usado for diferente do selecionado (substituição pontual pedida pelo usuário), o script registra a observação.
- Registrar `Rotação avançada: sim` em `metadata.md`.
- Nunca editar o arquivo de estado à mão.

## Referências

- `config/newsletter.json` — fonte de verdade das seções, plataforma e aprovação.
- `references/empresa-e-ofertas.md` — posicionamento, público, provas, ofertas e rodapé.
- `references/identidade-visual.md` — marca e regras de HTML para e-mail.
- `references/curadoria-editorial.md` — escopo, fontes e critérios das notícias.
- `references/aprovacao.md` — publicação em aprovacoes-unid, link e falhas.
- `references/brevo.md` — API da Brevo, credenciais e rascunho.
