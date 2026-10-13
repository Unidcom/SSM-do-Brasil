Tipo `pool-sem-repeticao` — qualquer item do catálogo `%%CATALOGO%%` que não esteja entre os últimos %%JANELA_ITENS%% usados.

1. TODO(criador): se o catálogo precisa ser atualizado antes da seleção (ex.: buscar posts novos no blog e acrescentá-los ao JSON), descrever aqui como e de onde.
2. Usar o item que `rotation.py select` retornou para `%%ID%%`.
3. Montar o bloco a partir do modelo do item ou do parcial padrão e inserir em `{{%%SLOT%%}}`.
4. Não avançar o estado aqui — só no passo de confirmação.
