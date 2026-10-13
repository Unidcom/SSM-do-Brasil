# Radar Estrutural SSM — 2026-10-14 (EDIÇÃO DE TESTE)

**Status: rascunho na Brevo**

## Dados da edição

- **Data:** Quarta-feira, 14 de outubro de 2026
- **Assunto:** Tarifa, bandeira verde e 92 GW: o que muda para a sua obra
- **Pré-header:** STF barra ICMS sobre subsídio, conta de luz pressiona IPCA e GD deve dobrar até 2036.
- **Nome da campanha:** Radar Estrutural SSM — 2026-10-14

## Itens das seções

### Radar do setor — janela 7 dias (2026-10-07 a 2026-10-14) — sem exceção de janela

Fontes verificadas nesta edição: Canal Solar, Fotovolt/Aranda, Giro ABSOLAR, Energy Channel, Folha, Exame + complementares (pv magazine Brasil, ONS).

**Destaques (3):**

1. **Regulação** — STF afasta cobrança de ICMS sobre subsídio de energia de baixa renda (Canal Solar, 13/10/2026). https://canalsolar.com.br/stf-icms-subsidio-energia-baixa-renda/
2. **Mercado** — Negociações de energia ganham força com queda dos preços futuros: 22 TWh negociados na BBCE em setembro, alta de 9,2% (Canal Solar, 10/10/2026). https://canalsolar.com.br/negociacoes-energia-queda-precos-futuros/
3. **Geração distribuída** — MMGD deve alcançar 91,7 GW até 2036, segundo PDE 2036 (EPE): +41,4 GW e R$ 96 bilhões em investimentos entre 2027 e 2036, puxados pela solar (pv magazine Brasil, 09/10/2026). https://www.pv-magazine-brasil.com/2026/10/09/mmgd-deve-alcancar-92-gw-de-capacidade-instalada-no-brasil-ate-2036/

**Giro rápido (5):**

1. Conta de luz pressiona IPCA: alta de 7,98% em setembro foi o maior impacto individual na inflação (Canal Solar, 09/10/2026). https://canalsolar.com.br/conta-de-luz-inflacao-setembro-ipca/
2. Outubro volta à bandeira verde após dois anos de bandeira vermelha em 2024 e 2025 (Canal Solar, 09/10/2026). https://canalsolar.com.br/bandeira-verde-outubro-apos-dois-anos-vermelha/
3. ABRATE avalia que a primeira etapa da PNAST fortalece o acesso à transmissão (Canal Solar, 09/10/2026). https://canalsolar.com.br/abrate-avalia-pnast-transmissao/
4. Maior carport solar da Califórnia é inaugurado em parque de diversões (Fotovolt/Aranda, 09/10/2026). https://www.arandanet.com.br/revista/fotovolt/noticia/13741-Parque-de-diversoes-inaugura-maior-carport-solar-da-California.html
5. Compensação por cortes de geração: sai a lista de elegibilidade (Fotovolt/Aranda, 09/10/2026). https://www.arandanet.com.br/revista/fotovolt/noticia/13740-Compensacao-por-cortes-de-geracao:-sai-a-lista-de-elegibilidade.html

### Do blog da SSM (pool-sem-repeticao) — item: `o-que-e-carport-solar`

Motivo: primeiro ativo fora dos últimos 10 usados (histórico vazio).

### Solução em destaque (rotacao-catalogo) — item: `carport`

Motivo: primeiro ativo, ordem circular (sem histórico).

## Seleção (registro para rotation.py)

- blog-ssm → o-que-e-carport-solar
- solucao-destaque → carport

## Rotação

Rotação avançada: **não** (edição de teste — nunca avança estado).

## Validação Brevo (2026-10-13)

- campaign_id: **81** · painel: https://app.brevo.com/marketing-campaign/edit/81
- Link de aprovação: https://unidcom.github.io/aprovacoes-unid/ssm/newsletter-2026-10-14-teste.html
- Acesso validado de ponta a ponta (publicação → rascunho). Sem MCP: API v3 direta via scripts (whitelist de IP ativa na conta).

## Ajustes 2026-10-13 (2ª rodada)

- Layout: 'Solução em destaque' movida para DENTRO do bloco de notícias — agora fica entre os 3 destaques e o Giro rápido, em faixa escura #052B4D (mesma cor do CTA 'Pronto para o seu próximo projeto?'), com card branco, título branco e texto claro.
- Base de destino atualizada para a BASE INTEIRA: listas 21, 5, 4, 22, 12 (~1.779 contatos). Fora: Equipes SSM (15, 14) e listas sistêmicas (8, 7).
- Campanha Brevo 81 atualizada (update) com o novo HTML e destinatários — confirmado na API: recipients.lists = [21,5,4,22,12].

- Correção de legibilidade (2026-10-13): no card da 'Solução em destaque', título e corpo voltaram a escuro (#0A1A24 / #2F3A45) sobre o card branco; o faixo escuro #052B4D fica no fundo da seção. Rótulo 'SOLUÇÃO EM DESTAQUE' permanece ciano sobre o azul-marinho. Campanha 81 atualizada.

- Imagem do card 'Solução em destaque' restaurada (havia sido perdida na correção de cores). Campanha 81 atualizada com HTML final.
