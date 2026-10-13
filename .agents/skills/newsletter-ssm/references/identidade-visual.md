# Identidade visual — SSM do Brasil

`assets/template.html` é a fonte executável deste padrão: estrutura, cores, espaçamentos e ordem das seções não mudam entre edições.

Paleta e tipografia **medidas diretamente no site oficial** (home, 2026-10-13), para o e-mail falar a mesma língua visual da marca.

## Paleta usada no template

| Papel | Cor | Onde aparece no site |
|---|---|---|
| Primária (header, faixa de números) | `#00539C` | hero e seções institucionais |
| Acento (rótulos de seção, CTAs, links) | `#01B5E1` | eyebrows, botões e links do site |
| Título sobre fundo claro | `#0A1A24` | h2 das seções brancas |
| Texto corrido | `#2F3A45` | parágrafos do site |
| Fundo da página | `#041E36` | rodapé do site (a moldura externa do e-mail é escura) |
| Fundo suave (giro rápido) | `#EEF4F9` | derivada da paleta |
| Bloco CTA escuro | `#052B4D` | seção "Pronto para o seu próximo projeto?" do site |
| Texto claro sobre ciano/escuro | `#0A1A24` / `#FFFFFF` | botões do site usam texto escuro sobre ciano |

Fonte: **corpo em `Inter,Arial,sans-serif`** (fonte do site); **títulos em `'Fira Sans Condensed','Arial Narrow',Arial,sans-serif`** (fonte condensada dos títulos do site, com fallback estreito para clientes sem web font). Sempre com fallback; nunca depender de fonte de marca para legibilidade.

Padrões do site replicados no template: rótulos de seção em caixa alta, ciano, 500, letter-spacing 1px; botões retos (sem border-radius), peso 600, texto escuro sobre ciano; faixas em azul sólido com texto branco.

## Logos

- Fundo escuro (header e footer do template): `https://ssmdobrasil.com.br/wp-content/uploads/elementor/thumbs/logo-white-rosghll1m2nqrkzjnxg2jk005mo5tji97hmpeo6uio.png` — logo branco, extraído do site oficial.
- Logo para fundo claro: não confirmado — o template usa logo branco apenas sobre fundos escuros (header azul `#00539C` e footer `#041E36`). Se um dia um bloco de fundo claro precisar de marca, buscar logo colorido aprovado antes.

Logos e imagens no e-mail sempre por URL HTTPS pública; arquivos locais servem só para preview.

## Direção visual

- Industrial e precisa: azul profundo (`#00539C`) como autoridade técnica, ciano (`#01B5E1`) como acento de energia — no site, o ciano é usado em pontos pequenos (rótulos, botões), nunca como cor dominante.
- Cantos retos em botões e cards (o site não usa border-radius) — a estética é de indústria, não de app.
- Botões ciano com **texto escuro** (`#0A1A24`), peso 600 — replicar exatamente; botão azul-escuro com texto branco também existe no site para CTAs em fundo claro.
- Títulos em fonte condensada (Fira Sans Condensed no site), peso 700, cor `#0A1A24` sobre claro e branco sobre escuro.
- Imagens de obra/estrutura reais sempre que possível (catálogos usam imagens do site oficial da SSM); nada de banco de imagens genérico.
- Evitar: gradientes, cantos arredondados, excesso de cores por bloco, ciano em áreas grandes de fundo.
- Ícones e setas como entidades HTML (`&#8594;`), nunca imagem.

## Compatibilidade de e-mail (obrigatório)

- Layout em tabelas (`<table role="presentation">`), largura máxima 620 px, CSS inline.
- Nunca `display:flex`, `grid`, `linear-gradient`, `rgba()`, JavaScript, `<div>` como wrapper externo, imagem em base64 ou caminho local.
- Sempre `bgcolor` além de `background-color` nos `<td>` coloridos; cores sólidas pré-calculadas no lugar de transparência.
- Declarar a família de fonte com fallback em cada bloco de texto.
- `alt` em toda imagem.
- Emojis e símbolos como entidades HTML (`&#8594;` →, `&#9889;` ⚡).
- HTML completo de `<!doctype html>` a `</html>`, com `xmlns:v`/`xmlns:o` e meta `x-apple-disable-message-reformatting`.
- Manter o HTML abaixo de ~100 KB (o Gmail corta mensagens maiores).
