import os,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
os.chdir(root)
os.environ['PATH']=r'C:/Users/Win 10/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd'+os.pathsep+os.environ['PATH']
repo=str(root.parent/'aprovacoes-unid')
for key,value in {'GIT_CONFIG_COUNT':'3','GIT_CONFIG_KEY_0':'safe.directory','GIT_CONFIG_VALUE_0':repo,'GIT_CONFIG_KEY_1':'user.name','GIT_CONFIG_VALUE_1':'angelianechefer','GIT_CONFIG_KEY_2':'user.email','GIT_CONFIG_VALUE_2':'angeliane.chefer@unidcom.com.br'}.items(): os.environ[key]=value
sys.path.insert(0,str(root/'.agents/skills/newsletter-ssm/scripts'))
import publish_approval
mode=sys.argv[1:]
sys.argv=['publish_approval.py','newsletter/2026-11-18','--timeout','55']+mode
raise SystemExit(publish_approval.main())
