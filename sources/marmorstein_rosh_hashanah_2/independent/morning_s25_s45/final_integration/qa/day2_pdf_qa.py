from pathlib import Path
import json,subprocess,re,hashlib
from pypdf import PdfReader
from lxml import etree
from PIL import Image,ImageDraw
base=Path('/home/efeins/src/opensiddur-repos/output/marmorstein_rosh_hashanah_2/morning_s25_s45/exports');manifest=json.load(open(base/'render_manifest.json'));report={'profiles':{},'findings':[]}
def overlap(a,b):return a[0]<b[2] and a[2]>b[0] and a[1]<b[3] and a[3]>b[1]
for name,row in manifest.items():
 folder=base/name;pdf=PdfReader(row['pdf']);bounds=etree.fromstring(subprocess.check_output(['pdftotext','-bbox',row['pdf'],'-']));pages=bounds.xpath('//*[local-name()="page"]');links=[];issues=[];internal=0;outside=[]
 for pn,(page,box)in enumerate(zip(pdf.pages,pages),1):
  width=float(page.mediabox.width);height=float(page.mediabox.height)
  words=[([float(n.get(k))for k in ['xMin','yMin','xMax','yMax']],''.join(n.itertext()))for n in box.xpath('.//*[local-name()="word"]')]
  outside +=[{'page':pn,'word':w,'bounds':r}for r,w in words if r[0]<-1 or r[1]<-1 or r[2]>width+1 or r[3]>height+1]
  rects=[]
  for item in page.get('/Annots',[]):
   a=item.get_object();action=a.get('/A',{});uri=str(action.get('/URI',''))
   if action.get('/S')=='/GoTo' or a.get('/Dest')is not None:internal+=1
   if '/page/n'not in uri:continue
   rect=list(map(float,a['/Rect']));view=[rect[0],height-rect[3],rect[2],height-rect[1]]
   if not (0<=rect[0]<rect[2]<=width and 0<=rect[1]<rect[3]<=height):issues.append({'page':pn,'kind':'outside source link','rect':rect})
   if rect[2]-rect[0]<8 or rect[3]-rect[1]<8:issues.append({'page':pn,'kind':'small source link','rect':rect})
   if any(overlap(rect,r)for r in rects):issues.append({'page':pn,'kind':'overlapping source links'})
   rects.append(rect);ink=[view[0]+1.05,view[1]+1.05,view[2]-1.05,view[3]-1.05];hits=[w for r,w in words if overlap(ink,r)and w!='↗'];arrow=any(w=='↗' and overlap(view,r)for r,w in words)
   if hits:issues.append({'page':pn,'kind':'source arrow collides with words','hits':hits,'rect':view})
   if not arrow:issues.append({'page':pn,'kind':'source link has no visible arrow','rect':view})
   links.append({'page':pn,'uri':uri,'rect':rect})
 log=(folder/'build/book.log').read_text(errors='replace');
 if 'Missing character:'in log:issues.append({'kind':'missing glyph'})
 if 'undefined references'in log.lower():issues.append({'kind':'unresolved references'})
 html_info=None
 if row.get('html'):
  h=etree.HTML(Path(row['html']).read_text());ids=h.xpath('//@id');hrefs=h.xpath('//a[starts-with(@href,"#")]/@href');html_info={'ids_unique':len(ids)==len(set(ids)),'missing_anchors':[v for v in hrefs if v[1:]and v[1:]not in ids]}
  if not html_info['ids_unique']or html_info['missing_anchors']:issues.append({'kind':'HTML anchors'})
 files=sorted(folder.glob('page-*.png'));sheet=Image.new('RGB',(1000,370*((len(files)+3)//4)),'#ddd');draw=ImageDraw.Draw(sheet)
 for i,p in enumerate(files):
  im=Image.open(p);im.thumbnail((245,335));x=i%4*250;y=i//4*370;sheet.paste(im,(x,y+25));draw.text((x+5,y+5),f'{name} p{i+1}',fill='black')
 sheet.save(folder/'contact.jpg')
 report['profiles'][name]={'pages':len(pdf.pages),'pdf_sha256':hashlib.sha256(Path(row['pdf']).read_bytes()).hexdigest(),'source_links':links,'internal_links':internal,'outside_page_words':outside,'overfull_warnings':log.count('Overfull'),'html':html_info,'findings':issues}
 report['findings'] +=[{'profile':name,**issue}for issue in issues]
 print(name,len(pdf.pages),'pages',len(links),'source links',len(issues),'findings',len(outside),'outside words')
report['status']='passed'if not report['findings']else'failed';(base/'pdf_qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PDF QA',report['status'])
