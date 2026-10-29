# Briefing da newsletter SSM do Brasil

Levantamento iniciado em 2026-10-09 para criar a skill `newsletter-ssm` no repositório `ssm`.

Fontes primárias desta rodada: MCP `ssm_do_brasil` (narrativa, ICP, PUV), site institucional e blog (API WordPress). Tudo que veio do MCP é inferência editorial da Unidcom sobre o cliente — números oficiais do cliente precisam de confirmação antes de ir a e-mail.

## 1. Empresa

- **Nome oficial:** SSM do Brasil · **Curto:** SSM
- **Site:** https://ssmdobrasil.com.br
- **Ramo:** indústria — soluções estruturais em aço e alumínio para o setor fotovoltaico e aplicações industriais
- **Endereço:** Rua Alcídio Zaniolo, 651, Roseira, CEP 83070-350, São José dos Pinhais/PR
- **Telefone/WhatsApp:** +55 (41) 99841-8202
- **E-mail comercial:** vendas@ssmdobrasil.com.br
- **CNPJ:** 12.273.815/0001-23
- **Fundação:** site diz "fundada em 22 de junho de 2010"; a narrativa no MCP diz "Desde 2011". **Precisa de confirmação** — não publicar ano divergente.
- **Objetivo da newsletter (proposto):** relacionamento técnico e autoridade de engenharia com integradores, EPCistas e distribuidores; manter a marca no ciclo de recompra e gerar pedidos de orçamento.

### Descrição consolidada a partir do site
Indústria brasileira especializada em estruturas para energia solar (solo, telhados, carport, correção de inclinação, acessórios, estruturas diversas) e extrusão de alumínio. Engenharia própria, fabricação nacional verticalizada (extrusora e perfiladeira próprias), materiais certificados (alumínio 6063/6005-T6, aço civil 300, inox 304), normas ABNT, certificações ISO 9001 e CE, selo ESG, programa PEIEX. Garantia estrutural de até 30 anos (conforme projeto e ambiente). Atende Brasil, América Latina e Europa.

### Posicionamento percebido
"Pioneira no desenvolvimento de estruturas para o setor fotovoltaico" no Brasil; engenharia aplicada como núcleo (não acessório); parceira técnica de integradores, EPCistas, distribuidores e indústrias — não fornecedora genérica de metal.

### Provas e diferenciais encontrados
- Engenharia própria com equipe técnica dedicada (projeto, cálculo, validação; canal direto com engenharia; atendimento em até 24h úteis — citado no ICP)
- Produção interna 100% nacional, verticalizada, com extrusora de alumínio e perfilaria própria em aço
- Certificações ISO 9001 e CE; laudos técnicos e documentação completa; rastreabilidade da matéria-prima à expedição
- Garantia estrutural de até 30 anos
- Reciclagem de 100% dos refugos de alumínio e descarte responsável (ESG técnico)
- Setor de PDI para produtos sob medida
- Portfólio: 6 linhas de solução + modelos 3D disponíveis no site

> **Precisa de confirmação:** ano de fundação (2010 no site × 2011 no MCP); números de market-share/projetos entregues não foram encontrados — não usar até confirmação.

## 2. Públicos identificados

Três ICPs (MCP `icp`):
1. **Distribuidores** — ticket 5, consciência 5. Previsibilidade de entrega, padronização entre lotes, política comercial estável, documentação e laudos, giro de estoque.
2. **EPCistas** — ticket 3, consciência 4. Projetos turn-key de grande porte; precisão de dimensionamento, qualidade constante entre lotes, soluções completas (solo/carport/telhado), suporte na obra.
3. **Integradores** — ticket 2, consciência 4. Geração distribuída residencial/comercial; agilidade de resposta técnica, confiança no dimensionamento, prazo, rastreabilidade.

### Decisão pendente de segmentação (base única × versões por público)
Sugestão: **base única** na primeira versão da newsletter, com tom técnico-comum (engenharia aplicada) e rodízio de foco por edição — as dores dos três públicos convergem (retrabalho, prazo, qualidade de lote, durabilidade).

## 3. Produtos e serviços encontrados

Soluções (menu do site): **Carport** · **Solo** · **Telhados** (cerâmico, fibrocimento, metálico, zipado, laje) · **Correção de inclinação** · **Acessórios** · **Estruturas diversas** · **Extrusão de Alumínio** · **Modelos 3D** (página própria) · **Projetos** (portfólio) · Catálogo 2026 (PDF no repositório local, `docs/referencias`).

## 4. Benefícios e argumentos encontrados

