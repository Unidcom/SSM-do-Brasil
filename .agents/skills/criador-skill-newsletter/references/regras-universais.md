# Regras universais das skills geradas

Extraídas das duas newsletters em produção (Vésper e Unidcom) e das decisões de arquitetura do criador. O scaffold insere todas no `SKILL.md` gerado (`assets/passos/regras.md`) e nos passos do fluxo. Ao revisar uma skill gerada, conferir que nenhuma foi removida.

| Regra | Por quê (incidente ou risco que evita) |
|---|---|
| Skill com `TODO(criador)` não gera edição | uma lacuna não preenchida iria para o e-mail ou deixaria a seção sem regra |
| Toda URL vem de uma página aberta na execução e passa por `check_links.py` com `--esperado` | link deduzido pelo nome do evento caiu em domínio inexistente e em evento homônimo de outro setor (teste SP<, 2026-10-02) |
| Confirmar a data real da execução no fuso do cliente | agendamentos atrasam; a data do cron não é a data da edição |
| Isolamento: a execução usa só a própria skill | outras skills mudam tom/estrutura e tornam a automação não reprodutível |
| Não inventar dados; catálogo e dados ao vivo usados como vieram | promessas comerciais e números errados chegam a milhares de contatos |
| Reescrever, não traduzir | tradução literal de fonte estrangeira soa artificial e importa regra que não vale no Brasil |
| Quantidades exatas por seção; faltou material → parar | edição "incompleta" quebra o layout aprovado |
| Publicar em `aprovacoes-unid` antes de qualquer chamada à plataforma | quem aprova vê exatamente o HTML que vai virar campanha |
| Só rascunho: a skill nunca envia, agenda ou dispara teste | o disparo para a base é irreversível e fica sob controle humano |
| Selecionar não grava; rotação só avança com o `campaign_id` | se a criação falhar, o item não pode ser dado como usado |
| Uma chamada à API por execução; nunca repetir sozinho | repetir o `create` cria campanhas duplicadas |
| Campanha já criada → retomar com `update`, nunca outro `create` | o script grava o ID antes do conteúdo justamente para isso |
| Artefatos salvos no projeto (`newsletter.html`, `plain-text.txt`, `payload.json`, `metadata.md`) | auditoria, aprovação e retomada dependem deles |
| Variáveis da plataforma literais no HTML | trocar `{{ mirror }}` por URL fixa quebra o espelho individual |
| Cópia de aprovação sem variáveis da plataforma | o descadastro é individual; publicá-lo exporia o link de outra pessoa |
| UTF-8 sem BOM; validar mojibake | PowerShell 5.1 grava em ANSI por padrão e corrompe acentos |
| Credenciais só em `private/<plataforma>.env` (ignorado pelo Git) | os repositórios e logs são compartilhados |
