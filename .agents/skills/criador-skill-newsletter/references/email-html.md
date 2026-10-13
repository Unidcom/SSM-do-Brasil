# HTML de e-mail e convenção de placeholders

## Dois tipos de marcador

| Marcador | Quem preenche | Quando |
|---|---|---|
| `%%TOKEN%%` | `scaffold_skill.py` | uma vez, ao gerar a skill (cores, fonte, logo, rodapé, variáveis da plataforma) |
| `{{SLOT}}` (MAIÚSCULAS) | a skill gerada | a cada edição (conteúdo das seções) |
| variáveis da plataforma (`{{ mirror }}`, `{$unsubscribe}`…) | a plataforma de envio | no processamento da campanha — **nunca** substituir |

O validador da edição falha se sobrar `{{MAIÚSCULAS}}`, `[MARCADOR EM CAIXA ALTA]` ou `TODO(`; variáveis da plataforma são exigidas literalmente.

## Template gerado

`scaffold_skill.py` monta `assets/template.html` a partir de `assets/email/base.html`, inserindo uma linha por seção, na ordem do config:

| Tipo | Linha gerada |
|---|---|
| `editorial` com slot | parágrafo de introdução |
| `curadoria-externa` | rótulo + uma linha por slot para blocos com `parcial`; caixa com fundo suave e lista para blocos sem parcial |
| tipos com catálogo/calendário/fixado | uma linha `{{SLOT}}` com respiro lateral |
| `dados-ao-vivo` | linha de largura total (para `partials/stats-bar.html`) |
| `bloco-fixo` com `valores` | barra de números fixos já preenchida (rótulos ficam como `TODO`) |

Slots fixos do base: `{{SUBJECT}}` (title), `{{PREHEADER}}`, `{{EDITION_DATE}}`.

Se o cliente já tem um template aprovado, **substituir** o gerado: converter os campos variáveis em `{{SLOT}}` com os mesmos nomes do config e manter o resto literal.

## Parciais disponíveis (`assets/partials/`)

- `highlight.html` — destaque de notícia: `{{ACCENT_COLOR}}`, `{{TAG}}`, `{{TITLE}}`, `{{URL}}`, `{{CONTEXT}}`, `{{IMPACT_LABEL}}`, `{{IMPACT}}`. Alternar `ACCENT_COLOR` entre os destaques (ex.: acento → primária → terceira cor).
- `quick-item.html` — notícia curta: `{{URL}}`, `{{TITLE}}`, `{{SUMMARY}}`.
- `catalog-card.html` — card de case/produto/artigo: imagem, eyebrow, título, corpo, CTA.
- `offer-block.html` — bloco de oferta em cor primária com CTA.
- `stats-bar.html` — três números com rótulo.

Parciais são preenchidos e colados no slot; o HTML final não pode conter os placeholders do parcial.

## Regras de compatibilidade

- Tabelas com `role="presentation"`, largura 620 px, CSS inline.
- Proibido: `display:flex`, `grid`, `linear-gradient`, `rgba()`, `<script>`, `<div>` como wrapper externo, imagem base64, caminho local/`file://`.
- `bgcolor` + `background-color` em `<td>` coloridos. Faixas multicoloridas = tabela de células sólidas, nunca gradiente.
- Fonte com fallback em cada bloco de texto (`Montserrat,Arial,sans-serif`).
- Imagens com URL HTTPS pública e `alt`.
- Emojis como entidades HTML.
- Doctype + `xmlns:v`/`xmlns:o` + `x-apple-disable-message-reformatting`.
- Abaixo de ~100 KB (corte do Gmail).

## Variáveis por plataforma

| Plataforma | Ver no navegador | Descadastro | Proibido |
|---|---|---|---|
| Brevo | `{{ mirror }}` | `{{ unsubscribe }}` | — |
| MailerLite Classic | `{$url}` | `{$unsubscribe}` | `{$name…}` |
| Outra | descobrir na documentação | idem | idem |
