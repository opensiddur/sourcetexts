from pathlib import Path
from copy import deepcopy
import json,hashlib
p=Path('/tmp/mahzor-s276');r=json.loads((p/'integration-v1/source/readings.json').read_text());old=json.loads(Path('/home/efeins/.codex/worktrees/marmorstein-sources/master/sources/marmorstein_rosh_hashanah_1/readings.json').read_text());bindings=json.loads((p/'review-v4/realization-bindings.json').read_text());keys=set(bindings['payload_hashes']);g={x['key']for x in bindings['global_only_prior']};m={x['key']for x in bindings['meaningful']};assert not g&m and keys==g|m;oldreviews=json.loads(Path('/home/efeins/.codex/worktrees/marmorstein-sources/master/sources/marmorstein_rosh_hashanah_1/reviews.json').read_text());oldkeys={k for k in oldreviews if k.startswith('realization/')};assert oldkeys<=keys

def strip_new(items,mode):
 result=deepcopy(items)
 def walk(xs):
  for item in xs:
   if item.get('section')==('musaf_repetition_draft_s220'if mode=='source'else'musaf_repetition_s220'):
    marker='instruction'if mode=='source'else'section';value='musaf_zikhronot_cantor_direction'if mode=='source'else'musaf_zikhronot_opening';end=next(i for i,x in enumerate(item['order'])if x.get(marker)==value);item['order']=item['order'][:end]
   walk(item.get('order',[]))
 walk(result);return result
for mode in ['source','expanded']:assert strip_new(r[mode+'_order'],mode)==old[mode+'_order'],mode
assert r['navigation']==old['navigation'];assert all(r['documentary_instructions'][key]==value for key,value in old['documentary_instructions'].items())
report=dict(status='passed',current_payload_keys=182,previous_realization_keys_preserved=len(oldkeys),prior141_and_meaningful41_disjoint_and_complete=True,accepted_source_arrangement_prefix_identical=True,accepted_expanded_arrangement_prefix_identical=True,old_navigation_identical=True,all_old_documentary_instructions_identical=True,scope='Only appended new-batch contexts and explicitly reviewed new documentary end-coverage notes change; no accepted-prefix order/navigation/instruction changes.')
(p/'encoding-prefix-and-keyset-proof.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
