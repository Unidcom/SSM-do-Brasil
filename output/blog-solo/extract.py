import sys
from pathlib import Path
sys.path.insert(0,str(Path('.pdf-tools').resolve()))
import fitz
root=Path('SSM-do-Brasil-main/.agents/skills/seo-geo-blog-writer/references/ssm')
out=Path('output/blog-solo'); (out/'imagens').mkdir(parents=True,exist_ok=True)
d=fitz.open(root/'Novo CATALOGO SSM 2026.Unid.pdf')
for n in [25,26,27,28]:
 d[n].get_pixmap(matrix=fitz.Matrix(1,1)).save(out/f'catalogo-{n+1}.png')
r=fitz.open(root/'ACESSORIOS SSM Renders.pdf')
sheet=fitz.open(); p=sheet.new_page(width=1000,height=1800)
for i,pg in enumerate(r):
 pix=pg.get_pixmap(matrix=fitz.Matrix(.15,.15))
 x=(i%5)*200;y=(i//5)*105
 p.insert_image(fitz.Rect(x,y,x+195,y+85),stream=pix.tobytes('png'))
 p.insert_text((x+5,y+100),str(i+1),fontsize=12)
p.get_pixmap().save(out/'renders-contato.png')
for n in [42,72,73]:
 pg=r[n-1]
 ims=pg.get_images(full=True)
 print(n,[(a[0],a[2],a[3],a[1]) for a in ims])
 a=max(ims,key=lambda a:a[2]*a[3]); pix=fitz.Pixmap(r,a[0])
 if a[1]: pix=fitz.Pixmap(pix,fitz.Pixmap(r,a[1]))
 pix.save(out/'imagens'/f'render-oficial-{n}.png')
d[25].get_pixmap(matrix=fitz.Matrix(4,4),clip=fitz.Rect(475,15,585,68)).save(out/'imagens/logo-ssm.png')
