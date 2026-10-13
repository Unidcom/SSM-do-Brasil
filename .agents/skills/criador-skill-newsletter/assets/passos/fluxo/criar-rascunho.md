# Criar o rascunho na %%PLATAFORMA_NOME%%

Detalhes em `references/%%PLATAFORMA_REF%%`.

```powershell
python %%SKILL_REL%%/scripts/create_draft.py create %%PASTA%%/AAAA-MM-DD --dry-run   # confere o corpo, sem chamar a API
python %%SKILL_REL%%/scripts/create_draft.py create %%PASTA%%/AAAA-MM-DD
```

- Chama **direto a API** da %%PLATAFORMA_NOME%% com as credenciais de `%%CREDENCIAIS%%` (nunca imprimir nem registrar os valores).
- Cria a campanha **só em rascunho**. O script não envia, não agenda e não dispara teste: o disparo aos contatos é feito manualmente no painel.
- Exige edição válida e `link_aprovacao` preenchido. Faz **uma única tentativa** e grava `%%PLATAFORMA%%-response.json` com `campaign_id` e link do painel.
- Se a edição já tiver campanha, o `create` é recusado — para trocar o conteúdo use `update %%PASTA%%/AAAA-MM-DD --campaign-id ID`. Nunca criar uma segunda campanha para a mesma edição.
- Se o `create` falhar depois de gravar o `campaign_id` (conteúdo `pendente`), retomar com `update`, não com `create`.
- Sucesso: registrar `campaign_id` e link em `metadata.md` com `Status: rascunho na %%PLATAFORMA_NOME%%`. Falha: `Status: falhou` com a mensagem (sem segredos) e parar — sem rotação.
