---
name: estrategista-editorial-multicanal
description: Planeja calendarios editoriais multicanal para clientes da Unidcom usando objetivos, boards estrategicos, referencias de cliente e formatos de conteudo. Use quando o usuario pedir planejamento editorial, pauta mensal, matriz de conteudo, calendario de posts, estrategia de canais ou desdobramentos de campanha para clientes atendidos.
---

# Skill: Estrategista Editorial Multicanal

Cria planejamentos editoriais para clientes da Unidcom com consistencia estrategica entre canais, objetivos de negocio, funil, narrativa de marca e capacidade real de producao.

Use esta skill para planejamento, pauta, calendario, pilares editoriais, series, campanhas, matriz de canais, linhas narrativas e desdobramentos multicanal. Nao use para produzir uma peca final isolada quando outra skill local for mais especifica, como carrossel, newsletter, blog SEO ou estatico.

## Fontes e Hierarquia de Contexto

Antes de fechar qualquer planejamento para um cliente, consulte as fontes disponiveis nesta ordem:

1. Pedido do usuario e arquivos anexados.
2. Board estrategico do cliente no MCP em `https://mcp.unidcom.com.br/`. Esta e a fonte primaria: prevalece sobre documento, historico e inferencias quando houver conflito.
3. Documento de referencia de clientes (`https://docs.google.com/document/d/1M2fF6-PeO3iT_bGZG_nFEtC_T1Ia4BriNYRbP-HIe5s/edit?usp=sharing`), somente para clientes que nao tenham board estrategico disponivel nos MCPs.
4. Historico local relevante em `codex/memory/`, `codex/config/`, `codex/templates/` e entregas anteriores do cliente neste repositorio.
5. Quando acessiveis, instrucoes ou materiais do GPT de referencia e anexos fornecidos pelo usuario.

Nao use o documento de clientes para complementar ou substituir um board existente sem pedido expresso do usuario. Se uma fonte externa exigir credencial, token, sessao ou permissao que nao esteja disponivel, avise objetivamente qual fonte ficou inacessivel e siga apenas se houver contexto suficiente. Para informacoes essenciais de posicionamento, oferta, publico ou objetivo, solicite o recorte minimo ao usuario em vez de preencher lacunas com suposicoes.

## Fluxo

1. Faca o diagnostico antes de propor ou estruturar o planejamento. Identifique cliente, segmento, produtos ou servicos, ticket medio quando relevante, diferencial, PUV, publico, dores, desejos, objecoes, canais ativos, blog, midia paga, objetivo do periodo e restricoes de producao. Obtenha esses dados primeiro no board; quando nao houver board, no documento de clientes e no contexto local. Pergunte ao usuario somente pelos dados essenciais que continuarem ausentes.
2. Pergunte ou verifique se ja existem pautas definidas para o periodo. Se existirem, use-as como insumo e valide sua coerencia estrategica; se nao existirem, proponha pautas baseadas em publico, dores, desejos, tendencias, oportunidades de busca e oportunidades de posicionamento.
3. Leia `references/fontes-e-boards.md` para aplicar a hierarquia de fontes e coletar o contexto do cliente.
4. Sintetize o diagnostico editorial: momento do cliente, publico, proposta, ofertas, objecoes, eventos, oportunidades e riscos. Diferencie fatos do board, inferencias e lacunas.
5. Defina a arquitetura do planejamento:
   - objetivo do periodo;
   - pilares editoriais;
   - campanhas ou temas-guia;
   - papeis por canal;
   - cadencia e formatos;
   - CTAs por etapa do funil.
6. Planeje, quando fizer sentido para o escopo do cliente, conteudos para blog, editorial/redes sociais e anuncios. Distribua pautas entre momentos do funil; preserve equilibrio entre formatos, objetivos e progressao narrativa.
7. Monte o calendario ou matriz no nivel pedido pelo usuario. Se o usuario nao especificar formato, entregue uma tabela por semana com data sugerida, canal, formato, pauta, angulo, objetivo, CTA e observacoes de producao.
8. Inclua uma camada de coerencia multicanal: explique como uma mesma ideia se desdobra sem repetir a mesma copy em todos os canais.
9. Feche com proximos passos praticos: aprovacoes pendentes, informacoes faltantes, prioridades de producao e pautas que podem virar brief para outras skills.

## Regras de Producao e Estrutura de Pautas

- Toda atividade de video cuja captacao ainda precisa acontecer deve conter a palavra `Gravação` na pauta da atividade. A regra se aplica ao titulo/pauta, e nao apenas a observacoes ou pendencias. Nao a use para videos feitos exclusivamente com materiais ja existentes.
- Ao detalhar uma pauta, use obrigatoriamente a estrutura correspondente em `references/estruturas-de-pauta.md`. Mantenha todos os campos, na ordem definida, e nao deixe campos obrigatorios sem resposta.
- Classifique o tipo de entrega antes de escolher a estrutura: organico/newsletter/boletim/GD/material grafico; anuncio; ou blog/SEO. Para uma peca hibrida, use a estrutura que corresponde ao objetivo predominante e registre a adaptacao no desenvolvimento ou direcionamentos.
- A tabela de calendario e um indice de execucao; ela nao substitui a estrutura completa de cada pauta quando o usuario pedir pautas, briefings, detalhamento ou direcionamentos de producao.

## Criterios Editoriais

- Planejamento deve conectar conteudo a objetivo de negocio; evite calendarios que sejam apenas uma lista de temas.
- Cada pilar precisa ter funcao clara: autoridade, educacao, prova, relacionamento, demanda, comunidade, produto, institucional ou conversao.
- Diferencie canal por comportamento de consumo. LinkedIn, Instagram, blog, newsletter, e-mail, YouTube, landing page e WhatsApp nao devem receber o mesmo texto com pequenas trocas.
- Priorize pautas com tese, conflito ou utilidade concreta. Evite temas genericos como "dicas", "beneficios" ou "importancia de" sem recorte especifico.
- Preserve o tom e as restricoes do cliente quando aparecerem no board ou no documento de referencia.
- Quando houver pouco contexto, entregue um planejamento assumidamente preliminar com hipoteses marcadas.
- Evite pautas genericas: cada uma deve ter uma tese, um publico ou dor clara, um papel no funil e uma acao esperada.

## Saida Padrao

Entregue em portugues do Brasil e com acentuacao correta.

Para planejamentos completos, use esta estrutura:

1. `Resumo estrategico`
2. `Pilares editoriais`
3. `Papel de cada canal`
4. `Calendario editorial`
5. `Desdobramentos por campanha`
6. `Pautas prioritarias para producao`
7. `Pendencias e hipoteses`

Para pedidos menores, responda no formato mais direto que resolva a demanda, mantendo as fontes e criterios acima.

## Referencias

- `references/fontes-e-boards.md` - como consultar boards estrategicos, documento de clientes e historico local.
- `references/modelos-de-saida.md` - modelos de tabelas e formatos de entrega para planejamentos.
- `references/estruturas-de-pauta.md` - campos obrigatorios para cada tipo de pauta.
