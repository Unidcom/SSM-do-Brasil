# Identidade visual — SSM do Brasil

`assets/template.html` é a fonte executável deste padrão: estrutura, cores, espaçamentos e ordem das seções não mudam entre edições. O layout de referência é o da edição `newsletter/2026-10-14-teste-v3/newsletter.html`.

Paleta e tipografia **medidas diretamente no site oficial** (home, 2026-10-13), para o e-mail falar a mesma língua visual da marca.

## Paleta usada no template

| Papel | Cor | Onde aparece |
|---|---|---|
| Primária (header, faixa de números, botões azuis) | `#00539C` | cabeçalho, números, botão "Ler a fonte"/"Conhecer a solução"/"Ler no blog" |
| Acento (rótulos, CTA, links, setas) | `#01B5E1` | eyebrows, faixa de 4 px, borda do destaque 1, botão do CTA |
| Fundo escuro | `#041E36` | barra "Ver no navegador", hero, CTA final |
| Fundo escuro de rodapé | `#052B4D` | rodapé |
| Fundo suave | `#E5F6FB` | faixa da Solução, faixa "Para a obra:", botão dos destaques compactos |
| Fundo da página (moldura externa) | `#EDF2F5` | atrás do container de 620 px |
| Borda de cards e linhas | `#D8E2E8` | cards dos destaques, Giro rápido, card do blog |
| Título sobre fundo claro | `#0A1A24` | h2 e links do Giro rápido |
| Texto corrido | `#34424E` | parágrafos sobre fundo claro |
| Texto corrido sobre escuro | `#D7E5EF` | deck do hero e texto do CTA |

Fonte: **corpo em `Inter,Arial,sans-serif`**; **títulos em `'Fira Sans Condensed','Arial Narrow',Arial,sans-serif`** (condensada, com fallback estreito para clientes sem web font — o e-mail não carrega as fontes, então o fallback é o que a maioria vê). Sempre com fallback; nunca depender de fonte de marca para legibilidade.

## Estrutura do layout (ordem fixa)

1. Barra "Dificuldade para visualizar? Ver no navegador" (`#041E36`) e faixa ciano de 4 px.
2. Header azul `#00539C`: logo branco à esquerda, data por extenso (sem ponto final) à direita.
3. **Hero** (`#041E36`): mosaico de 3 capas (uma por destaque, 210 px de altura, separadas por 3 px `#E5F6FB`), eyebrow "Radar Estrutural SSM", `<h1>` = assunto, deck e 3 takeaways numerados 01–03 em ciano.
4. **Radar do setor**: destaque 1 principal (borda-topo ciano 4 px, título 28 px, faixa `#E5F6FB` com "Para a obra:", botão azul); destaques 2 e 3 compactos (título 23 px, "Para a obra:" em negrito, botão `#E5F6FB`).
5. **Solução em destaque**: faixa `#E5F6FB`, rótulo `#00539C`, card branco com imagem, título 27 px, texto curto e botão azul.
6. **Giro rápido**: 5 linhas com borda `#D8E2E8`; o título inteiro é o link, seguido de seta ciano.
7. **Do blog da SSM**: card com imagem, kicker "Conteúdo técnico" (ciano), título 25 px, texto curto e botão azul.
8. **SSM em números**: faixa `#00539C`, 3 colunas.
9. **CTA**: faixa `#041E36`, botão ciano com texto escuro "Solicitar orçamento pelo WhatsApp →" (sem ícone de imagem).
10. **Rodapé** (`#052B4D`): logo | dados da empresa em 2 colunas, redes sociais, site, motivo do recebimento e descadastro.

## Logos

- Fundo escuro (header e rodapé): `https://ssmdobrasil.com.br/wp-content/uploads/2026/10/logotipo-branco-ssm-scaled.png` — logo branco do site oficial (155 px no header, 145 px no rodapé).
- Logo para fundo claro: não confirmado — o template usa logo branco apenas sobre fundos escuros. Se um dia um bloco de fundo claro precisar de marca, buscar logo colorido aprovado antes.

Logos e imagens no e-mail sempre por URL HTTPS pública; arquivos locais servem só para preview.

## Direção visual

- Industrial e precisa: azul profundo (`#00539C`) como autoridade técnica, ciano (`#01B5E1`) como acento de energia em pontos pequenos (rótulos, bordas, botão do CTA) — nunca como cor dominante de área grande.
- Cantos retos em botões e cards (o site não usa border-radius) — a estética é de indústria, não de app.
- Botões azuis com texto branco nos conteúdos; botão ciano com **texto escuro** (`#0A1A24`) no CTA final.
- Títulos em fonte condensada, peso 700, `#0A1A24` sobre claro e branco sobre escuro.
- Imagens de obra/estrutura reais sempre que possível (catálogos usam imagens do site oficial da SSM); capas do mosaico vêm da própria matéria ou, na falta, de imagem gerada ilustrativa; nada de banco de imagens genérico.
- Evitar: gradientes, cantos arredondados, excesso de cores por bloco, ciano em áreas grandes de fundo.
- Setas como entidades HTML (`&#8594;`), nunca imagem. Exceção do rodapé: ícones sociais PNG de `img.icons8.com` (dependência externa; se sair do ar, os links continuam funcionando pelo `alt`).

## Compatibilidade de e-mail (obrigatório)

- Layout em tabelas (`<table role="presentation">`), largura máxima 620 px, CSS inline.
- Nunca `display:flex`, `grid`, `linear-gradient`, `rgba()`, JavaScript, `<div>` como wrapper externo, imagem em base64 ou caminho local.
- Sempre `bgcolor` além de `background-color` nos `<td>` coloridos; cores sólidas pré-calculadas no lugar de transparência.
- Declarar a família de fonte com fallback em cada bloco de texto.
- `alt` em toda imagem; `width`/`height` explícitos nas capas do mosaico.
- Capas: JPG ou PNG, proporção ~207×210 (ex.: 414×420 para telas de alta densidade). `object-fit:cover` é só melhoria — Outlook desktop ignora e **não renderiza WebP**; por isso o validador avisa capa `.webp`.
- Emojis e símbolos como entidades HTML (`&#8594;` →, `&#9889;` ⚡).
- HTML completo de `<!doctype html>` a `</html>`, com `xmlns:v`/`xmlns:o` e meta `x-apple-disable-message-reformatting`.
- Manter o HTML abaixo de ~100 KB (o Gmail corta mensagens maiores).
