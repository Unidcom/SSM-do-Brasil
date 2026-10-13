---
name: criador-skill-newsletter
description: Cria, para um projeto/cliente, uma skill completa de newsletter recorrente (no molde de newsletter-vesper e newsletter-unidcom) — briefing do cliente, desenho das seções e de como cada uma puxa conteúdo (curadoria de notícias, rotação de cases/produtos, alternância por calendário, conteúdo fixado de campanha, dados ao vivo, blocos fixos), template HTML de e-mail, scripts de rotação/validação, publicação para aprovação no repositório aprovacoes-unid e criação do rascunho direto pela API da plataforma (Brevo, MailerLite Classic). Use quando o usuário pedir para "criar a skill de newsletter" de um cliente, montar uma nova newsletter automatizada para um projeto, adaptar a newsletter de um cliente para outro, ou adicionar/alterar seções de uma skill de newsletter já gerada.
---

# Criador de skill de newsletter

Esta skill **não gera uma edição de newsletter**. Ela gera a *skill* que, depois, gera as edições de um projeto — como `newsletter-vesper` e `newsletter-unidcom` foram feitas à mão.

Modelo mental: **toda newsletter é uma lista ordenada de seções, e cada seção tem um tipo que define de onde ela puxa conteúdo, quando seu estado avança e o que fazer se falhar.** O resto (data, pasta da edição, HTML de e-mail, validação, publicação para aprovação, rascunho na plataforma) é infraestrutura comum que a skill gerada herda pronta.

Fluxo de toda skill gerada, no fim: **edição salva e validada → publicada em `aprovacoes-unid/<cliente>/` (link do GitHub Pages) → aprovação → rascunho criado direto pela API da plataforma → rotação confirmada.** A skill gerada nunca envia, agenda nem dispara teste: o disparo aos contatos é manual, no painel.

Toda a especificação da newsletter fica num único arquivo: `config/newsletter.json` dentro da skill gerada. Scripts leem esse arquivo; o `SKILL.md` gerado o descreve em prosa.

## Referências desta skill

Ler sob demanda, na fase indicada:

| Arquivo | Quando |
|---|---|
| `references/briefing-modelo.md` | Fase 1 — roteiro de levantamento e modelo do documento de briefing |
| `references/tipos-de-secao.md` | Fase 2 — catálogo dos tipos de seção, campos e comportamento |
| `references/config-newsletter.md` | Fase 2–4 — schema completo de `config/newsletter.json` |
| `references/email-html.md` | Fase 3 — regras de HTML de e-mail e convenção de placeholders |
| `references/modulos/*.md` | Fase 4 — Brevo (API), MailerLite Classic (API), MailerLite atual (API), aprovação em aprovacoes-unid |
| `references/regras-universais.md` | Fase 5 — regras que toda skill gerada precisa conter |
| `references/estrutura-skill-gerada.md` | Fase 5 — árvore de arquivos e o que cada um contém |

Exemplos completos de config: `assets/exemplos/vesper.newsletter.json` e `assets/exemplos/unidcom.newsletter.json` — a mesma ferramenta descrevendo as duas newsletters existentes. Usá-los como referência de preenchimento.

## Fluxo

As fases podem ser feitas em uma ou várias conversas. Ao retomar, ler o briefing e o `config/newsletter.json` já existentes antes de perguntar de novo.

### Fase 0 — Localizar o projeto

1. Confirmar o repositório do projeto e o slug (`newsletter-<slug>`; slug minúsculo, sem acento).
2. Verificar se já existe `.agents/skills/newsletter-<slug>/`. Se existir:
   - Buscar `TODO(criador)` em toda a pasta da skill (Grep). **Se houver algum, a criação ficou incompleta numa conversa anterior:** listar ao usuário o que falta, agrupado por arquivo, e retomar a Fase 5, passo 2, preenchendo cada lacuna junto com ele (a partir do briefing; o que o briefing não responde, perguntar).
   - Se não houver, é um trabalho de **alteração**: ler o `SKILL.md` e o `config/newsletter.json` atuais e ir direto à fase afetada.
