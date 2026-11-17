from pathlib import Path
import json, html, sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / '.agents/skills/newsletter-ssm'
sys.path.insert(0, str(SKILL / 'scripts'))
import rotation
from _newsletter_common import load_config

ED = ROOT / 'newsletter/2026-11-18'
if ED.exists():
    raise RuntimeError('A pasta da edição já existe; preservar antes de gerar outra versão.')
ED.mkdir()
subject = 'Solar com backup: autonomia começa no dimensionamento'
preheader = 'Projetos em escolas, expansão solar e decisões que afetam a execução da obra.'
intro = 'Do backup residencial às instalações em escolas, esta edição conecta geração solar, armazenamento e planejamento de montagem para quem precisa entregar sistemas compatíveis com as condições reais de cada obra.'
highlights = [
 dict(tag='Armazenamento', titulo='Sete dias sem rede: o projeto vem antes da promessa',
 contexto='Em 16/11, o Canal Solar apresentou uma residência paulista com 44 módulos e 12 baterias. Segundo a Ecori, o sistema operou isolado da rede por sete dias em teste. O resultado dependeu do consumo, da geração disponível e da capacidade instalada; não é uma autonomia garantida para outros projetos.',
 impacto='Levante as cargas prioritárias e a autonomia necessária antes de fechar equipamentos, área de módulos e planejamento da instalação.',
 url='https://canalsolar.com.br/sistema-hibrido-permite-residencia-opere-sete-dias-apagoes/',
 imagem='https://canalsolar.com.br/wp-content/uploads/2026/11/Canal-Solar-Sistema-hibrido-permite-que-residencia-no-interior-de-SP-opere-por-sete-dias-durante-apagoes.webp',
 data='2026-11-16', esperado='Sistema híbrido permite', takeaway='Backup exige dimensionamento'),
 dict(tag='Projetos', titulo='Escolas recebem solar: montagem pede planejamento por unidade',
 contexto='Segundo o Canal Solar, em 15/11, São Bernardo do Campo iniciará instalações fotovoltaicas em três escolas. A primeira etapa prevê 132 módulos por escola, dentro de um projeto municipal que combina geração solar e modernização da iluminação.',
 impacto='Confira cobertura, acesso e sequência de montagem de cada unidade antes de programar fabricação e entrega das estruturas.',
 url='https://canalsolar.com.br/municipio-investira-45-milhoes-solar-predios-publicos/',
 imagem='https://canalsolar.com.br/wp-content/uploads/2026/11/Canal-Solar-Foto_-PMSBC_Patricia-Ribeiro.webp',
 data='2026-11-15', esperado='Município paulista investirá', takeaway='Montagem por unidade'),
 dict(tag='Planejamento', titulo='IEA projeta expansão solar; conexão continua decisiva',
 contexto='A Fotovolt destacou em 13/11 a projeção da IEA de 3,6 TW adicionais de solar até 2031. O relatório também aponta filas de conexão e reforça a necessidade de redes e flexibilidade acompanharem a expansão.',
 impacto='Vincule compras e mobilização ao cronograma de conexão; crescimento projetado do mercado não confirma a execução de cada empreendimento.',
 url='https://www.arandanet.com.br/revista/fotovolt/noticia/13950-IEA-preve-aumento-de-3,6-TW-em-solar-fotovoltaica-ate-2031.html',
 imagem='https://unidcom.github.io/aprovacoes-unid/ssm/img/2026-11-18/expansao-solar-conexao.png',
 data='2026-11-13', esperado='IEA prevê aumento', takeaway='Conexão orienta o cronograma')
]
quick = [
 dict(titulo='Tarifa Hora Certa: proposta ainda depende da diretoria da ANEEL',url='https://www.arandanet.com.br/revista/fotovolt/noticia/13955-Aneel-propoe-enquadramento-compulsorio-na-tarifa-branca.html',data='2026-11-13',esperado='Aneel propõe enquadramento'),
 dict(titulo='ABGD passa a se chamar RED e incorpora armazenamento à atuação',url='https://www.arandanet.com.br/revista/fotovolt/noticia/13952-ABGD-muda-nome-para-RED-e-amplia-atuacao.html',data='2026-11-13',esperado='ABGD muda nome'),
 dict(titulo='Estudo conecta solar, baterias e eletrificação ao custo do sistema',url='https://www.arandanet.com.br/revista/fotovolt/noticia/13954-Energia-solar-e-baterias-podem-reduzir-custos-com-eletricidade-em-40-.html',data='2026-11-13',esperado='Energia solar e baterias'),
 dict(titulo='Termômetro ACL compara atratividade dos mercados livre e regulado',url='https://canalsolar.com.br/nova-ferramenta-acompanhar-precos-livres-energia/',data='2026-11-14',esperado='Mercado ganha nova ferramenta'),
 dict(titulo='SolarEdge comunica encerramento das vendas diretas no Brasil',url='https://canalsolar.com.br/solaredge-comunica-fim-das-vendas-diretas-e-das-operacoes-locais-no-brasil/',data='2026-11-13',esperado='SolarEdge comunica fim')
]
def read(rel): return (SKILL / rel).read_text(encoding='utf-8-sig')
def fill(template, values):
    for k,v in values.items(): template=template.replace('{{'+k+'}}',str(v))
    return template
