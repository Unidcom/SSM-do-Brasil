# Selecionar as seções com rotação

```powershell
python %%SKILL_REL%%/scripts/rotation.py select --date AAAA-MM-DD
```

O script lê `config/newsletter.json` e o estado em `%%ESTADO%%` e devolve, para cada seção com seleção automática, o item escolhido, o motivo, o modelo HTML e se a imagem está pronta para envio.

- **Selecionar não grava nada.** O estado só avança no passo de confirmação, depois do retorno da plataforma.
- Se alguma seção vier com `erro` (catálogo vazio, nenhum item ativo), parar e avisar.
- Registrar a seleção (seção → item, motivo) em `metadata.md`.