3. Destino padrão da skill gerada: `<projeto>/.agents/skills/newsletter-<slug>/` (padrão das skills existentes, com `agents/openai.yaml`). Se o projeto usar outro local, seguir o do projeto.

### Fase 1 — Briefing

Ler `references/briefing-modelo.md`.

1. Pesquisar o que for público (site, blog, redes, páginas de oferta) e pré-preencher o briefing — nunca perguntar ao usuário o que o site já responde.
2. Salvar em `<projeto>/docs/briefing-newsletter-<slug>.md`, marcando com **Precisa de confirmação** tudo que estiver divergente ou não verificado.
3. Fazer ao usuário apenas as perguntas prioritárias que faltam (frequência, público, seções, plataforma, aprovação), em lote, com sugestão de resposta para cada uma.
4. Registrar as respostas na seção “Decisões confirmadas em AAAA-MM-DD” do briefing.

Não avançar para a Fase 5 com pendências que bloqueiam o envio (plataforma, identidade visual, CTA principal) sem dizer ao usuário que a skill sairá com essas lacunas marcadas.

### Fase 2 — Desenho das seções

Ler `references/tipos-de-secao.md` e `references/config-newsletter.md`.

Para **cada seção** do e-mail, em ordem de aparição, definir com o usuário:

- tipo (`curadoria-externa`, `rotacao-catalogo`, `pool-sem-repeticao`, `alternancia`, `calendario`, `fixado`, `dados-ao-vivo`, `bloco-fixo`, `editorial`);
- de onde puxa (fontes, catálogo, regra, URL);
- quantidade e formato de cada item (campos, contagem de palavras);
- quando o estado avança (sempre: só depois que o rascunho existir na plataforma, com `campaign_id`);
- o que fazer se falhar (parar, usar fallback declarado, omitir a seção).

Apresentar o resultado como uma tabela de seções (id · tipo · como puxa · quantidade · avança quando · se falhar) para aprovação **antes** de gerar arquivos. Esse é o ponto central da skill: o usuário precisa enxergar como cada seção é alimentada.

### Fase 3 — Identidade visual e template

Ler `references/email-html.md`.

1. Coletar logo (URL HTTPS pública — e-mail não aceita caminho local), paleta, fonte e rodapé legal.
2. Partir de `assets/email/base.html` e dos parciais em `assets/email/partials/`; adaptar cores, header e footer à marca. Se o cliente já tem um template aprovado, usá-lo como base e só converter os campos variáveis em placeholders `{{SLOT}}`.
3. Um slot por seção, com o mesmo nome declarado em `slot` no config.
4. Gerar também o modelo de plain text.

### Fase 4 — Plataforma e aprovação

**Plataforma de e-mail.** Identificar qual o cliente usa e ler o módulo correspondente em `references/modulos/`:

| Plataforma | `plataforma.tipo` | Módulo |
|---|---|---|
| Brevo | `brevo` | `brevo.md` |
| MailerLite Classic | `mailerlite-classic` | `mailerlite-classic.md` |
| MailerLite (atual, connect) | `mailerlite` | `mailerlite.md` — HTML via API exige plano Advanced |
| outra | — | pesquisar a API e escrever um adaptador novo em `assets/skill-base/scripts/create_draft.py` (contrato: só rascunho, devolve `campaign_id` numérico, grava a resposta) e registrá-lo em `PLATFORMS` no `scaffold_skill.py` |

Registrar no config: `plataforma.tipo`, variáveis de sistema obrigatórias (ver no navegador, descadastro), textos proibidos e `nome_campanha`. Credenciais vão **só** em `private/<plataforma>.env` na raiz do projeto (o scaffold gera o modelo `config/<plataforma>.env.exemplo` e põe `private/` no `.gitignore`). Avisar o usuário quais chaves ele precisa preencher — nunca pedir que cole a chave na conversa.