- Reduz custo e tempo de execução, evita retrabalho, protege reputação em campo (proposta de valor, MCP)
- Estrutura sob medida para cargas reais, normas e exigências do projeto — não perfil genérico
- Montagem sem falhas; durabilidade comprovada; previsibilidade de obra
- Kits estruturais prontos para montagem, entrega programada por fase de obra (síntese da oferta, MCP)
- Suporte técnico do dimensionamento à instalação

> **Regra recomendada:** dados regulatórios (NBR, ABNT), percentuais e condições financeiras verificados em fonte atual a cada edição. Tema sensível: **histórico de Recuperação Judicial** — nunca citar espontaneamente; a narrativa pede "transparência e maturidade" apenas se o cliente pedir.

## 5. Tom editorial sugerido

Técnico, direto, de engenharia — fala de campo, não de marketing. Argumento técnico antes de comercial. Reescrever notícias em pt-BR; nada de clickbait. Vocabulário a priorizar: "engenharia aplicada", "estrutura", "dimensionamento", "durabilidade", "montagem", "obra", "previsibilidade".

### Temas editoriais identificados
Blog ativo (2–3 posts/mês): dimensionamento técnico (isopletas NBR 6123, fixação lateral vs inferior, aço vs alumínio), educação (o que é carport, estrutura de solo), escolha de fornecedor, eventos (Intersolar 2026), corrosão/ambientes agressivos, correção de inclinação.

## 6. Seções da newsletter (proposta)

| # | Seção | Tipo | Como puxa | Quantidade | Avança quando | Se falhar |
|---|---|---|---|---|---|---|
| 1 | Abertura (assunto, data, intro) | `editorial` | escrito a partir da edição | 1 assunto + 1 intro | — | — |
| 2 | Radar do setor (destaques + giro rápido) | `curadoria-externa` | busca web, janela 7 dias, fontes do setor solar | 3 destaques + 5 curtas | — | estender até 10 dias; faltou material → parar |
| 3 | Solução em destaque | `rotacao-catalogo` | `assets/solucoes/catalog.json` (6 linhas) | 1 solução | `campaign_id` gravado | sem item → parar |
| 4 | Do blog da SSM | `pool-sem-repeticao` | `assets/blog/catalog.json` (posts publicados) | 1 post | `campaign_id` gravado | sem item → omitir |
| 5 | SSM em números | `bloco-fixo` | números aprovados no config: Desde 2010 · até 30 anos de garantia · ISO 9001 e CE | 3 números | — | — |
| 6 | CTA orçamento | `bloco-fixo` | botão com ícone WhatsApp → wa.me/554198418202 | 1 CTA | — | — |

## 7. Conteúdo comercial para rotação

- **Blog:** 12 posts públicos (API WP), todos elegíveis; catálogo inicial montado a partir da lista em 2026-10-09.
- **Soluções (6):** carport, solo, telhados, correção de inclinação, acessórios, estruturas diversas — cada uma com página própria no site para imagem/CTA.
- **CTA principal:** "Solicitar orçamento" → https://ssmdobrasil.com.br/contato/ (âncora #orcamento no site).
- **CTA secundários:** catálogo → https://ssmdobrasil.com.br/solucoes/ (verificar página exata do catálogo); modelos 3D → https://ssmdobrasil.com.br/modelos-3d/.

## 8. Identidade visual

### Encontrado
- Cores do site (usadas na home): primária **#00539C** (azul), acento **#15D1FF**/**#01B5E1** (ciano), escura **#041E36**, fundo claro #FFFFFF/#F5F7FA (proposto), texto #333F4B (proposto).
- Logo branco (fundo escuro), HTTPS público: `https://ssmdobrasil.com.br/wp-content/uploads/elementor/thumbs/logo-white-rosghll1m2nqrkzjnxg2jk005mo5tji97hmpeo6uio.png` (5 KB; variante menor de 3 KB também disponível).
- Fonte do site: pilha Elementor padrão (confirmar; sugestão e-mail: `Montserrat,Arial,sans-serif`).

### Ainda necessário
> **Precisa de confirmação:** logo horizontal em alta resolução preferido; logo para fundo claro (versão colorida/azul), se existir; fonte oficial da marca; manual de marca, se houver.

## 9. Métricas e prova social

- Números candidatos (todos do MCP/site, **precisam de aprovação antes de publicar**): "Desde 2010" (ou 2011 — ver divergência) · "até 30 anos de garantia" · "ISO 9001 e CE" · "100% produção nacional".
- Não há contadores públicos no site → nada de `dados-ao-vivo` por enquanto; **bloco-fixo** com 3 números aprovados.

