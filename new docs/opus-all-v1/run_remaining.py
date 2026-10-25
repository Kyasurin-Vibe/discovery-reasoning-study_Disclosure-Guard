"""Serial paid drafting only; already reserved packages are never regenerated."""
import subprocess,sys,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
if '--allow-api' not in sys.argv: raise SystemExit('Use --allow-api only for authorized paid drafting')
subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE/'prepare.py')],cwd=ROOT,check=True)
for i in range(1,8):
    pid=f'T{i}'
    folder=HERE/'runs'/pid
    if folder.exists():
        source=folder/'SOURCE.json'
        if source.exists():
            data=json.loads(source.read_text())
            if data.get('stop_reason')=='stop':
                print(pid+': saved; skipped',flush=True)
                continue
        raise SystemExit(pid+': existing/in-flight/incomplete record; stop without duplicate call')
    command=[str(ROOT/'.venv/bin/inspect'),'eval',str(HERE/'runner.py'),
        '--model','anthropic/claude-opus-5-5','-T',f'package={pid}','-T','allow_api=true',
        '--max-connections','1','--max-retries','2','--max-samples','1',
        '--log-dir',str(HERE/'logs'/pid),'--display','plain']
    print('Starting '+pid+'; no judge.',flush=True)
    result=subprocess.run(command,cwd=ROOT)
    source=folder/'SOURCE.json'
    if result.returncode or not source.exists(): raise SystemExit(pid+': interrupted; preserved and stopped')
    data=json.loads(source.read_text())
    if data.get('stop_reason')!='stop': raise SystemExit(pid+': non-normal stop; saved and stopped')
print('Remaining Opus drafts complete. No judge calls.',flush=True)
