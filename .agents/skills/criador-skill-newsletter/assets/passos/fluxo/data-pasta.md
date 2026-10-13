# Confirmar data e pasta da edição

1. Confirmar a data real da execução no fuso `%%FUSO%%` (ex.: `Get-Date` / `date`). Nunca presumir a data pelo agendamento nem reaproveitar a de outra edição.
2. Formato por extenso para o e-mail: `Quarta-feira, 5 de agosto de 2026`.
3. Pasta da edição: `%%PASTA%%/AAAA-MM-DD/`. Se já existir, preservar e criar `%%PASTA%%/AAAA-MM-DD-2/` (sufixo incremental). Edições de teste usam o sufixo `-teste` e nunca são publicadas.