def esc(s): return html.escape(s, quote=True)
config=load_config()
state=rotation.load_state(config)
selected={}
for section in config['secoes']:
    if section['tipo'] in rotation.SELECTABLE:
        chosen=rotation.choose(section,rotation.history_for(state,section['id']),rotation.date.fromisoformat('2026-11-18'))
        selected[section['id']]=chosen
        if not chosen.get('item'): raise RuntimeError(chosen)
values=dict(SUBJECT=esc(subject),PREHEADER=esc(preheader),EDITION_DATE='Quarta-feira, 18 de novembro de 2026',INTRO=esc(intro))
for i,h in enumerate(highlights,1):
    words=len(h['contexto'].split()); impact=len(h['impacto'].split())
    assert (35<=words<=60 if i==1 else 25<=words<=45),(i,words)
    assert (15<=impact<=30 if i==1 else 10<=impact<=25),(i,impact)
    partial='highlight-featured.html' if i==1 else 'highlight-compact.html'
    values[f'HIGHLIGHT_{i}']=fill(read('assets/partials/'+partial),dict(TAG=esc(h['tag']),TITLE=esc(h['titulo']),CONTEXT=esc(h['contexto']),IMPACT=esc(h['impacto']),URL=esc(h['url'])))
    values[f'HERO_COVER_{i}']=fill(read('assets/partials/hero-cover.html'),dict(COVER_URL=esc(h['url']),COVER_IMG=esc(h['imagem']),COVER_ALT=esc(h['titulo'])))
    values[f'TAKEAWAY_{i}']=esc(h['takeaway'])
for i,q in enumerate(quick,1): values[f'QUICK_{i}']=fill(read('assets/partials/quick-item.html'),dict(URL=esc(q['url']),TITLE=esc(q['titulo'])))
for sid,slot in [('solucao-destaque','SOLUCAO_BLOCK'),('blog-ssm','BLOG_BLOCK')]:
    item=selected[sid]['item']; d=item['dados']
    values[slot]=fill(read(item['modelo']),dict(TITLE=esc(d['titulo']),BODY=esc(d.get('texto_curto',d['texto'])),IMAGE_SRC=esc(item['imagem_publica']),IMAGE_ALT=esc(d['titulo']),CTA_URL=esc(d['cta_url'])))
