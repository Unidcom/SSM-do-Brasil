# Fontes e Boards

Use esta referencia quando a tarefa envolver planejamento editorial para um cliente atendido pela Unidcom.

## Board Estrategico

Fonte: `https://mcp.unidcom.com.br/`

O board estrategico e a fonte primaria do planejamento. Se houver um board do cliente, use-o antes de qualquer outra fonte e trate seus fatos explicitos como prevalentes em caso de conflito. Procure por:

- nome do cliente, segmento e ofertas prioritarias;
- objetivos comerciais e de comunicacao;
- publico, personas, decisores e influenciadores;
- posicionamento, diferenciais, mensagens-chave e promessas que podem ser sustentadas;
- pilares de conteudo, campanhas, eventos, sazonalidades e temas em andamento;
- restricoes de tom, compliance, palavras proibidas, aprovacoes e canais ativos;
- aprendizados, objecoes recorrentes, provas, cases, dados e materiais ja existentes.

Se o site expuser uma interface em vez de API direta, use navegador ou ferramenta disponivel para localizar o board do cliente. Se houver MCP/tool especifico disponivel na sessao, prefira-o ao scraping manual. Nao salve credenciais, cookies, tokens ou dumps sensiveis no repositorio.

Ao usar informacoes do board, separe:

- `fatos do board`: informacoes explicitamente encontradas;
- `inferencias`: conclusoes editoriais derivadas desses fatos;
- `lacunas`: dados que faltam para fechar o planejamento com seguranca.

## Documento de Clientes

Fonte: `https://docs.google.com/document/d/1M2fF6-PeO3iT_bGZG_nFEtC_T1Ia4BriNYRbP-HIe5s/edit?usp=sharing`

Consulte este documento somente quando nao houver board estrategico do cliente disponivel nos MCPs. Nessa situacao, use-o como fonte de contexto e busque dados de:

- descricao do negocio;
- produtos, servicos e prioridades atuais;
- tom de voz;
- publico-alvo;
- canais usados;
- historico de comunicacao;
- cuidados, restricoes e preferencias aprovadas.

Nao use o Google Doc para completar, atualizar ou contradizer um board existente, salvo instrucao expressa do usuario. Se nao houver board e o Google Doc estiver indisponivel, use o contexto local e avise a indisponibilidade quando ela afetar decisoes importantes.

## GPT de Referencia

Fonte: `https://chatgpt.com/g/g-69a86484b600819194a037816ae6e185-estrategista-editorial-multicanal`

Use como referencia conceitual quando suas instrucoes estiverem visiveis ou forem fornecidas pelo usuario. Se a pagina nao expuser o prompt/instrucoes, nao invente o conteudo interno do GPT. Preserve apenas o objetivo observavel: estrategia editorial multicanal para planejamentos de clientes.

## Historico Local

Antes de planejar, verifique arquivos locais relevantes:

- `codex/config/project-rules.md`
- `codex/config/client-preferences.md`
- `codex/memory/`
- `codex/templates/`
- entregas anteriores em pastas como `Blog/`, `Carrosseis/`, `Newsletter/` e `Estaticos/`

Use o historico para evitar repeticao, reaproveitar aprendizados e manter coerencia com entregas ja aprovadas.

## Quando Falta Contexto

Nao interrompa por detalhes menores. Siga com hipoteses marcadas quando a decisao for reversivel.

Pare e pergunte pelo minimo necessario quando faltar uma destas informacoes:

- qual cliente sera planejado;
- periodo do planejamento;
- canais obrigatorios;
- objetivo principal do periodo;
- oferta/campanha central, quando o planejamento depende disso.

Se o usuario pedir velocidade, entregue uma versao preliminar com uma secao `Hipoteses usadas`.
