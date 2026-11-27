from pathlib import Path
import json,hashlib,subprocess
from collections import Counter
from lxml import etree
from PIL import Image,ImageChops,ImageDraw
from pypdf import PdfReader
base=Path('/home/efeins/src/opensiddur-repos/output/marmorstein_rosh_hashanah_2/pesuqei_s46_s63/exports');old=base.with_name('exports_rejected_stream_v1');manifest=json.loads((base/'render_manifest.json').read_text());report={'status':'passed_bounded_exporter_change_only','profiles':{},'findings':[]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def scanlinks(pdf):
 r=PdfReader(pdf);out=[]
 for pn,p in enumerate(r.pages,1):
  for a in p.get('/Annots',[]):
   a=a.get_object();u=str(a.get('/A',{}).get('/URI',''))
   if '/page/n' in u:out.append((pn,u,tuple(map(float,a['/Rect']))))
 return r,out
for name in manifest:
 a=old/name;b=base/name;ra,la=scanlinks(a/'book.pdf');rb,lb=scanlinks(b/'book.pdf');assert len(ra.pages)==len(rb.pages)
 removed=list((Counter(la)-Counter(lb)).elements());added=list((Counter(lb)-Counter(la)).elements());assert not added,(name,added)
 boxes=[]
 for folder in (a,b):
  root=etree.fromstring(subprocess.check_output(['pdftotext','-bbox',str(folder/'book.pdf'),'-'],stderr=subprocess.DEVNULL));boxes.append([[(tuple(n.get(k)for k in ('xMin','yMin','xMax','yMax')),''.join(n.itertext()))for n in p.xpath('.//*[local-name()="word"]')if ''.join(n.itertext())!='↗']for p in root.xpath('//*[local-name()="page"]')])
 assert boxes[0]==boxes[1],name+' wordcoordinateschanged'
 changed=[];pageproof=[]
 for pn,(pa,pb)in enumerate(zip(sorted(a.glob('page-*.png')),sorted(b.glob('page-*.png'))),1):
  ia,ib=Image.open(pa).convert('RGB'),Image.open(pb).convert('RGB');delta=ImageChops.difference(ia,ib);bounds=delta.getbbox()
  if bounds:
   mask=Image.new('L',ia.size,0);draw=ImageDraw.Draw(mask);sx=ia.width/float(ra.pages[pn-1].mediabox.width);sy=ia.height/float(ra.pages[pn-1].mediabox.height);h=float(ra.pages[pn-1].mediabox.height)
   for page,url,r in removed:
    if page==pn:draw.rectangle([int(r[0]*sx)-3,int((h-r[3])*sy)-3,int(r[2]*sx)+3,int((h-r[1])*sy)+3],fill=255)
   outside=ImageChops.multiply(delta.convert('L'),ImageChops.invert(mask));assert outside.getbbox()is None,(name,pn,bounds,'non-arrowpixelschanged')
   changed.append({'physical_page':pn,'pixel_difference_bounds':bounds,'removed_source_urls':[u for page,u,r in removed if page==pn]})
  pageproof.append({'physical_page':pn,'before_png_sha256':sha(pa),'after_png_sha256':sha(pb),'unchanged_except_removed_source_arrow':True})
 report['profiles'][name]={'pages':len(ra.pages),'before_pdf_sha256':sha(a/'book.pdf'),'after_pdf_sha256':sha(b/'book.pdf'),'prayer_word_coordinates_identical':True,'added_source_links':added,'removed_source_links':[{'physical_page':p,'url':u,'rect':r}for p,u,r in removed],'changed_pages':changed,'pixel_proof':pageproof};print(name,'pixels+text+linkdiffOK',len(removed),'redundantlinksremoved',flush=True)
(base/'bounded_stream_v2_diff.json').write_text(json.dumps(report,indent=2)+'\n')
