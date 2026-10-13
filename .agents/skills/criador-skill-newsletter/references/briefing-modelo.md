# Briefing da newsletter — roteiro e modelo

O briefing é o documento de levantamento do cliente: tudo que se sabe, de onde veio e o que falta confirmar. Ele fica em `<projeto>/docs/briefing-newsletter-<slug>.md` e evolui por datas. A skill gerada só usa o que está **confirmado**; o resto fica como pendência.

## Como levantar

1. **Pesquisar antes de perguntar:** site institucional, páginas de produto/oferta, blog, contato, redes, LinkedIn. Pré-preencher tudo o que for público e citar a fonte (URL) no fim.
2. **Marcar divergências:** quando o site traz números diferentes em páginas diferentes (anos, clientes, prazos), registrar os dois e marcar `> **Precisa de confirmação:**`. Nunca escolher um sozinho.
3. **Perguntar em lote, com sugestão:** só o que falta, priorizado, com uma resposta sugerida em cada pergunta para o usuário só confirmar.
4. **Registrar decisões com data:** seção `## Decisões confirmadas em AAAA-MM-DD`, uma por rodada. Pendências que restarem vão para `### Pendências remanescentes`.

## Modelo

```markdown
# Briefing da newsletter <Empresa>

Levantamento iniciado em AAAA-MM-DD para criar a skill `newsletter-<slug>`.

## 1. Empresa
- Nome oficial / curto · Site · Ramo · Área de atuação · Endereço · Telefone/WhatsApp · E-mail · CNPJ
- Objetivo da newsletter (relacionamento, geração de oportunidades, retenção…)
### Descrição consolidada a partir do site
### Posicionamento percebido
### Provas e diferenciais encontrados
> **Precisa de confirmação:** …

## 2. Públicos identificados
### Decisão pendente de segmentação (base única × versões por público)

## 3. Produtos e serviços encontrados

## 4. Benefícios e argumentos encontrados
> **Regra recomendada:** dados regulatórios, percentuais e condições financeiras verificados em fonte atual a cada edição.

## 5. Tom editorial sugerido
### Temas editoriais identificados

## 6. Seções da newsletter (proposta)
| # | Seção | Tipo | Como puxa | Quantidade | Avança quando | Se falhar |
|---|---|---|---|---|---|---|

## 7. Conteúdo comercial para rotação
- Ofertas, cases, produtos, artigos do blog candidatos; CTA principal e secundários (com links)

## 8. Identidade visual
### Encontrado
### Ainda necessário (logo HTTPS claro/escuro, paleta hex, fonte, manual)

## 9. Métricas e prova social
- Remover × números fixos aprovados × fonte dinâmica (site, CRM, API)

## 10. Informações editoriais
- Frequência, dias, horário, fuso · janela das notícias · quantidades · fontes obrigatórias/proibidas · temas proibidos · limite de promoção · textos de referência de tom

## 11. Blocos fixos
- Abertura padrão · CTA permanente · rodapé jurídico · motivo de recebimento · endereço/contatos · variáveis "ver no navegador"/"descadastro"

## 12. Envio e automação
- Plataforma (Brevo, MailerLite…) · remetente verificado · listas/segmento de destino · quem preenche `private/<plataforma>.env` · aprovação: sempre × execução agendada segue direto · pasta do cliente em `aprovacoes-unid` · pasta das edições · histórico de uso

## 13. Perguntas prioritárias

## 13.1. Decisões confirmadas em AAAA-MM-DD
### Pendências remanescentes

## 14. Fontes consultadas
```

## Perguntas que quase sempre faltam

Fazer só as que o site não responde:

1. Público principal: base única ou segmentada?
2. Frequência, dias, horário.
3. Seções e quantidades (sugerir a partir das duas newsletters existentes: 3 destaques + 5 curtas + 1–2 blocos da marca).
4. Escopo da curadoria e fontes obrigatórias; janela de dias.
5. O que roda nos blocos da marca (cases, ofertas, produtos, blog) e com qual regra (ordem, alternância, calendário, campanha fixa).
6. Layout: adaptar um existente ou identidade própria? Logo, cores, fonte.
7. Métricas: quais números estão aprovados e de onde vêm.
8. Plataforma de envio, integração e critério de sucesso.
9. Aprovação: sempre para antes de criar registros externos, ou execução agendada segue direto?
10. Números oficiais que divergem no site; ofertas permanentes; o que nunca pode aparecer.
11. Remetente verificado e lista/segmento de destino na plataforma.
