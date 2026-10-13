# `config/newsletter.json` — schema

Arquivo único de especificação da skill gerada. Fica em `.agents/skills/newsletter-<slug>/config/newsletter.json`, em UTF-8 sem BOM. Todos os scripts da skill gerada leem daqui. Caminhos são relativos à **raiz do projeto**, exceto `catalogo`, `modelo` e `parcial`, que são relativos à **pasta da skill**.

Validar a qualquer momento com:

```powershell
python .claude/skills/criador-skill-newsletter/scripts/scaffold_skill.py --config <arquivo> --check
```

Exemplos completos: `assets/exemplos/vesper.newsletter.json` (Brevo) e `assets/exemplos/unidcom.newsletter.json` (MailerLite Classic).

## Raiz

| Campo | Tipo | Exemplo | Descrição |
|---|---|---|---|
| `versao` | int | `1` | versão do schema |
| `slug` | str | `vesper` | nome da skill = `newsletter-<slug>` |
| `nome` | str | `Newsletter Vésper` | nome de exibição |
| `empresa` | str | `Vésper Energia Solar` | nome oficial |
| `cor_marca` | str | `#4070A2` | usado no `agents/openai.yaml` |
| `fuso` | str | `America/Sao_Paulo` | fuso da data da edição |
| `agenda` | obj | `{"dias":["qua"],"hora":"09:00"}` | referência; o agendamento real é feito à parte |
| `edicoes.pasta` | str | `newsletter` | pasta das edições na raiz do projeto |
| `verificar_links` | bool | `false` | **recomendado `true`**: o validador exige `links-report.json` aprovado (gerado por `scripts/check_links.py`) e do mesmo HTML |
| `vocabulario` | obj | — | ênfase de termos pedida pelo cliente: `{"priorizar": [...], "secundario": [...], "ignorar": [...]}`. O validador recusa a edição se os termos de `priorizar` (radicais, sem acento) não aparecerem mais vezes que os de `secundario` no texto visível; `ignorar` remove expressões antes de contar (ex.: o nome da marca) |
| `edicoes.subpastas` | str | — | subpastas por data dentro de `edicoes.pasta`, ex.: `{AAAA}/{MM}` → `Newsletter/2026/10/2026-10-06/`; os scripts aceitam só `2026-10-06` como argumento |
| `estado` | str | `newsletter/.rotation-state.json` | arquivo de estado das seções com rotação |
| `assunto_max` | int | `70` | limite de caracteres do assunto |
| `nome_campanha` | str | `Radar Vésper — {AAAA-MM-DD}` | nome interno da campanha na plataforma; aceita `{AAAA-MM-DD}` e `{DD/MM/AAAA}` |
| `aprovacao` | str | `sempre` \| `dispensada-quando-solicitada-ou-agendada` | se a skill espera o OK do usuário antes de criar o rascunho |
| `aprovacao_repo` | obj | ver abaixo | publicação em `aprovacoes-unid` |
| `visual` | obj | ver `estrutura-skill-gerada.md` | cores, fonte e logo usados pelo scaffold no template |
| `rodape` | obj | ver `estrutura-skill-gerada.md` | linhas de contato, site e motivo de recebimento |
| `plataforma` | obj | ver abaixo | plataforma de e-mail |
| `secoes` | list | ver `tipos-de-secao.md` | seções em ordem de aparição |

## `aprovacao_repo`

| Campo | Padrão | Descrição |
|---|---|---|
| `local` | `../aprovacoes-unid` | clone local do repositório (relativo à raiz do projeto ou absoluto) |
| `pasta` | — (obrigatório) | pasta do cliente dentro do repositório, ex.: `vesper` |
| `base_url` | `https://unidcom.github.io/aprovacoes-unid` | URL do GitHub Pages do repositório |
| `nome_arquivo` | `newsletter-{AAAA-MM-DD}.html` | nome do material; edições com sufixo (`-2`, `-teste`) ganham o sufixo no nome |

Link final: `<base_url>/<pasta>/<nome_arquivo>`.

## `plataforma`

| Campo | Descrição |
|---|---|
| `tipo` | `brevo`, `mailerlite-classic` ou `mailerlite` (outra exige adaptador novo em `create_draft.py`) |
| `credenciais` | caminho do `.env`, padrão `private/<tipo>.env` (relativo à raiz do projeto) |
| `variaveis_html` | variáveis de sistema que **devem** existir literalmente no HTML (Brevo: `{{ mirror }}`, `{{ unsubscribe }}`; MailerLite: `{$url}`, `{$unsubscribe}`) |
| `variaveis_texto` | idem, no plain text |
| `variaveis_espelho` | quais delas são "ver no navegador" (na cópia de aprovação apontam para a própria página) |
| `variaveis_descadastro` | quais são descadastro (somem da cópia de aprovação) |
| `proibido` | textos que nunca podem aparecer (ex.: `{$name` no MailerLite) |

Credenciais **nunca** aparecem no config — só no `.env` (chaves em `references/modulos/<plataforma>.md`).

## `payload.json` (formato fixo)

Montado por `validate_edition.py --sync`, igual para qualquer plataforma:

```json
{"nome_campanha": "Radar Vésper — 2026-10-07", "assunto": "...", "pre_header": "...",
 "html": "<!doctype html>...", "texto": "...", "link_aprovacao": "https://unidcom.github.io/aprovacoes-unid/vesper/newsletter-2026-10-07.html"}
```

`link_aprovacao` é preenchido por `publish_approval.py`. Remetente e listas não ficam no payload — vêm do `.env` na hora de criar o rascunho.

## `secoes[]`

Ver `tipos-de-secao.md` para os campos de cada tipo. Restrições validadas pelo `--check`:

- `id` único; `slot` único (exceto `bloco-fixo`/`editorial` sem slot e `curadoria-externa`, cujos slots ficam nos blocos);
- tipo conhecido;
- `fixado.senao` não pode ser outro `fixado`;
- `curadoria-externa` com pelo menos uma fonte obrigatória e um bloco.

## Arquivo de estado

Gerenciado só por `rotation.py`. Formato:

```json
{
  "versao": 1,
  "secoes": {
    "cases": {"historico": [
      {"data": "2026-08-05", "item": "case-3", "grupo": null, "confirmacao": "4"}
    ]}
  }
}
```

`confirmacao` é o `campaign_id` do rascunho. O mesmo ID nunca é gravado duas vezes para a mesma seção — repetir `mark-used` com ele é idempotente.