## 10. Informações editoriais

- Frequência/dia/horário: **semanal, quarta, 09:00** (confirmado 2026-10-09).
- Janela das notícias: 7 dias (extensão até 10).
- Fontes obrigatórias de curadoria (setor solar — as mesmas validadas na Vésper): Canal Solar, Fotovolt/Aranda, Giro ABSOLAR, Energy Channel, Folha (energia solar), Exame (energia solar); complementares: ANEEL, EPE, pv magazine.
- Temas a evitar: política partidária, especulação como fato, promessas absolutas de economia, menção espontânea a Recuperação Judicial, falência/demissões de terceiros sem relação operacional.
- Limite de promoção: 2 blocos comerciais por edição (blog + solução) + CTA fixo.

## 11. Blocos fixos

- Abertura padrão: introdução curta conectando a edição a engenharia, obra e previsibilidade.
- CTA permanente: solicitar orçamento → https://ssmdobrasil.com.br/contato/
- Rodapé jurídico: SSM do Brasil · Rua Alcídio Zaniolo, 651, Roseira, São José dos Pinhais/PR · CNPJ 12.273.815/0001-23 · vendas@ssmdobrasil.com.br · (41) 99841-8202 · site ssmdobrasil.com.br
- Motivo de recebimento (proposto): "Você recebeu este e-mail por fazer parte da base de relacionamento da SSM do Brasil."
- Variáveis "ver no navegador"/"descadastro": conforme plataforma escolhida.

## 12. Envio e automação

- Plataforma: **Brevo** (confirmado 2026-10-09).
- Remetente verificado: **`marketing@ssmdobrasil.com.br` (sender ID 1, ativo)** — confirmado na API em 2026-10-13; alternativa ativa: `gestaocomercial@ssmdobrasil.com.br` (ID 2).
- Lista de destino: **padrão `BREVO_LIST_IDS=21` (CLIENTES INTERSOLAR, 1.092 contatos)** — ajustar quando a base da newsletter for definida. Outras listas: [5] DIA 1 2º Lista (275) · [4] DIA 2 1º Lista (297) · [22] Pesquisa de satisfação (115).
- Credenciais: **`private/brevo-ssm.env`** (cópia operacional em `private/brevo.env`) — fora do Git. **Atenção: a conta tem whitelist de IP**; liberar IPs em https://app.brevo.com/security/authorised_ips antes de usar de outra rede.
- Base de destino: **base inteira** (decisão 2026-10-13): `BREVO_LIST_IDS=21,5,4,22,12` — CLIENTES INTERSOLAR (1.092) + DIA 1 2º Lista (275) + DIA 2 1º Lista (297) + Pesquisa de satisfação (115) + Captação de Leads (0) ≈ **1.779 contatos**. Fora da base: Equipes SSM (15, 14) e listas sistêmicas (8, 7).
- Sem servidor MCP (não há MCP oficial do Brevo) — acesso 100% via API v3 (`https://api.brevo.com/v3`, header `api-key`), encapsulada nos scripts da skill.
- Aprovação: **dispensada quando solicitada ou agendada** (confirmado 2026-10-09) — execução agendada segue direto ao rascunho.
- `aprovacoes-unid`: clonado em `C:\Users\UNID\Desktop\Repositórios\aprovacoes-unid` (irmão do projeto) ✓; pasta do cliente: **`ssm`** (confirmado).
- Pasta das edições (proposta): `newsletter/` na raiz do projeto.
- Histórico de uso: `newsletter/.rotation-state.json` (gerido só por `rotation.py`).

## 13. Perguntas prioritárias

1. Nome da newsletter (sugestão: **Radar Estrutural SSM**).
2. Frequência, dia e horário (sugestão: semanal, quarta, 09:00).
3. Base única (integradores + EPCistas + distribuidores) ou segmentada? (sugestão: base única)
4. Plataforma de envio e remetente verificado? (sugestão: Brevo, como a Vésper, se a base já estiver lá)
5. Aprovação sempre antes de criar rascunho? (sugestão: sempre)
6. Pasta do cliente em `aprovacoes-unid`: `ssm` ou `ssm-do-brasil`?
7. Ano oficial: 2010 ou 2011?
8. Números aprovados para a barra "SSM em números"?

## 13.1. Decisões confirmadas em 2026-10-09

