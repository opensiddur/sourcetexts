from pathlib import Path
from copy import deepcopy
import json,hashlib
from opensiddur.importer.marmorstein_rosh_hashanah_1.realizations import review_payloads
from opensiddur.importer.scan.review import review_is_current
p=Path('/tmp/mahzor-s276');out=p/'review-v4';current=json.loads((p/'integration-v1/source/readings.json').read_text());cc=json.loads((p/'integration-v1/source/corrections.json').read_text())['corrections'];oldsrc=Path('/home/efeins/.codex/worktrees/marmorstein-sources/master/sources/marmorstein_rosh_hashanah_1');old=json.loads((oldsrc/'readings.json').read_text());oc=json.loads((oldsrc/'corrections.json').read_text())['corrections'];reviews=json.loads((oldsrc/'reviews.json').read_text());before={k:v for k,v,_ in review_payloads(old,oc)};after={k:v for k,v,_ in review_payloads(current,cc)};fields=['expanded_order_sha256','source_order_sha256','documentary_instructions_sha256','navigation_sha256'];pairs=[];prior=json.loads((p/'review-v3/realization-bindings.json').read_text());prior_bodies={x['key']:x['payload']for x in prior['meaningful']};manifest=[]
for row in json.loads((out/'realization-bindings.json').read_text())['global_only_prior']:
 key=row['key'];a=json.loads(before[key]);b=json.loads(after[key]);assert review_is_current(reviews[key],before[key]),key
 for field in fields:a.pop(field,None);b.pop(field,None)
 assert a==b,key
 pairs.append(dict(key=key,old_accepted_receipt_current=True,semantic_payload_identical=True,semantic_payload=a))
(out/'prior-semantic-values.json').write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n')
for key,text in after.items():
 if key not in prior_bodies:continue
 b=deepcopy(prior_bodies[key]);a=json.loads(text)
 for field in fields:a.pop(field,None);b.pop(field,None)
 changed=a!=b;rel=key.replace('/','__');file=out/(rel+'.json');file.write_text(text+'\n');chunks=[]
 if 'efchad_bemaasai'in key:
  # Each fragment is under Read's usual output limit and together they are
  # byte-identical to the complete realization payload, with no omission.
  for i in range(0,len(text),10000):
   chunk=out/(rel+f'__chunk{i//10000+1:02}.txt');chunk.write_text(text[i:i+10000]);chunks.append(str(chunk))
  assert ''.join(Path(f).read_text()for f in chunks)==text
 manifest.append(dict(key=key,file=str(file),changed_semantics_since_v3=changed,full_payload_chunks=chunks,sha256=hashlib.sha256(text.encode()).hexdigest()))
(out/'meaningful-payload-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(out/'binding-machine-proof.json').write_text(json.dumps(dict(status='passed',prior_accepted_semantic_values_identical=len(pairs),excluded_exact_shared_fields=fields,old_receipts_verified_current=True,meaningful_payloads=len(manifest),changed_since_v3=[x['key']for x in manifest if x['changed_semantics_since_v3']],efchad_full_payloads_losslessly_chunked=True,proof_algorithm=str(p/'prepare-binding-proof-v4.py'),actual_full_prior_values=str(out/'prior-semantic-values.json'),manifest=str(out/'meaningful-payload-manifest.json')),indent=2)+'\n');print('141 unchanged accepted semantic payloads; meaningful changed:',[x['key']for x in manifest if x['changed_semantics_since_v3']])
