# Salvar artefatos e validar

Salvar **dentro do projeto**, na pasta da edição:

- `newsletter.html` — HTML completo, autossuficiente;
- `plain-text.txt`;
- `metadata.md` — começa com `Status: rascunho local`; registra data, assunto, itens de cada seção (com fontes das notícias), valores ao vivo, exceções de janela e, depois, IDs/links externos;
- `payload.json` — montado pelo validador, em formato fixo: `nome_campanha`, `assunto`, `pre_header`, `html`, `texto`, `link_aprovacao`.

Gravar em UTF-8 sem BOM (no PowerShell, nunca `Set-Content` sem `-Encoding utf8`; preferir a ferramenta de escrita de arquivos).

**Verificar links e imagens** antes de validar (e de novo a cada alteração do HTML):

```powershell
python %%SKILL_REL%%/scripts/check_links.py %%PASTA%%/AAAA-MM-DD --esperado "<URL>=<nome do evento/item>" ...
```

- Abre cada link e imagem do HTML e grava `links-report.json`. Erro: domínio inexistente, HTTP 4xx/5xx, domínio à venda, imagem que não é imagem, página que não menciona o texto `--esperado`.
- Passar `--esperado` para **todo link de conteúdo externo** (notícia, evento): `URL=nome do evento` ou `URL=trecho do título da matéria`. Isso prova que o link é da coisa certa, não só que abre.
- Erro → trocar o link pelo correto (achado na fonte original ou no site oficial) e rodar de novo. Nunca deduzir uma URL pelo nome do evento/site — toda URL vem de uma página aberta nesta execução.
- Aviso de redirecionamento → trocar pela URL final. Aviso de bloqueio (401/403/429) → abrir a página por outro meio (WebFetch/navegador), confirmar e registrar em `metadata.md`.

```powershell
python %%SKILL_REL%%/scripts/validate_edition.py %%PASTA%%/AAAA-MM-DD --sync --assunto "<assunto>" --pre-header "<pré-header>"
```

Com `verificar_links: true` no config, o validador recusa a edição sem `links-report.json` aprovado e do mesmo HTML.

`--sync` grava nome da campanha (`%%NOME_CAMPANHA%%`), assunto, pré-header, HTML e texto no `payload.json`; depois valida placeholders esquecidos, variáveis obrigatórias, CSS proibido, imagens sem HTTPS, mojibake, tamanho do assunto e divergência entre payload e HTML. **Com qualquer erro, corrigir e validar de novo — nunca enviar.** Toda edição posterior do HTML exige novo `--sync`.

Nunca concluir uma edição sem `newsletter.html` salvo no projeto.
