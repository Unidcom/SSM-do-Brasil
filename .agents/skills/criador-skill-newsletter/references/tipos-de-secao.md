# Tipos de seção

Cada seção da newsletter é declarada em `config/newsletter.json → secoes[]` e tem exatamente um tipo. O tipo responde a quatro perguntas:

1. **De onde puxa?** (fonte do conteúdo)
2. **Como escolhe?** (regra de seleção)
3. **Quando o estado avança?** (só tipos com estado)
4. **E se falhar?** (parar, fallback, omitir)

Campos comuns a todas as seções:

| Campo | Obrigatório | Descrição |
|---|---|---|
| `id` | sim | identificador curto, `kebab-case`, único |
| `tipo` | sim | um dos tipos abaixo |
| `titulo` | sim | rótulo visível ou interno (ex.: `Destaques da semana`) |
| `slot` | sim | placeholder no template, ex.: `CASE_BLOCK` → `{{CASE_BLOCK}}` |
| `descricao` | não | uma frase do papel da seção no e-mail |
| `se_falhar` | não | `parar` (padrão para seções com estado e dados ao vivo), `omitir`, ou `fallback` com `fallback_html` |

Tipos **com estado** gravam histórico em `estado` (ver `config-newsletter.md`) por meio de `scripts/rotation.py`. Regra universal: **selecionar não grava nada; o estado só avança com `mark-used`, depois que o rascunho existir na plataforma (`campaign_id`)** (ver `regras-universais.md`).

Exceção ao campo `slot`: em `curadoria-externa` os slots ficam em cada bloco (`blocos[].slots`), não no nível da seção; em `bloco-fixo` e `editorial` o slot é opcional.

---

## `curadoria-externa` — notícias de fontes externas

**Puxa de:** busca na web nas fontes declaradas, dentro de uma janela de dias.
**Escolhe:** critérios editoriais de relevância (prosa em `references/curadoria-editorial.md` da skill gerada).
**Estado:** nenhum. A repetição entre edições é evitada pela janela curta e, opcionalmente, conferindo o `metadata.md` das últimas edições.

Campos:

| Campo | Exemplo | Nota |
|---|---|---|
| `janela_dias` | `7` | aceitar só publicação dentro da janela; confirmar a data na página original |
| `janela_max_dias` | `10` | extensão permitida se faltar material; registrar a exceção em `metadata.md` |
| `fontes_obrigatorias` | `[{"nome","url"}]` | todas devem ser verificadas a cada edição |
| `fontes_complementares` | `[...]` | usadas para completar ou confirmar (fontes primárias/oficiais) |
| `blocos` | ver abaixo | uma seção de curadoria pode alimentar vários blocos |
| `evitar` | `["demissões", ...]` | temas proibidos |
| `idioma_saida` | `pt-BR` | sempre reescrever, nunca traduzir literalmente |

`blocos` divide a curadoria em formatos — é o que permite "3 destaques + 5 curtas" saírem da mesma pesquisa:

```json
"blocos": [
  {"id": "destaques", "quantidade": 3, "slots": ["HIGHLIGHT_1","HIGHLIGHT_2","HIGHLIGHT_3"],
   "parcial": "assets/partials/highlight.html",
   "campos": {"tag": "tema estratégico, não a fonte", "titulo": "gancho específico, sem clickbait",
              "contexto": "80–130 palavras", "impacto": "45–80 palavras, rótulo 'O que isso significa para você:'",
              "url": "fonte original"}},
  {"id": "curtas", "quantidade": 5, "slots": ["QUICK_1","QUICK_2","QUICK_3","QUICK_4","QUICK_5"],
   "campos": {"titulo": "uma linha", "url": "fonte"}}
]
```

Uma notícia não pode aparecer em dois blocos da mesma edição. `quantidade` é exata — nunca entregar a menos; se faltar material após `janela_max_dias`, parar e avisar.

**Exemplos:** Vésper (energia solar, 7 dias, 3+5), Unidcom (marketing digital, 2 dias, 3+5).

---

## `rotacao-catalogo` — próximo item de uma lista, em ordem

