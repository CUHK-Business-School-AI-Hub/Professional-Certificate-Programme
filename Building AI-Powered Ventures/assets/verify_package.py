"""Check navigable files and distribution boundaries without opening private .env files."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
import re,zipfile,json
ROOT=Path(__file__).resolve().parents[1]
errors=[];links=0
for p in ROOT.rglob('*'):
    if not p.is_file() or p.suffix not in {'.md','.html'} or 'local-state' in p.parts:continue
    text=p.read_text()
    refs=re.findall(r'\]\(([^\n\)]+)\)',text) if p.suffix=='.md' else re.findall(r'(?:href|src|data-source)="([^"]+)"',text)
    for ref in refs:
        ref=ref.strip('<>');u=urlsplit(ref)
        if u.scheme or u.netloc or not u.path:continue
        if any(x in ref for x in ['${','{{']):continue
        dest=(p.parent/unquote(u.path).lstrip('/')).resolve() if '/reference-products/case2/static/' in str(p) else (p.parent/unquote(u.path)).resolve();links+=1
        if not dest.exists():errors.append(f'{p.relative_to(ROOT)} -> {ref}')
for archive in ROOT.rglob('*.zip'):
    with zipfile.ZipFile(archive) as z:
        if z.testzip():errors.append('Corrupt ZIP: '+archive.name)
        for name in z.namelist():
            parts=Path(name).parts
            if any(x in parts for x in ['.env','.env.local','local-state','__pycache__','.DS_Store','.git']) or name.startswith('/') or '..' in parts:
                errors.append('Forbidden archive entry: '+archive.name+' / '+name)
            if archive.name=='student-data.zip' and not name.startswith('student-data/'):
                errors.append('Non-student entry: '+name)
html=(ROOT/'slides/AI-Ventures-202612-Slides-1.html').read_text();ids=re.findall(r'<section class="slide\b[^>]*id="slide-(\d+)"',html)
if ids!=[str(i) for i in range(1,84)]:errors.append('Slide sequence is not 1–83')
note_pages=re.findall(r'^## Slide (\d+) ',(ROOT/'notes/Slide Notes.md').read_text(),re.M)
if note_pages!=[str(i) for i in range(45,84)]:errors.append('Instructor slide notes must cover only slides 45–83')
expected={'slides','notes','data','reference-products','guides','assets'}
if {p.name for p in ROOT.iterdir() if p.is_dir()}!=expected:errors.append('Unexpected top-level folder')
print(json.dumps({'local_links_checked':links,'slides':len(ids),'archives':len(list(ROOT.rglob('*.zip'))),'errors':errors},indent=2))
raise SystemExit(bool(errors))
