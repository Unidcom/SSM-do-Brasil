# Montar HTML e plain text

1. Partir de `assets/template.html` — estrutura, cores, espaçamentos e ordem são fixos. Substituir **somente** os placeholders `{{MAIÚSCULAS}}`; parciais em `assets/partials/`.
2. Preservar literalmente as variáveis de sistema da plataforma: %%VARS_HTML%%. Elas não são placeholders editoriais e só viram links válidos no processamento da plataforma.%%PROIBIDO%%
3. Regras de compatibilidade e identidade: `references/identidade-visual.md`. Nunca `display:flex`, `grid`, `linear-gradient`, `rgba()`, JavaScript, imagem em base64 ou caminho local.
4. Plain text a partir de `assets/plain-text-template.txt`, com as variáveis %%VARS_TEXTO%%.
