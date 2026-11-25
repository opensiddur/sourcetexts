from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,hashlib
from PIL import Image,ImageChops
from pypdf import PdfReader
p=Path('/tmp/mahzor-s276');out=Path('/home/efeins/.codex/worktrees/marmorstein-processor/master/output/pdf/marmorstein_s293');before=p/'note-fix-before/documentary.pdf';after=out/'documentary.pdf';assert len(PdfReader(before).pages)==len(PdfReader(after,strict=True).pages)==226
base=p/'note-fix-raster';base.mkdir(exist_ok=True)
def render(item):
 label,path=item;folder=base/label;folder.mkdir(exist_ok=True);subprocess.run(['pdftoppm','-r','60','-png',str(path),str(folder/'page')],check=True,capture_output=True)
with ThreadPoolExecutor(max_workers=2)as pool:list(pool.map(render,[('before',before),('after',after)]))
changes=[]
for a in sorted((base/'before').glob('page-*.png')):
 b=base/'after'/a.name;im1=Image.open(a).convert('RGB');im2=Image.open(b).convert('RGB');diff=ImageChops.difference(im1,im2);bbox=diff.getbbox()
 if bbox:changes.append(dict(page=int(a.stem.split('-')[-1]),changed_bbox_at60dpi=list(bbox)))
assert [r['page']for r in changes]==[206],changes
subprocess.run(['pdftoppm','-f','206','-l','206','-scale-to','2200','-png',str(after),str(p/'full-pdf-images/documentary-note-fix')],check=True,capture_output=True)
report=dict(status='passed',pages_compared=226,raster_dpi=60,only_changed_page=206,unchanged_pages=225,changes=changes,source_and_footnote_words_unchanged='Actual TeX diff changes only the two visible anchor labels:128 becomes128,129;129 becomesempty. Apparatus128and129 retained.',before_pdf_sha256=hashlib.sha256(before.read_bytes()).hexdigest(),after_pdf_sha256=hashlib.sha256(after.read_bytes()).hexdigest(),corrected_page_image=str(p/'full-pdf-images/documentary-note-fix-206.png'))
(p/'note-fix-pdf-page-proof.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
