Tipo `fixado` — conteúdo de campanha que sobrepõe a rotação normal%%ATE%%.

%%DETALHES%%

1. Usar o item que `rotation.py select` retornou para `%%ID%%`. Enquanto a fixação vale, é sempre o item fixado; quando expira (ou o item é desativado no catálogo), o script aplica a regra `senao` automaticamente (`"via": "senao"`).
2. Substituir o item fixado numa edição específica **só com pedido explícito do usuário**; registrar a substituição pontual em `metadata.md` e confirmar o item realmente usado no `mark-used`.
3. Inserir em `{{%%SLOT%%}}`.
