# Curadoria editorial — SSM do Brasil

## Escopo

Cobrir energia solar, setor elétrico, regulação, estruturas e construção — com utilidade prática para quem dimensiona, compra e instala estruturas fotovoltaicas: alterações regulatórias e tarifárias; geração distribuída e armazenamento; normas técnicas e dimensionamento (vento, fixação, corrosão); tecnologia fotovoltaica e materiais (aço, alumínio, tratamentos); financiamento e retorno de projetos; mercado solar brasileiro e regional; manutenção, segurança e qualidade em campo. Toda notícia termina em consequência prática para a obra ou para a decisão de compra — não é resenha de mercado por si só.

## Janela, fontes e blocos

- **Janela:** últimos 7 dias (máximo 10 se faltar material, registrando a exceção).
- **Fontes obrigatórias:**
  - Canal Solar: https://canalsolar.com.br/
  - Fotovolt / Aranda: https://www.arandanet.com.br/revista/fotovolt/noticias
  - Giro ABSOLAR: https://www.absolar.org.br/posts/?category_name=giro-absolar
  - Energy Channel: https://www.energychannel.co/
  - Folha — energia solar: https://www1.folha.uol.com.br/folha-topicos/energia-solar/
  - Exame — energia solar: https://exame.com/noticias-sobre/energia-solar/
- **Fontes complementares:**
  - ANEEL: https://www.gov.br/aneel/
  - EPE: https://www.epe.gov.br/pt/imprensa/noticias
  - ONS: https://www.ons.org.br/
  - pv magazine Brasil: https://www.pv-magazine-brasil.com/
  - pv magazine Global: https://www.pv-magazine.com/
  - IEA — Solar PV: https://www.iea.org/news?energySystem%5B0%5D=solar-pv
  - IRENA: https://www.irena.org/News
  - MME: https://www.gov.br/mme/
  - Câmara dos Deputados: https://www.camara.leg.br/noticias
- **Evitar:** especulação apresentada como fato; promessas absolutas de economia; política partidária sem relação operacional; menção espontânea a recuperação judicial de qualquer empresa; falências e demissões sem relação operacional.

| Bloco | Quantidade | Slots | Campos |
|---|---:|---|---|
| destaques (parcial `assets/partials/highlight.html`) | 3 (exato) | `{{HIGHLIGHT_1}}`, `{{HIGHLIGHT_2}}`, `{{HIGHLIGHT_3}}` | `tag`: tema estratégico (ex.: regulação, estruturas, mercado); `titulo`: gancho específico, sem clickbait; `contexto`: 80–130 palavras; `impacto`: 45–80 palavras, rótulo 'O que isso significa para sua obra:'; `url`: fonte |
| curtas (parcial `assets/partials/quick-item.html`) | 5 (exato) | `{{QUICK_1}}`, `{{QUICK_2}}`, `{{QUICK_3}}`, `{{QUICK_4}}`, `{{QUICK_5}}` | `titulo`: uma linha; `url`: fonte |

Confirmar a data de publicação na página original, não apenas no resultado de busca.

## Seleção

Priorizar:

- alterações regulatórias e tarifárias (ANEEL, leilões, marco da GD);
- normas técnicas e dimensionamento (NBR, vento, fixação, estruturas);
- geração distribuída e armazenamento;
- tecnologia e materiais (módulos, aço, alumínio, tratamentos, corrosão);
- financiamento e retorno de projetos solares;
- usinas e projetos de grande porte (o que o mercado está construindo);
- manutenção, segurança e qualidade de instalação;
- mercado solar brasileiro e regional (dados ABSOLAR, capacidade instalada);
- internacional apenas com consequência prática para o Brasil (preço de painel, tarifa de importação, tecnologia).

Dar prioridade extra a matérias sobre **estruturas** (normas, novas linhas, ensaios) — é o território da marca.

Evitar sempre:

- republicações sem informação nova;
- especulação apresentada como fato;
- matérias cujo conteúdo integral não pôde ser verificado;
- tragédias ou polêmicas usadas só para chamar atenção.

## Redação dos destaques

- A tag indica o **tema estratégico**, não a fonte.
- Título com gancho específico — tensão, contraste ou consequência prática — sem clickbait. Evitar títulos meramente descritivos ("Empresa lança recurso X").
- Contexto com fonte, data, dado específico e por que importa; não traduzir literalmente.
- Bloco de impacto fecha com uma implicação concreta: o que revisar, medir, testar, evitar ou priorizar. Nada de "é importante ficar atento".
- Fontes estrangeiras: reescrever com contexto brasileiro e não sugerir que regra de outro país vale aqui.
- Legislação, tarifas, incentivos e números financeiros: confirmar em fonte oficial/primária.
