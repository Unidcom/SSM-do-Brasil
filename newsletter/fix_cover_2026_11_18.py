from pathlib import Path
import json
root=Path(__file__).resolve().parent
edition=root/'2026-11-18'
old='https://www.arandanet.com.br/assets/ckeditor/kcfinder/upload/images/Noticias/FV/S2979/Foto5.jpg'
new='https://unidcom.github.io/aprovacoes-unid/ssm/img/2026-11-18/expansao-solar-conexao.png'
file=edition/'newsletter.html'
source=file.read_text(encoding='utf-8')
assert source.count(old)==1
file.write_text(source.replace(old,new),encoding='utf-8')
file=edition/'editorial.json'
data=json.loads(file.read_text(encoding='utf-8'))
assert data['destaques'][2]['imagem']==old
data['destaques'][2]['imagem']=new
data['destaques'][2]['imagem_origem']='Ilustração gerada por IA; usina solar e conexão à rede, sem representar empreendimento específico.'
file.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
file=edition/'metadata.md'
source=file.read_text(encoding='utf-8').replace('  Capa: '+old,'  Capa: '+new)
source+='\n## Correção da terceira capa\n\n- Substituída a capa textual do relatório IEA por ilustração gerada de usina solar e conexão à rede, sem texto ou logotipos. A imagem anterior ficava cortada no mosaico.\n- Arquivo: imagens/expansao-solar-conexao.png. Imagem ilustrativa; não representa projeto documentado.\n- Textos, links das notícias e demais imagens preservados.\n'
file.write_text(source,encoding='utf-8')
file=root/'build_2026_11_18.py'
file.write_text(file.read_text(encoding='utf-8').replace(old,new),encoding='utf-8')
print('Terceira capa substituída.')
