"""Offline preflight and immutable snapshot. No API usage."""
import json, hashlib, sys, zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
import runner
sha=runner.sha
inputs={}
for pid in runner.IDS:
    _,messages,_=runner.preflight(pid)
    inputs[pid]=runner.input_hash(messages)
runner.existing_base()
if '--freeze' in sys.argv:
    if (HERE/'FREEZE.json').exists(): raise SystemExit('Refusing to overwrite freeze')
    old=json.loads((ROOT/'new docs/optimized-v2/VERSION.json').read_text())
    names=set(old['files'])
    names.update(str(p.relative_to(ROOT)) for p in HERE.iterdir() if p.is_file() and p.suffix in ('.py','.md','.txt'))
    files={n:sha((ROOT/n).read_bytes()) for n in sorted(names)}
    with zipfile.ZipFile(HERE/'snapshot.zip','w',zipfile.ZIP_DEFLATED) as z:
        for n in files: z.write(ROOT/n,n)
    runner.dump(HERE/'FREEZE.json',{'version':'opus-only-all-v1','inputs':inputs,'files':files,
        'model':runner.MODEL,'config':runner.CONFIG.model_dump(exclude_none=True),
        'snapshot_sha256':sha((HERE/'snapshot.zip').read_bytes()),
        'reused_base':str(runner.existing_base()[0].relative_to(ROOT))})
runner.verify()
manifest=json.loads((HERE/'FREEZE.json').read_text())
assert sha((HERE/'snapshot.zip').read_bytes())==manifest['snapshot_sha256']
with zipfile.ZipFile(HERE/'snapshot.zip') as z:
    assert set(z.namelist())==set(manifest['files'])
    for n,h in manifest['files'].items(): assert sha(z.read(n))==h
# Test authorization, base protection, and isolation without contacting any provider.
for kwargs in ({}, {'package':'base','allow_api':True}, {'package':'invalid','allow_api':True}):
    try: runner.opus_only(**kwargs)
    except ValueError: pass
    else: raise AssertionError('Guard did not block '+str(kwargs))
assert runner.CONFIG.effort=='medium' and runner.CONFIG.cache_prompt is False
print('OFFLINE OK: all 8 input hashes, existing base, snapshot, API/base guards; no model calls.')
