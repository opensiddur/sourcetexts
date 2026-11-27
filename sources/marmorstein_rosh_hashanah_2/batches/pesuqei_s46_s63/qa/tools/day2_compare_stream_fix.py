from pathlib import Path
import json,sys,importlib.util
from lxml import etree
from opensiddur.exporter import cli_common
from opensiddur.exporter.scan_links import mark_scan_links,SCAN_LINK
oldpath=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-processor/master/opensiddur/exporter/scan_links.py');spec=importlib.util.spec_from_file_location('scan_stream_before_fix',oldpath);old=importlib.util.module_from_spec(spec);sys.modules[spec.name]=old;spec.loader.exec_module(old)
base=Path('/home/efeins/src/opensiddur-repos/output/marmorstein_rosh_hashanah_2/pesuqei_s46_s63/exports');manifest=json.loads((base/'render_manifest.json').read_text());rows={}
for name,row in manifest.items():
 rows[name]={}
 for mode in ('print','electronic'):
  if not row.get(mode):continue
  outputs=[]
  for mark in (old.mark_scan_links,mark_scan_links):
   root=etree.parse(row[mode]).getroot();cli_common.mark_scan_links=mark;cli_common.prepare_compiled_tree(root,scan_links=True);tree=root.getroottree();outputs.append({tree.getpath(n):n.get('facs')for n in root.iter('{http://www.tei-c.org/ns/1.0}pb')if n.get(SCAN_LINK)})
  a,b=outputs;removed=[{'xpath':path,'facs':facs}for path,facs in a.items()if path not in b];added=[{'xpath':path,'facs':facs}for path,facs in b.items()if path not in a];rows[name][mode]={'before':len(a),'after':len(b),'removed':removed,'added':added};print(name,mode,len(a),'->',len(b),'removed',len(removed),'added',len(added))
cli_common.mark_scan_links=mark_scan_links
(base/'stream_fix_comparison.json').write_text(json.dumps({'status':'bounded_marker_comparison','profiles':rows,'changed_profiles':[k for k,row in rows.items()if any(v['removed']or v['added']for v in row.values())]},indent=2)+'\n')
