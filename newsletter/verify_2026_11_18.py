import sys,json,hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'.agents/skills/newsletter-ssm'
sys.path.insert(0,str(SKILL/'scripts'))
import check_links as c
from _newsletter_common import write_json,load_config
from validate_edition import sync_payload,validate
ED=ROOT/'newsletter/2026-11-18'
data=json.loads((ED/'editorial.json').read_text(encoding='utf-8'))
source=(ED/'newsletter.html').read_text(encoding='utf-8')
expected={x['url']:[x['esperado']] for x in data['destaques']+data['curtas']}
refs=c.collect(source)
print('Verificando',len(refs),'links e imagens',flush=True)
def check(ref):
    r=c.check(ref[0],ref[1],expected.get(ref[0],[]))
    print(ref[1],r.get('status'),ref[0],r['erros'],flush=True)
    return r
with ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(check,refs))
errors=[f"{r['url']}: {e}" for r in results for e in r['erros']]
warnings=[f"{r['url']}: {e}" for r in results for e in r['avisos']]
report=dict(ok=not errors,verificado_em=datetime.now(timezone.utc).isoformat(timespec='seconds'),html_sha256=hashlib.sha256(source.encode()).hexdigest(),total=len(results),erros=errors,avisos=warnings,resultados=results)
write_json(ED/'links-report.json',report)
sync_payload(ED,load_config(),data['assunto'],data['pre_header'])
errors,warnings=validate(ED,load_config())
write_json(ED/'validation-report.json',dict(ok=not errors,erros=errors,avisos=warnings))
print(json.dumps(dict(ok=not errors,erros=errors,avisos=warnings),ensure_ascii=True),flush=True)
