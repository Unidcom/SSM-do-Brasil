# Aprovação em `aprovacoes-unid` — Radar Estrutural SSM

Toda edição é publicada para aprovação no repositório `aprovacoes-unid`, servido pelo GitHub Pages, **antes** de qualquer chamada à plataforma de e-mail. Cada cliente tem sua pasta:

```text
aprovacoes-unid/
├── ssm/
│   └── newsletter-AAAA-MM-DD.html
└── <outros clientes>/
```

Link de aprovação: `https://unidcom.github.io/aprovacoes-unid/ssm/newsletter-AAAA-MM-DD.html`

## Script

```powershell
python .agents/skills/newsletter-ssm/scripts/publish_approval.py newsletter/AAAA-MM-DD
```

1. Valida a edição.
2. Gera a cópia de aprovação: o link "ver no navegador" aponta para a própria página; o descadastro (individual por destinatário) é trocado por um aviso. Falha se sobrar qualquer variável da plataforma.
3. Grava no clone local (`../aprovacoes-unid`, relativo à raiz do projeto), faz `git add`/`commit` **só desse arquivo** e `git push`. Outros arquivos do repositório — inclusive de outros clientes — não são tocados.
4. Espera o link servir **a versão nova** (compara o conteúdo, não só o HTTP 200 — a versão antiga também responde 200). Se na metade do tempo (padrão 300 s) ainda não atualizou, pede um novo deploy do GitHub Pages (`gh api -X POST repos/<org>/<repo>/pages/builds`). Só então grava `link_aprovacao` no `payload.json`.
   - Incidente que motivou isso (2026-10-05): o deploy do Pages travou 30 min e expirou; o link seguia respondendo 200 com a versão anterior.

Republicar a mesma edição substitui o arquivo no mesmo link (útil depois de ajustes).

Opções de teste: `--sem-push` (commit local apenas) e `--sem-espera` (não espera o HTTP 200).

## Pré-requisitos (uma vez por máquina)

- `aprovacoes-unid` clonado em `../aprovacoes-unid` com permissão de push.
- GitHub Pages ativo no repositório (Settings → Pages → branch `main`, pasta `/(root)`).
- O repositório é público via Pages: não publicar nada que não possa ser visto por quem tiver o link.

## Falhas

- Clone ausente → o script para e diz o caminho esperado (ajustável em `aprovacao_repo.local`).
- Push recusado ou link sem HTTP 200 → registrar em `metadata.md` e parar; não criar rascunho na plataforma.
