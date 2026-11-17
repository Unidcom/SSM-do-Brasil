Status: publicado para aprovação; criação na Brevo falhou

# Radar Estrutural SSM — 2026-11-18

- Data do cabeçalho: Quarta-feira, 18 de novembro de 2026.
- Fechamento: 16/11/2026, America/Sao_Paulo. Edição preparada antecipadamente; não inclui fatos futuros.
- Janela editorial: 11 a 18/11/2026, limitada aos fatos disponíveis até o fechamento em 16/11. Sem ampliação.
- Assunto: Solar com backup: autonomia começa no dimensionamento
- Pré-header: Projetos em escolas, expansão solar e decisões que afetam a execução da obra.
- Fontes obrigatórias consultadas via web: Canal Solar, Fotovolt/Aranda, Giro ABSOLAR, Energy Channel, Folha e Exame. ABSOLAR sem notícia recente na listagem; Folha e Exame com listagens desatualizadas; matérias do Energy Channel sem conteúdo integral verificável foram excluídas.
- Fonte primária complementar: https://www.iea.org/files/2e65f28e-b5f9-4f1b-86eb-942fc2946ceb/Renewables2026.pdf (previsões; não resultados já realizados).
- Confirmação regulatória: https://www.gov.br/aneel/pt-br/assuntos/noticias/2026/tarifa-hora-certa-proposta-preve-enquadramento-automatico-de-consumidores-que-usam-mais-de-500-kwh-mes (09/11; usada como confirmação, não como item adicional; proposta ainda depende de deliberação).
- API WordPress consultada; sem resposta utilizável na execução. Catálogo existente preservado, conforme fallback da skill.
- Histórico de rotação ausente. Seleção por script: primeiro ativo para solução e primeiro elegível para blog. A edição de 09/11 também selecionou carport, mas não registra campaign_id; não foi considerado uso confirmado.
- MCP ssm_do_brasil não consta entre as ferramentas disponíveis; utilizados os dados aprovados da própria skill.
- Capas: imagens principais das páginas abertas; duas WebP sem alternativa JPG/PNG confirmada. Aviso de compatibilidade: Outlook desktop pode não renderizar WebP; imagens originais preservadas conforme alternativa permitida pela skill.
- Verificação estrutural e de links: aprovada; 27 URLs verificadas, zero erros. Facebook retornou bloqueio HTTP 400 ao robô; demais links e imagens acessíveis.
- Publicação para aprovação: https://unidcom.github.io/aprovacoes-unid/ssm/newsletter-2026-11-18.html — HTTP 200 e conteúdo publicado confirmado.
- Brevo: uma tentativa de criação, HTTP 401 unauthorized por IP não autorizado. Nenhum campaign_id retornado. Autorizar o IP 2804:84:81ea:b300:a926:2d4:31c3:a27e em https://app.brevo.com/security/authorised_ips antes de retomar. Sem repetição automática.
- Rotação avançada: não.

## Conteúdo e fontes

- Destaque (2026-11-16): Sete dias sem rede: o projeto vem antes da promessa — https://canalsolar.com.br/sistema-hibrido-permite-residencia-opere-sete-dias-apagoes/
  Capa: https://canalsolar.com.br/wp-content/uploads/2026/11/Canal-Solar-Sistema-hibrido-permite-que-residencia-no-interior-de-SP-opere-por-sete-dias-durante-apagoes.webp

- Destaque (2026-11-15): Escolas recebem solar: montagem pede planejamento por unidade — https://canalsolar.com.br/municipio-investira-45-milhoes-solar-predios-publicos/
  Capa: https://canalsolar.com.br/wp-content/uploads/2026/11/Canal-Solar-Foto_-PMSBC_Patricia-Ribeiro.webp

- Destaque (2026-11-13): IEA projeta expansão solar; conexão continua decisiva — https://www.arandanet.com.br/revista/fotovolt/noticia/13950-IEA-preve-aumento-de-3,6-TW-em-solar-fotovoltaica-ate-2031.html
  Capa: https://unidcom.github.io/aprovacoes-unid/ssm/img/2026-11-18/expansao-solar-conexao.png

- Curta (2026-11-13): Tarifa Hora Certa: proposta ainda depende da diretoria da ANEEL — https://www.arandanet.com.br/revista/fotovolt/noticia/13955-Aneel-propoe-enquadramento-compulsorio-na-tarifa-branca.html

- Curta (2026-11-13): ABGD passa a se chamar RED e incorpora armazenamento à atuação — https://www.arandanet.com.br/revista/fotovolt/noticia/13952-ABGD-muda-nome-para-RED-e-amplia-atuacao.html

- Curta (2026-11-13): Estudo conecta solar, baterias e eletrificação ao custo do sistema — https://www.arandanet.com.br/revista/fotovolt/noticia/13954-Energia-solar-e-baterias-podem-reduzir-custos-com-eletricidade-em-40-.html

- Curta (2026-11-14): Termômetro ACL compara atratividade dos mercados livre e regulado — https://canalsolar.com.br/nova-ferramenta-acompanhar-precos-livres-energia/

- Curta (2026-11-13): SolarEdge comunica encerramento das vendas diretas no Brasil — https://canalsolar.com.br/solaredge-comunica-fim-das-vendas-diretas-e-das-operacoes-locais-no-brasil/

- solucao-destaque: carport; motivo: primeiro ativo (sem histórico).

- blog-ssm: estrutura-para-carport-solar-como-escolher; motivo: primeiro ativo fora dos últimos 10 usados.

## Correção da terceira capa

- Substituída a capa textual do relatório IEA por ilustração gerada de usina solar e conexão à rede, sem texto ou logotipos. A imagem anterior ficava cortada no mosaico.
- Arquivo: imagens/expansao-solar-conexao.png. Imagem ilustrativa; não representa projeto documentado.
- Textos, links das notícias e demais imagens preservados.

## Correções solicitadas — 17/11/2026

- Solução substituída: solo — Estruturas de solo dimensionadas para cada projeto.
- Blog substituído: painel-solar-telhado-kalhetao — seis verificações antes de especificar.
- Primeira notícia: dimensionamento inicial para 48 horas; sete dias isolado nas condições específicas do teste.
- Rotação editorial passa a considerar HTMLs de edições anteriores, independentemente do campaign_id; confirmação da Brevo permanece separada.

## Publicação pendente — 17/11/2026

- HTML e payload corrigidos; validate_edition.py --sync aprovado.
- Verificação de 27 URLs aprovada; Facebook retornou bloqueio HTTP 400.
- Teste de rotação: 18/11 seleciona solo/Kalhetão; 25/11 seleciona telhados/outro artigo.
- GitHub recusou escrita em Unidcom/aprovacoes-unid (HTTP 403: Resource not accessible by integration). Página pública ainda não atualizada.
- Sincronização adicional com Unidcom/SSM-do-Brasil bloqueada pela revisão automática por exigir autorização explícita para exportação dos artefatos.
