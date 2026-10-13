# Confirmar a rotação

Somente depois que `create_draft.py` devolver o `campaign_id`. Para cada seção com estado usada na edição:

```powershell
%%COMANDOS_MARK_USED%%
```

- `--confirmacao` é o `campaign_id` exato; o script rejeita qualquer valor não numérico e é idempotente (repetir com o mesmo ID não duplica).
- Se o item usado for diferente do selecionado (substituição pontual pedida pelo usuário), o script registra a observação.
- Registrar `Rotação avançada: sim` em `metadata.md`.
- Nunca editar o arquivo de estado à mão.
