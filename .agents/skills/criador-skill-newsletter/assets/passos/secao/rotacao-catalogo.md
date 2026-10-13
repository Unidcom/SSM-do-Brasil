Tipo `rotacao-catalogo` — um item por edição, em ordem circular, do catálogo `%%CATALOGO%%`.

1. Usar o item que `rotation.py select` retornou para `%%ID%%`. Não escolher outro por conta própria.
2. Partir do modelo HTML do item (`modelo_path`). Não alterar números, segmento ou resultados do item — eles vêm do catálogo.
3. Preview local pode usar `imagem_local`; o HTML de envio exige `imagem_publica` HTTPS (`pronto_para_envio: true`). Sem URL pública, parar antes do envio.
4. Inserir em `{{%%SLOT%%}}`. Não avançar o estado aqui — só no passo de confirmação.
