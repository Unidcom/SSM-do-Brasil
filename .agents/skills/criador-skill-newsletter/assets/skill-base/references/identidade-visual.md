# Identidade visual — %%EMPRESA%%

`assets/template.html` é a fonte executável deste padrão: estrutura, cores, espaçamentos e ordem das seções não mudam entre edições.

## Paleta usada no template

| Papel | Cor |
|---|---|
| Primária (header, rótulos, blocos de confiança) | `%%V_COR_PRIMARIA%%` |
| Acento (CTA, destaques) | `%%V_COR_ACENTO%%` |
| Texto | `%%V_COR_TEXTO%%` |
| Fundo da página | `%%V_COR_FUNDO%%` |
| Fundo suave (blocos de lista) | `%%V_COR_SUAVE%%` |
| Footer | `%%V_COR_ESCURA%%` |

Fonte: `%%V_FONTE%%` — sempre com fallback; nunca depender de fonte de marca para legibilidade.

## Logos

- Fundo escuro: `%%V_LOGO_FUNDO_ESCURO%%`
- TODO(criador): logo para fundo claro (se usada) e regra de uso de cada versão.

Logos e imagens no e-mail sempre por URL HTTPS pública; arquivos locais servem só para preview.

## Direção visual

TODO(criador): 3–5 bullets do que a marca comunica visualmente e o que evitar (do manual de marca ou do site).

## Compatibilidade de e-mail (obrigatório)

- Layout em tabelas (`<table role="presentation">`), largura máxima 620 px, CSS inline.
- Nunca `display:flex`, `grid`, `linear-gradient`, `rgba()`, JavaScript, `<div>` como wrapper externo, imagem em base64 ou caminho local.
- Sempre `bgcolor` além de `background-color` nos `<td>` coloridos; cores sólidas pré-calculadas no lugar de transparência.
- Declarar a família de fonte com fallback em cada bloco de texto.
- `alt` em toda imagem.
- Emojis e símbolos como entidades HTML (`&#8594;` →, `&#9889;` ⚡).
- HTML completo de `<!doctype html>` a `</html>`, com `xmlns:v`/`xmlns:o` e meta `x-apple-disable-message-reformatting`.
- Manter o HTML abaixo de ~100 KB (o Gmail corta mensagens maiores).
