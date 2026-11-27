from pathlib import Path
import json,hashlib
from opensiddur.exporter.tex.latex import transform_xml_to_tex
base=Path('/home/efeins/src/opensiddur-repos/output/marmorstein_rosh_hashanah_2/morning_s25_s45/exports');project=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-projects/master/project');manifest=json.loads((base/'render_manifest.json').read_text());out=Path('/tmp/day2-final-tex-candidates');out.mkdir(exist_ok=True);rows=[]
for name,r in manifest.items():
 path=out/(name+'.tex');text=transform_xml_to_tex(Path(r['print']),output_file=str(path),settings_file=Path(r['settings']),project_directory=project)
 changed=text!=(base/name/'book.tex').read_text();row={'profile':name,'changed':changed,'old_tex_sha256':hashlib.sha256((base/name/'book.tex').read_bytes()).hexdigest(),'new_tex_sha256':hashlib.sha256(path.read_bytes()).hexdigest()};rows.append(row);print(name,changed,flush=True)
Path('/tmp/day2-final-tex-change-report.json').write_text(json.dumps(rows,indent=2)+'\n')
