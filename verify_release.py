"""Offline integrity/privacy checks for the repository and its website (docs/). No model, API, or network calls.
Run from the repository root: python3 verify_release.py [--deep]
--deep requires pypdf and also examines decoded PDF objects and metadata.
"""
from pathlib import Path, PurePosixPath
import hashlib, json, re, io, zipfile, sys, html, urllib.parse
ROOT=Path(__file__).resolve().parent
DEEP='--deep' in sys.argv
ID_DIGESTS=['aa947479ad254953e24d39ef7b0c242aebba637c929c54d85a0949aac2262906']
issues=[];counts={'files':0,'archives':0,'archive_members':0,'pdfs_deep_checked':0,'local_links':0}
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader=None
if DEEP and PdfReader is None:
    print('DEEP CHECK UNAVAILABLE: install the recorded pypdf dependency; no network was used.');sys.exit(2)
KEY=re.compile(r'\bsk-(?:ant-)?[A-Za-z0-9_-]{24,}')
LOCAL=re.compile(r'/Users/[A-Za-z0-9_.-]+|/home/[A-Za-z0-9_.-]+|[A-Za-z]:\\Users\\[^\\\s"\']+')
def issue(name,kind):
    issues.append({'file':name,'issue':kind})  # Never include the matched value.
def excluded(name):
    parts=PurePosixPath(name).parts
    return any(x in {'.git','.venv','venv','__pycache__','.pytest_cache','__MACOSX','node_modules'} for x in parts) or any(x=='.env' or x.startswith('.env.') or x=='.DS_Store' or x.endswith(('.pyc','.pyo','.pem','.key')) for x in parts)
def textcheck(s,name):
    if LOCAL.search(s):issue(name,'local identifying absolute path')
    if KEY.search(s):issue(name,'key-shaped value; suppressed')
    for word in re.findall(r'[A-Za-z0-9]+',urllib.parse.unquote(s)):
        if hashlib.sha256(word.lower().encode()).hexdigest() in ID_DIGESTS:
            issue(name,'known local identifier; value suppressed');break
    # Unexpected personal contact details are flagged, not silently redacted.
    emails=re.findall(r'[A-Za-z0-9_.+%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',s)
    if any(not e.lower().endswith(('.example','.invalid')) for e in emails):issue(name,'non-placeholder email requires review; value suppressed')
def check_pdf(data,name):
    if not DEEP:return
    counts['pdfs_deep_checked']+=1
    try:r=PdfReader(io.BytesIO(data))
    except Exception:issue(name,'PDF could not be parsed');return
    seen=set()
    def walk(x,depth=0):
        if depth>60:return
        try:
            if hasattr(x,'get_object'):x=x.get_object()
        except Exception:return
        if id(x) in seen:return
        seen.add(id(x))
        if isinstance(x,dict):
            for k,v in x.items():walk(k,depth+1);walk(v,depth+1)
            if hasattr(x,'get_data'):
                try:walk(x.get_data(),depth+1)
                except Exception:pass
        elif isinstance(x,(list,tuple)):
            for v in x:walk(v,depth+1)
        elif isinstance(x,str):textcheck(x,name+'!decoded-PDF-object')
        elif isinstance(x,bytes):textcheck(x.decode('latin1','ignore'),name+'!decoded-PDF-stream')
    walk(r.trailer)
def inspect(data,name,depth=0):
    if depth>5:issue(name,'archive nesting beyond audit limit');return
    textcheck(name,name)
    suffix=PurePosixPath(name.split('!')[-1]).suffix.lower()
    if suffix in {'.eval','.zip'} or data[:4]==b'PK\x03\x04':
        counts['archives']+=1
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                textcheck(z.comment.decode('latin1','ignore'),name+'!archive-comment')
                for info in z.infolist():
                    if info.is_dir():continue
                    counts['archive_members']+=1
                    p=PurePosixPath(info.filename)
                    if p.is_absolute() or '..' in p.parts:issue(name,'unsafe archive member path');continue
                    member=name+'!'+info.filename
                    if excluded(info.filename):issue(member,'excluded archive entry')
                    textcheck(info.comment.decode('latin1','ignore'),member+'!comment')
                    inspect(z.read(info),member,depth+1)
        except Exception:issue(name,'archive unreadable')
        return
    if suffix=='.pdf':check_pdf(data,name);return
    try:s=data.decode('utf-8')
    except UnicodeError:issue(name,'uninspected binary format');return
    textcheck(s,name)
    if suffix=='.json':
        try:json.loads(s)
        except Exception:issue(name,'invalid JSON')
    if suffix in {'.md','.html'} and '!' not in name:
        links=re.findall(r'\]\(([^)]+)\)',s) if suffix=='.md' else re.findall(r'href="([^"]+)"',s)
        for link in links:
            link=html.unescape(link)
            if re.match(r'^(?:https?://|mailto:|#)',link):continue
            part=re.sub(r':\d+$','',urllib.parse.unquote(link.split('#')[0]))
            counts['local_links']+=1
            target=(ROOT/name).parent/part
            try:target.resolve().relative_to(ROOT)
            except ValueError:issue(name,'local link escapes release');continue
            if not target.exists():issue(name,'broken local link; target omitted from diagnostic')
manifest=ROOT/'MANIFEST.sha256'
if not manifest.exists():print('RELEASE FAILED: manifest absent');sys.exit(1)
expected={}
for line in manifest.read_text().splitlines():
    h,n=line.split('  ',1);expected[n]=h
# Git's own metadata (only the top-level .git directory of a clone) is not publication content.
present={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p!=manifest and p.relative_to(ROOT).parts[0]!='.git'}
for n in sorted(set(expected)-present):issue(n,'missing manifest file')
for n in sorted(present-set(expected)):issue(n,'unexpected file outside manifest')
for n in sorted(present):
    p=ROOT/n;counts['files']+=1
    if p.is_symlink():issue(n,'symbolic link is not allowed')
    if excluded(n):issue(n,'excluded file type')
    data=p.read_bytes()
    if n in expected and hashlib.sha256(data).hexdigest()!=expected[n]:issue(n,'release hash mismatch')
    inspect(data,n)
unique=[]
for x in issues:
    if x not in unique:unique.append(x)
print(json.dumps({'status':'PASS' if not unique else 'FAIL','checks':counts,'pdf_mode':'decoded metadata, objects and streams' if DEEP else 'integrity only; use --deep for PDF privacy','issues':unique},indent=2))
sys.exit(0 if not unique else 1)
