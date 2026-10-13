Tipo `kit-catalogo` — um kit por edição: o próximo item principal em ordem circular + um item de cada componente **compatível com ele** (lista de compatibilidade no próprio item), escolhendo em cada componente o usado há mais tempo. Componente opcional sem item compatível fica de fora.

1. Usar o kit que `rotation.py select` retornou (item principal + `componentes`). Não trocar nenhuma peça por conta própria.
2. Montar o bloco com o parcial do kit, usando nomes, descrições e imagens **do catálogo** (sem reescrever dados). Componente omitido → remover o bloco dele do parcial.
3. Imagens: só `imagem_publica` (HTTPS, formato que o e-mail exibe). `pronto_para_envio: false` → parar.
4. Inserir em `{{%%SLOT%%}}`. Não avançar o estado aqui; no passo de confirmação usar `mark-used` com o `--componentes` que o `select` mostrou.
