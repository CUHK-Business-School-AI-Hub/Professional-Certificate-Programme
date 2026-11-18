"""Generate instructor slide notes and shareable, secret-free reference packages."""
from pathlib import Path
import re,zipfile,hashlib,json,sys
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
class PlainText(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.hrefs=[]
    def handle_data(self,text):self.parts.append(text)
    def handle_starttag(self,tag,attrs):
        if tag in {'p','br','li'}:self.parts.append('\n')
        if tag=='a':
            href=dict(attrs).get('href','')
            self.hrefs.append(href);self.parts.append('[')
    def handle_endtag(self,tag):
        if tag in {'p','li'}:self.parts.append('\n')
        if tag=='a' and self.hrefs:self.parts.append(']('+self.hrefs.pop()+')')
def plain(s):
    p=PlainText();p.feed(s);return re.sub(r'\n{3,}','\n\n',''.join(p.parts)).strip()
s=(ROOT/'slides/AI-Ventures-202612-Slides-1.html').read_text()
notes=['# Day 1 case notes · Slides 45–83\n\nInstructor-only companion covering slides 45–83, generated from the HTML speaker notes. Morning lecture notes and Day 2 are excluded. Edit the HTML for Case One, or `assets/case-two/build_slides.py` for Case Two, then regenerate this file. The [Instructor Outline](Instructor%20Outline.md) is the teaching plan. Do not distribute these notes before the exercises.\n']
for section in re.findall(r'<section class="slide\b.*?</section>',s,re.S):
    note=re.search(r'<aside class="speaker-notes" hidden>(.*?)</aside>',section,re.S)
    if not note:continue
    n=re.search(r'id="slide-(\d+)"',section)[1]
    if int(n)<45:continue
    title=re.search(r'<h[12][^>]*>(.*?)</h[12]>',section,re.S)
    notes.append('\n## Slide '+n+' · '+re.sub(r'\s+',' ',plain(title[1]))+'\n\n'+plain(note[1])+'\n')
(ROOT/'notes/Slide Notes.md').write_text(''.join(notes))
if '--notes-only' in sys.argv:
    print('Generated instructor notes for slides 45–83 only.')
    raise SystemExit(0)
def archive(path,files):
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for file,name in files:
            assert file.name not in {'.env','.env.local','.DS_Store'}
            assert not any(x in file.parts for x in ['local-state','__pycache__','.git'])
            if Path(name).parts[0]=='case2' and Path(name).suffix=='.md' and len(Path(name).parts)==2:
                content=file.read_text().replace('../../data/case2/','data/')
                content=re.sub(r'For a standalone copy, download .*?Inside the course workspace, the app reads shared data from `data/`\.','This standalone package includes data in `data/`. Start from this directory with `python3 server.py`.',content,flags=re.S)
                content=re.sub(r' From the repository root:\n\n```sh\n.*?```','',content,flags=re.S)
                z.writestr(str(name),content)
            else:z.write(file,name)
    with zipfile.ZipFile(path) as z:assert z.testzip() is None
skill=ROOT/'reference-products/case1/product-intelligence'
archive(skill.parent/'product-intelligence.zip',[(p,p.relative_to(skill.parent)) for p in sorted(skill.rglob('*')) if p.is_file()])
app=ROOT/'reference-products/case2'
allowed={'.py','.js','.css','.html','.json','.md','.command'}
files=[(p,Path('case2')/p.relative_to(app)) for p in sorted(app.rglob('*')) if p.is_file() and (p.suffix in allowed or p.name=='.env.example') and not any(x in p.parts for x in ['local-state','__pycache__']) and (p.parent==app and p.name in {'README.md','WALKTHROUGH.md','TEST_REPORT.md','rules.md','engine.py','service.py','chat.py','server.py','start.command','.env.example'} or p.relative_to(app).parts[0] in {'static','tests','context'})]
for folder in ['student-data','ground-truth']:
    for p in sorted((ROOT/'data/case2'/folder).rglob('*')):
        if p.is_file():files.append((p,Path('case2/data')/p.relative_to(ROOT/'data/case2')))
# Make the extracted README independent of its download link and workspace paths.
archive(ROOT/'reference-products/case2-reference.zip',files)
print('Generated slide notes, Case One skill ZIP and self-contained Case Two reference ZIP.')