result=fill(read('assets/template.html'),values)
(ED/'newsletter.html').write_text(result,encoding='utf-8')
plain_values=dict(SUBJECT=subject,EDITION_DATE=values['EDITION_DATE'],INTRO_PLAIN=intro,
    DESTAQUES_PLAIN='\n\n'.join(h['titulo']+'\n'+h['contexto']+'\nPara a obra: '+h['impacto']+'\nFonte: '+h['url'] for h in highlights),
    CURTAS_PLAIN='\n\n'.join(q['titulo']+'\n'+q['url'] for q in quick))
for sid,slot in [('solucao-destaque','SOLUCAO_BLOCK_PLAIN'),('blog-ssm','BLOG_BLOCK_PLAIN')]:
    d=selected[sid]['item']['dados']; plain_values[slot]=d['titulo']+'\n'+d.get('texto_curto',d['texto'])+'\n'+d['cta_url']
(ED/'plain-text.txt').write_text(fill(read('assets/plain-text-template.txt'),plain_values),encoding='utf-8')
edition_data=dict(assunto=subject,pre_header=preheader,destaques=highlights,curtas=quick,selecoes=selected)
(ED/'editorial.json').write_text(json.dumps(edition_data,ensure_ascii=False,indent=2),encoding='utf-8')
metadata='''Status: rascunho local

# Radar Estrutural SSM — 2026-11-18

- Data do cabeçalho: Quarta-feira, 18 de novembro de 2026.
- Fechamento: 16/11/2026, America/Sao_Paulo. Edição preparada antecipadamente; não inclui fatos futuros.
- Janela editorial: 11 a 18/11/2026, limitada aos fatos disponíveis até o fechamento em 16/11. Sem ampliação.
- Assunto: '''+subject+'''
- Pré-header: '''+preheader+'''
- Fontes obrigatórias consultadas via web: Canal Solar, Fotovolt/Aranda, Giro ABSOLAR, Energy Channel, Folha e Exame. ABSOLAR sem notícia recente na listagem; Folha e Exame com listagens desatualizadas; matérias do Energy Channel sem conteúdo integral verificável foram excluídas.
- Fonte primária complementar: https://www.iea.org/files/2e65f28e-b5f9-4f1b-86eb-942fc2946ceb/Renewables2026.pdf (previsões; não resultados já realizados).
- Confirmação regulatória: https://www.gov.br/aneel/pt-br/assuntos/noticias/2026/tarifa-hora-certa-proposta-preve-enquadramento-automatico-de-consumidores-que-usam-mais-de-500-kwh-mes (09/11; usada como confirmação, não como item adicional; proposta ainda depende de deliberação).
- API WordPress consultada; sem resposta utilizável na execução. Catálogo existente preservado, conforme fallback da skill.
- Histórico de rotação ausente. Seleção por script: primeiro ativo para solução e primeiro elegível para blog. A edição de 09/11 também selecionou carport, mas não registra campaign_id; não foi considerado uso confirmado.
- MCP ssm_do_brasil não consta entre as ferramentas disponíveis; utilizados os dados aprovados da própria skill.
- Capas: imagens principais das páginas abertas; duas WebP sem alternativa JPG/PNG confirmada. Compatibilidade com Outlook desktop pendente de resolução.
- Verificação estrutural e de links: pendente.
- Publicação para aprovação: pendente.
- Brevo: nenhuma campanha criada nesta execução.
- Rotação avançada: não.

## Conteúdo e fontes
'''
for h in highlights: metadata+='\n- Destaque ('+h['data']+'): '+h['titulo']+' — '+h['url']+'\n  Capa: '+h['imagem']+'\n'
for q in quick: metadata+='\n- Curta ('+q['data']+'): '+q['titulo']+' — '+q['url']+'\n'
for sid,s in selected.items(): metadata+='\n- '+sid+': '+s['item']['id']+'; motivo: '+s['motivo']+'.\n'
(ED/'metadata.md').write_text(metadata,encoding='utf-8')
print('Edição montada:',ED)
