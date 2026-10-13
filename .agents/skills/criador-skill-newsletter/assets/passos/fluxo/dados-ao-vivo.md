# Capturar dados ao vivo

Executar antes de qualquer redação, para falhar cedo:

```powershell
python %%SKILL_REL%%/scripts/fetch_live_data.py
```

- O script faz no máximo o número de tentativas configurado por seção e sai com código `1` se qualquer campo não puder ser confirmado.
- Se a falha for de sandbox/proxy (conexão recusada local), repetir **uma única vez** com permissão de rede. Nunca uma terceira tentativa.
- Se falhar: **parar a edição** sem preview, sem envio e sem tocar na rotação. Avisar o usuário e perguntar se ele quer fornecer os valores manualmente ou adiar.
- Nunca inventar, estimar ou reaproveitar valores de uma edição anterior.