**Puxa de:** `catalogo` (JSON) com itens prontos (modelo HTML + dados).
**Escolhe:** o item ativo seguinte ao último usado, em ordem circular. Sem histórico → primeiro ativo.
**Estado:** avança com `mark-used`.

Campos: `catalogo` (caminho relativo à skill), `ordem: "circular"` (único valor hoje).

Formato do item no catálogo:

```json
{"id": "case-1", "ativo": true, "modelo": "assets/cases/models/case-1.html",
 "imagem_publica": "https://...", "imagem_local": "docs/cases/case-1.png",
 "dados": {"segmento": "Residência", "potencia": "16,2 kWp", "paineis": 40}}
```

- `ativo: false` tira o item da rotação sem apagá-lo (ex.: produto esgotado).
- Se o item tem imagem, `imagem_publica` HTTPS é obrigatória para envio; `imagem_local` só para preview.
- Dados do item (números, resultados) não podem ser alterados na redação — vêm do catálogo.

**Exemplo:** cases da Vésper (12 cases, um por edição, circular).

---

## `pool-sem-repeticao` — qualquer item ainda não usado recentemente

**Puxa de:** `catalogo` (ex.: artigos do blog do cliente).
**Escolhe:** primeiro item ativo, na ordem do catálogo, que não esteja entre os últimos `janela_itens` usados. Se todos foram usados recentemente, o usado há mais tempo.
**Estado:** avança com `mark-used`.

Campos: `catalogo`, `janela_itens` (ex.: `10`).

Use quando a ordem não importa, mas repetir sim. O catálogo pode ser atualizado a cada edição (ex.: buscar posts novos no blog e acrescentar ao JSON antes de selecionar) — descrever isso no passo da seção.

**Exemplo:** blogs da Unidcom (não repetir os últimos 10).

---

## `kit-catalogo` — item principal + componentes compatíveis

**Puxa de:** `catalogo` (itens principais) e um catálogo por componente (`componentes[].catalogo`).
**Escolhe:** o próximo item principal em ordem circular; em cada componente, entre os itens listados como compatíveis no item principal (campo `campo_compat`), o usado há mais tempo (empate → ordem do catálogo). Componente `opcional` sem compatível fica fora do kit.
**Estado:** avança com `mark-used --componentes id=item,...` (o `select` mostra o comando).

Campos: `catalogo`, `componentes` (`id`, `catalogo`, `campo_compat`, `opcional`), `parcial`. Use quando a seção combina peças de listas diferentes que precisam ser compatíveis entre si (ex.: produto + técnica + acabamento) e as duplas não podem se repetir em sequência fixa.

**Exemplo:** kit da semana da SP< (32 produtos × 5 aplicações × 5 personalizações do catálogo 2026).

---

## `alternancia` — alterna entre grupos, um por edição

**Puxa de:** `catalogo` cujos itens têm o campo `grupo`.
**Escolhe:** o grupo seguinte ao último usado na lista `grupos`; dentro do grupo, o próximo item em ordem circular (por grupo).
**Estado:** avança com `mark-used`.

Campos: `catalogo`, `grupos` (ex.: `["blog","produto"]`).

**Exemplo:** seção "Da Unidcom para você" (blog ↔ produto, edição a edição).

---

## `calendario` — o item depende da data, sem estado

**Puxa de:** `opcoes` declaradas no config (cada uma com `modelo` ou conteúdo).
**Escolhe:** pela regra:

| `regra` | Chaves de `opcoes` |
|---|---|
| `semana-iso-paridade` | `impar`, `par` |
| `dia-da-semana` | `seg`, `ter`, `qua`, `qui`, `sex`, `sab`, `dom` |
| `mes` | `01`…`12` (ausentes usam `padrao`) |

**Estado:** nenhum — a mesma data sempre dá o mesmo resultado (reprodutível em reenvios).

**Exemplo:** oferta da Vésper (orçamento na semana ímpar, viabilidade na par).

---

## `fixado` — conteúdo de campanha que sobrepõe a rotação

**Puxa de:** um item fixo (`item` de um `catalogo`, ou `modelo` direto).
**Escolhe:** sempre o item fixado enquanto `ate` (data, opcional) não passou. Depois, aplica `senao` — outra regra completa (qualquer tipo com estado ou `calendario`).
**Estado:** registra o uso com `mark-used` (para histórico), mesmo sem precisar dele para escolher.

