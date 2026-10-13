# Publicar para aprovação e aprovar

Detalhes em `references/aprovacao.md`.

```powershell
python %%SKILL_REL%%/scripts/publish_approval.py %%PASTA%%/AAAA-MM-DD
```

- Gera a cópia de aprovação sem as variáveis da plataforma, grava em `aprovacoes-unid/%%APROV_PASTA%%/%%APROV_ARQUIVO%%`, faz commit e push **só desse arquivo** e espera o link responder HTTP 200.
- Link: `%%APROV_BASE%%/%%APROV_PASTA%%/%%APROV_ARQUIVO%%`. O script grava em `payload.json → link_aprovacao`; registrar também em `metadata.md`.
- Se o script falhar (repositório não clonado, push recusado, link fora do ar): registrar e parar. Não criar rascunho na plataforma sem link de aprovação.

**Aprovação:** %%REGRA_APROVACAO%%

Mostrar o link de aprovação junto com o assunto, o pré-header e o resumo das seções (item escolhido em cada uma). Um pedido de "rascunho" ou "preview" nunca autoriza criar a campanha na plataforma. Se o usuário pedir ajustes, corrigir o HTML, rodar `validate_edition.py --sync` e publicar de novo — o arquivo é substituído no mesmo link.
