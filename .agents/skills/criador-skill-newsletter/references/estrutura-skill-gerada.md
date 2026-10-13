# Estrutura da skill gerada

```text
<projeto>/
├── .agents/skills/newsletter-<slug>/
│   ├── SKILL.md                      fluxo montado a partir das seções (Passo 0…N)
│   ├── agents/openai.yaml            exibição no Codex; invocação implícita desligada
│   ├── config/
│   │   ├── newsletter.json           fonte de verdade: seções, plataforma, aprovação
│   │   └── <plataforma>.env.exemplo  chaves que vão em private/<plataforma>.env (sem valores)
│   ├── assets/
│   │   ├── template.html             e-mail com um {{SLOT}} por seção
│   │   ├── plain-text-template.txt
│   │   ├── partials/                 highlight, quick-item, catalog-card, offer-block, stats-bar
│   │   └── <secao>/catalog.json      + models/<item>.html   (seções com catálogo)
│   ├── references/
│   │   ├── empresa-e-ofertas.md      versão aprovada do briefing
│   │   ├── identidade-visual.md
│   │   ├── curadoria-editorial.md    (se houver curadoria)
│   │   ├── aprovacao.md              aprovacoes-unid: link, publicação e falhas
│   │   └── brevo.md | mailerlite-classic.md | mailerlite.md
│   └── scripts/
│       ├── _newsletter_common.py     config, raiz do projeto, data no fuso, .env, aprovação
│       ├── rotation.py               select / mark-used / status
│       ├── check_links.py            abre links/imagens, confere conteúdo esperado → links-report.json
│       ├── validate_edition.py       --sync monta o payload fixo; valida a edição
│       ├── publish_approval.py       publica em aprovacoes-unid/<cliente>/ e espera o HTTP 200
│       ├── create_draft.py           rascunho direto pela API (Brevo / MailerLite Classic)
│       └── fetch_live_data.py        (se dados ao vivo)
├── private/<plataforma>.env          credenciais — fora do Git
├── docs/briefing-newsletter-<slug>.md
└── <pasta-edicoes>/
    ├── .rotation-state.json          estado das seções com rotação (só via rotation.py)
    └── AAAA-MM-DD/
        ├── newsletter.html
        ├── plain-text.txt
        ├── payload.json              nome_campanha, assunto, pre_header, html, texto, link_aprovacao
        ├── metadata.md
        └── <plataforma>-response.json   campaign_id e link do rascunho

../aprovacoes-unid/                   repositório compartilhado, servido pelo GitHub Pages
└── <slug>/newsletter-AAAA-MM-DD.html
```

## O que o scaffold entrega pronto × o que é completado com o usuário

| Pronto | Completado (`TODO(criador)`) |
|---|---|
| scripts, parciais, referências de API e de aprovação | parágrafo de propósito no `SKILL.md` |
| `config/newsletter.json` e o modelo do `.env` | `empresa-e-ofertas.md`, direção visual, temas prioritários da curadoria |
| `SKILL.md` com regras, tabela de seções e todos os passos | modelos HTML de cada item de catálogo e de cada opção de calendário |
| template com slots na ordem do config | conteúdo real dos `catalog.json` |
| `private/` no `.gitignore` | rótulos da barra de números fixos; rodapé, se não veio no config |

Depois de completar, conferir com Grep que não restou `TODO(criador)` na skill.

## Sobrescrita

| Arquivo | sem flag | `--force` | `--force-all` |
|---|---|---|---|
| scripts, parciais, config, `.env.exemplo`, referências de API/aprovação | só cria | atualiza | atualiza |
| SKILL.md, template, empresa/identidade/curadoria, catálogos, modelos | só cria | preserva | regenera **só se ainda tiver `TODO(criador)`** |

## Campos visuais do config (usados só pelo scaffold)

```json
"visual": {
  "cor_primaria": "#4070A2", "cor_acento": "#DF9937", "cor_texto": "#263442",
  "cor_fundo": "#F3F6F9", "cor_suave": "#EEF5FC", "cor_escura": "#1D2935",
  "fonte": "Montserrat,Arial,sans-serif",
  "logo_fundo_escuro": "https://.../logo-branco.png"
},
"rodape": {
  "linhas": ["Rua Exemplo, 100 — Cidade/UF", "contato@empresa.com · (00) 00000-0000"],
  "site": "https://www.empresa.com/",
  "motivo": "Você recebeu este e-mail por fazer parte da base de relacionamento da Empresa."
}
```