| # | Decisão | Valor |
|---|---|---|
| 1 | Agenda | Semanal, **quarta, 09:00** (America/Sao_Paulo) |
| 2 | Plataforma | **Brevo** (rascunho via API; credenciais em `private/brevo.env`) |
| 3 | Aprovação | **Dispensada quando solicitada ou agendada** — execução agendada segue direto ao rascunho |
| 4 | Nome | **Radar Estrutural SSM** |
| 5 | Ano oficial | **2010** (site oficial prevalece sobre o MCP) |
| 6 | Público | **Base única** (integradores + EPCistas + distribuidores, tom técnico-comum) |
| 7 | Pasta em aprovacoes-unid | **`ssm`** |
| 8 | Barra de números | **Desde 2010 · até 30 anos de garantia · ISO 9001 e CE** |
| 9 | Imagens dos cards | **Imagens das páginas de solução do site oficial** (URLs verificados na Fase 6) |

### Decisões confirmadas em 2026-10-13

| # | Decisão | Valor |
|---|---|---|
| 10 | Ordem das seções | **Solução em destaque logo após os destaques** do Radar do setor (e antes do Giro rápido e do blog) |
| 11 | CTA orçamento | ~~Botão com ícone WhatsApp~~ — **substituída pelo layout v3 (2026-10-29)**: botão ciano "Solicitar orçamento pelo WhatsApp →", sem ícone; link direto **wa.me/554198418202** (número oficial do site), com mensagem pré-preenchida |
| 12 | Visual da seção Solução | ~~Faixa escura `#052B4D`~~ — **substituída pelo layout v3 (2026-10-29)**: faixa azul-clara `#E5F6FB` com card branco; continua distinta do bloco do blog (que não tem faixa) |
| 13 | Base de destino | **Base inteira**: listas 21, 5, 4, 22, 12 (~1.779 contatos). Fora: Equipes SSM (15, 14) e sistêmicas (8, 7) |

### Decisões confirmadas em 2026-10-29 (layout v3)

Referência: `newsletter/2026-10-14-teste-v3/newsletter.html`; a skill `newsletter-ssm` passou a gerar esse layout.

| # | Decisão | Valor |
|---|---|---|
| 14 | Layout | Hero com mosaico de 3 capas + título (h1 = assunto) + deck + 3 takeaways; destaque 1 principal e 2 compactos; Solução em faixa `#E5F6FB`; Giro rápido em linhas sem resumo; rodapé com redes sociais |
| 15 | Tamanho dos textos | Destaque 1: contexto 35–60 e "Para a obra" 15–30 palavras; destaques 2–3: contexto 25–45 e "Para a obra" 10–25. Solução e blog usam `texto_curto` do catálogo |
| 16 | Imagens das capas | **Imagem da própria notícia (og:image) por padrão**; imagem gerada (ex.: via Codex, publicada em `aprovacoes-unid/ssm/img/`) quando a da matéria não servir |
| 17 | Decisões #11 e #12 | Substituídas pelo v3 (ver acima) |

### Pendências remanescentes
- ~~Remetente verificado na Brevo e ID(s) de lista de destino~~ → resolvido em 2026-10-13 (sender 1 `marketing@ssmdobrasil.com.br`; lista padrão 21). Ajustar `BREVO_LIST_IDS` quando a base definitiva da newsletter for decidida.
- Nome de campanha fixado como `Radar Estrutural SSM — {AAAA-MM-DD}` (implícito pela decisão 4).
- Logo para fundo claro, se existir (não bloqueia: header/rodapé usam fundo escuro).
- Whitelist de IP da Brevo: a conta exige IPs autorizados (https://app.brevo.com/security/authorised_ips). IP desta máquina já liberado em 2026-10-13; em outra rede, liberar antes de gerar edição.

## 14. Fontes consultadas

- MCP `ssm_do_brasil` — `consultar_cliente` (narrativa, icp, puv, checklist) · https://mcp.unidcom.com.br/mcp
- Site institucional — https://ssmdobrasil.com.br (home, quem-somos)
- Blog via API WordPress — https://ssmdobrasil.com.br/wp-json/wp/v2/posts (12 posts, 2026-06 a 2026-10)
- Catálogo 2026 (PDF local) e formulário "Produtos SSM | Diferenciais" (PDF local, `docs/referencias/`)
- Repositório de aprovação — `C:\Users\UNID\Desktop\Repositórios\aprovacoes-unid`
- Repositório `vesper-newsletter` — fontes de notícias validadas em 10 edições reais (2026-07 a 2026-10; 70 URLs extraídos das edições): Canal Solar (43 usos), Fotovolt/Aranda (9), Exame (4), Folha (4), pv magazine (3), ABSOLAR, MME, Câmara, IEA. Energy Channel existe como obrigatória da Vésper, mas ainda sem uso prático.
