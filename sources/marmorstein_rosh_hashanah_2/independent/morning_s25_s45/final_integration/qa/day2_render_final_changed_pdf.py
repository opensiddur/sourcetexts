from pathlib import Path
import json,subprocess,sys
from opensiddur.exporter.pdf.pdf import export_to_pdf
from opensiddur.exporter.html.html import build_book
base=Path('/home/efeins/src/opensiddur-repos/output/marmorstein_rosh_hashanah_2/morning_s25_s45/exports');project=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-projects/master/project');manifest=json.load(open(base/'compile_manifest.json'));matrix=base.parent/'matrix'
for key in ['german_False_gender_male_shabbat_False','german_True_gender_female_shabbat_True']:
 folder=base/('expanded_'+('weekday'if'False'in key else'shabbat'));folder.mkdir(exist_ok=True)
 manifest[folder.name]={'settings':str(matrix/(key+'.yaml')),'print':str(matrix/(key+'.xml'))}
report=json.load(open(base/"render_manifest.json"))
for name,row in manifest.items():
 if name != "documentary_parallel":continue
 folder=base/name;folder.mkdir(exist_ok=True);settings=Path(row['settings']);xml=Path(row['print']);pdf=folder/'book.pdf';tex=folder/'book.tex'
 print('RENDERING',name,flush=True)
 if not export_to_pdf(xml,pdf,settings_file=settings,tex_output=tex,build_dir=folder/'build',project_directory=project):
  raise RuntimeError('PDF failed: '+name)
 if row.get('electronic'):
  (folder/'book.html').write_text(build_book(Path(row['electronic']),settings,project),encoding='utf-8')
 for old in folder.glob('page-*.png'):old.unlink()
 subprocess.run(['pdftoppm','-r','110','-png',str(pdf),str(folder/'page')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 report[name]={**row,'pdf':str(pdf),'html':str(folder/'book.html')if row.get('electronic')else None}
 print('DONE',name,flush=True)
(base/'render_manifest.json').write_text(json.dumps(report,indent=2)+'\n')
