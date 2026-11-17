from pathlib import Path
from urllib.request import urlopen, Request
import re
root=Path(__file__).resolve().parent/'2026-11-18'
url='https://www.arandanet.com.br/assets/ckeditor/kcfinder/upload/images/Noticias/FV/S2979/Foto5.jpg'
print('Baixando capa',flush=True)
with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=15) as r:
    content=r.read()
    print(r.status,r.headers.get('Content-Type'),len(content),flush=True)
(root/'terceira-original.jpg').write_bytes(content)
