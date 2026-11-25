from pathlib import Path
import json,re,hashlib
from pypdf import PdfReader
from lxml import html
from urllib.parse import unquote
q=Path('/home/efeins/.codex/worktrees/marmorstein-processor/master/output/pdf/marmorstein_s253');reports=[]
for name in ['documentary-hebrew','documentary','expanded']:
 f=q/(name+'.pdf');r=PdfReader(f);named=r.named_destinations;unresolved=[];count=0
 for page in r.pages:
  for ref in page.get('/Annots',[]):
   a=ref.get_object();action=a.get('/A',{});target=a.get('/Dest')
   if action.get('/S')=='/GoTo':target=action.get('/D')
   if target is None:continue
   count+=1
   if isinstance(target,str)and target not in named:unresolved.append(target)
 log=(q/(name+'-latex')/(name+'.log')).read_text(errors='replace');over=re.findall(r'Overfull \\hbox[^\n]*',log);missing=re.findall(r'Missing character:[^\n]*',log)
 h=q/(name+'.html');tree=html.fromstring(h.read_bytes());ids=tree.xpath('//@id');assert len(ids)==len(set(ids));links=tree.xpath('//a[starts-with(@href,"#")]/@href');broken=[s for s in links if len(s)>1 and unquote(s[1:])not in ids]
 assert not unresolved and not over and not missing and not broken,(name,unresolved,over,missing,broken)
 reports.append(dict(profile=name,pdf_pages=len(r.pages),pdf_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),html_sha256=hashlib.sha256(h.read_bytes()).hexdigest(),pdf_internal_links=count,html_internal_links=len(links),unresolved_destinations=[],duplicate_html_ids=0,pdf_overfull_hboxes=0,missing_glyphs=0))
(q/'artifact-verification.json').write_text(json.dumps(reports,indent=2)+'\n');print([(r['profile'],r['pdf_pages'])for r in reports],'all destinations/glyphs/overflow checks pass')