**Aprovação.** Ler `references/modulos/aprovacao.md`. Definir `aprovacao_repo.pasta` (pasta do cliente em `aprovacoes-unid`, normalmente o slug) e a política `aprovacao` (`sempre` ou `dispensada-quando-solicitada-ou-agendada`). Confirmar que `aprovacoes-unid` está clonado no caminho de `aprovacao_repo.local` (padrão: pasta irmã do projeto).

### Fase 5 — Gerar a skill

1. Salvar o config aprovado em um arquivo temporário e rodar o scaffold:

```powershell
python .claude/skills/criador-skill-newsletter/scripts/scaffold_skill.py --config <config.json> --project-root <projeto>
```

O script cria a árvore, copia scripts e parciais, gera stubs de catálogo para cada seção com catálogo e escreve um `SKILL.md` rascunho montado a partir dos passos de cada tipo de seção (`assets/passos/<tipo>.md`). Sem flag, não sobrescreve nada que já exista.

2. Completar junto com o usuário o que o scaffold só esboça (marcado com `TODO(criador)`):
   - `references/empresa-e-ofertas.md`, `curadoria-editorial.md`, `identidade-visual.md` a partir do briefing;
   - modelos HTML de cada item de catálogo e o `catalog.json` real;
   - `assets/template.html` final;
   - o parágrafo de propósito no topo do `SKILL.md`.
3. Garantir que todas as regras de `references/regras-universais.md` estão no `SKILL.md` gerado.
4. Nenhum `TODO(criador)` pode sobrar. Conferir com Grep.

### Fase 6 — Validar com uma edição de teste

1. Rodar `scripts/rotation.py select` da skill gerada e conferir a seleção de cada seção com estado.
2. Rodar `scripts/fetch_live_data.py` se houver seção `dados-ao-vivo`.
3. Gerar uma edição de teste seguindo o `SKILL.md` gerado, salvar na pasta de edições com sufixo `-teste` e rodar `scripts/validate_edition.py --sync`.
4. Rodar `create_draft.py create <edição> --dry-run` para conferir o corpo que iria para a API (sem chamada).
5. Mostrar o preview ao usuário. Só publicar a edição de teste em `aprovacoes-unid` ou criar um rascunho real se ele pedir — e nunca avançar a rotação numa edição de teste.
6. Apagar ou manter a edição de teste conforme o usuário preferir.

### Fase 7 — Entrega

Informar: caminho da skill, tabela final de seções, pendências abertas (do briefing e externas: `private/<plataforma>.env` a preencher, `aprovacoes-unid` a clonar), e como disparar (`$newsletter-<slug>` / pedido em linguagem natural; agendamento via skill `schedule` se desejado).

## Alterar uma skill já gerada

- **Melhorias nos scripts do criador:** `scaffold_skill.py --config <skill>/config/newsletter.json --project-root <projeto> --force` atualiza só a infraestrutura (scripts, parciais, config e referências técnicas de API/aprovação). Conteúdo preenchido nunca é tocado.
- **Regenerar arquivos ainda incompletos:** `--force-all` regenera também SKILL.md, template, referências de conteúdo, catálogos e modelos — **só os que ainda contêm `TODO(criador)`**. Arquivos já preenchidos são sempre preservados (o relatório lista o que foi preservado).
- **Nova seção ou mudança de tipo:** editar `config/newsletter.json`, o slot no template, o passo correspondente no `SKILL.md` e, se tiver catálogo, criá-lo. Validar com `scaffold_skill.py --config ... --check`.
- **Campanha temporária** (ex.: isca fixada por algumas semanas): usar uma seção `fixado` com `ate` e `senao`, em vez de reescrever a rotação — quando a data passar, a rotação original volta sozinha.
- Nunca editar o arquivo de estado de rotação à mão para "pular" um item; usar `rotation.py mark-used` ou desativar o item no catálogo (`"ativo": false`).

## Regras desta skill

- Não inventar dados do cliente (números, prazos, financiamento, resultados). O que não for confirmado vai para o briefing como pendência.
- A skill gerada deve ser autocontida: tudo que a execução precisa está nela, sem depender de outras skills durante a geração da edição.
- Toda decisão do usuário vira texto em um arquivo da skill gerada ou do briefing — nada fica só na conversa.