Campos: `catalogo` + `item`, ou `modelo`; `ate` (`AAAA-MM-DD`, opcional); `senao` (objeto de seção sem `id`/`slot`); `substituicao_pontual` — texto dizendo que trocar o item numa edição exige pedido explícito do usuário.

**Exemplo:** isca da Calculadora de CPL na Unidcom (fixada enquanto a campanha estiver ativa; antes era `alternancia` blog/produto — isso vira o `senao`).

---

## `dados-ao-vivo` — números buscados na hora

**Puxa de:** uma URL (HTML ou JSON), via `scripts/fetch_live_data.py`.
**Escolhe:** extrai campos por regex (HTML) ou caminho (JSON).
**Estado:** nenhum. **Nunca reaproveitar valor de edição anterior nem estimar.**

Campos:

```json
{"fonte": "html", "url": "https://unidcom.com.br/", "tentativas": 2,
 "campos": [
   {"id": "ads",  "rotulo": "Investimento em Anúncios", "regex": "id=\"counter-ads-value\"[^>]*data-number=\"([^\"]+)\"", "formato": "R$ X,XM+"},
   {"id": "roas", "rotulo": "ROAS", "regex": "id=\"counter-roas-value\"[^>]*data-number=\"([^\"]+)\"", "formato": "XX,XX×"}
 ]}
```

```json
{"fonte": "json", "url": "https://n8n.../numeros-mailerlite", "metodo": "POST", "corpo": {},
 "campos": [{"id": "total", "caminho": "data[title=_active-subscribers].total", "formato": "inteiro pt-BR (33.020)"}]}
```

O regex depende da ordem real dos atributos no markup — escrevê-lo a partir do HTML baixado e testá-lo na Fase 6. A primeira captura do regex é o valor bruto; `formato` orienta a formatação na redação. `se_falhar` padrão: `parar` antes do preview e do envio, avisando o usuário.

**Exemplos:** stats do site da Unidcom; total de inscritos ativos no MailerLite.

---

## `bloco-fixo` — HTML que não muda

**Puxa de:** `modelo` (arquivo HTML) ou diretamente do template.
**Escolhe:** nada. Mudança só com aprovação do usuário.

Campos: `modelo` (opcional; se ausente, o bloco vive no próprio template e `slot` pode ser omitido), `valores` (opcional, para números fixos aprovados — ex.: `{"clientes":"1.000+"}`).

**Exemplos:** métricas fixas da Vésper (1.000+ clientes, 6+ anos, 72 meses), CTA box e footer da Unidcom.

---

## `editorial` — texto escrito a cada edição a partir do resto

**Puxa de:** as outras seções da própria edição.
**Escolhe:** —

Campos: `campos` com regras de redação. Usos típicos:

- `assunto` (até `assunto_max` caracteres, sustentado pela notícia principal, uma emoção dominante);
- `pre_header`;
- `intro` (saudação fixa + conexão com o tema da edição);
- `data_extenso` (ex.: `Quinta-feira, 17 de abril de 2026`).

---

## Escolhendo o tipo

| A seção… | Tipo |
|---|---|
| traz notícias de fora | `curadoria-externa` |
| mostra um item de uma lista fixa, em ordem | `rotacao-catalogo` |
| mostra um item que não pode repetir, ordem tanto faz | `pool-sem-repeticao` |
| combina peças de listas diferentes que precisam ser compatíveis | `kit-catalogo` |
| alterna entre tipos de conteúdo | `alternancia` |
| muda conforme semana/dia/mês | `calendario` |
| mostra sempre a mesma campanha por um tempo | `fixado` (com `senao`) |
| mostra números atuais de um site/API | `dados-ao-vivo` |
| nunca muda | `bloco-fixo` |
| é escrita a partir do resto da edição | `editorial` |

Se nenhum tipo serve, descrever a seção em prosa no `SKILL.md` gerado como tipo `editorial` e registrar no briefing que ela é manual — não inventar um tipo novo sem implementar o suporte em `rotation.py`.
