"""Read-only archive and current-source verification; no APIs."""
from pathlib import Path
import hashlib,json,zipfile
here=Path(__file__).resolve().parent
root=here.parents[2]
m=json.loads((here/'FREEZE_REVISED.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
errors=[]
zpath=here/'snapshot.zip'
if sha(zpath.read_bytes())!=m['snapshot_zip_sha256']:errors.append('snapshot.zip hash mismatch')
with zipfile.ZipFile(zpath) as z:
    if set(z.namelist())!=set(m['files']):errors.append('archive file set differs')
    for name,expected in m['files'].items():
        if name not in z.namelist() or sha(z.read(name))!=expected:errors.append('archived '+name)
        p=root/name
        if not p.is_file() or sha(p.read_bytes())!=expected:errors.append('current '+name)
current=set(m['explicit_files'])
for pattern in m['patterns']:
    current.update(str(p.relative_to(root)) for p in root.glob(pattern) if p.is_file() and p.name!='.DS_Store' and '__pycache__' not in p.parts)
if current!=set(m['files']):errors.append('current scoped file set changed')
if sha((root/'FREEZE.json').read_bytes())!=m['historical_freeze_sha256']:errors.append('historical FREEZE.json changed')
if errors:raise SystemExit('FREEZE MISMATCH\n'+'\n'.join(errors))
print(f"REVISED FREEZE OK: {len(m['files'])} files; 8 input hashes; archive and current sources match.")
