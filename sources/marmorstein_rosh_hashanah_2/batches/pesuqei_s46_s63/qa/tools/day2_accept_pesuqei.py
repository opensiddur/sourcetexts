from pathlib import Path
import json,hashlib,shutil
from datetime import datetime,timezone
S=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-sources/master/sources/marmorstein_rosh_hashanah_2');B=S/'batches/pesuqei_s46_s63';I=S/'independent/pesuqei_s46_s63';P=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-processor/master');J=Path('/home/efeins/.codex/worktrees/marmorstein-day-two-projects/master/project');C=Path('/home/efeins/src/opensiddur-repos/output/marmorstein_rosh_hashanah_2/pesuqei_s46_s63/exports')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
closure=read(I/'question1023_closure.json');generated=closure['generated_output_sha256'];assert len(generated)==34
assert all(sha(J/p)==h for p,h in generated.items())
recipe=read(B/'pesuqei_units.json');assert all(sha(J/p)==h for p,h in recipe['protected_files'].items())
assert read(B/'recipe_approval.json')['recipe_sha256']==sha(B/'pesuqei_units.json')
assert recipe['source_approval_sha256']==sha(B/'source_approval.json')
assert not read(B/'source_approval.json')['unresolved_readings']
frozen=read(B/'qa/frozen_exports.json')
for files in frozen['profiles'].values():
 for p,h in files.items():assert sha(Path(p))==h,(p,'changed reviewed artifact')
for p,h in frozen['independently_captured_browser_evidence'].items():assert sha(Path(p))==h,p
assert read(I/'final_pdf_review.json')['status']=='approved_presentation_scope'
assert read(I/'final_html_review.json')['status']=='approved_presentation_scope'
for file in ['day2-pesuqei-production.log','day2-pesuqei-production-qa.log','day2-pesuqei-production-ref.log','day2-production-names.log','day2-production-features.log','day2-production-profiles.log']:shutil.copyfile('/tmp/'+file,B/'qa'/file)
shutil.copyfile('/tmp/day2_pesuqei_production_qa.py',B/'qa/tools/day2_pesuqei_production_qa.py');shutil.copyfile('/tmp/day2_apply_1023.py',B/'qa/tools/day2_apply_1023.py')
now=datetime.now(timezone.utc).isoformat();actual={'status':'accepted_exact_reviewed_artifacts','batch':'pesuqei_s46_s63','accepted_utc':now,'source_question1023':'Resolved by user: printed maqaf. Provisional literal source already matched; no artifact changed.','source_approval_sha256':sha(B/'source_approval.json'),'recipe_approval_sha256':sha(B/'recipe_approval.json'),'production_xml_sha256':generated,'unchanged_previous_review_manifest_sha256':sha(B/'qa/frozen_exports.json'),'profiles':frozen['profiles'],'independent_pdf_review_sha256':sha(I/'final_pdf_review.json'),'independent_html_review_sha256':sha(I/'final_html_review.json'),'exporter_dependency':{'pr':349,'commit':'87c27ce','status':'open_ready_ci_passed','merge_before':[331,110]},'reviewed_presentation_limitations':'Inherited English labels in the default expanded electronic Contents; visible bilingual headings and navigation work. Exact review details retained.'};write(C/'accepted_manifest.json',actual);shutil.copyfile(C/'accepted_manifest.json',B/'qa/accepted_artifacts.json')
reviews=['source_v4_closure.json','question1023_closure.json','recipe_final_review.json','code_v5/review.json','exporter_stream_fix/review.json','final_pdf_review.json','final_html_review.json']
acceptance={'status':'accepted','accepted_utc':now,'batch':'pesuqei_s46_s63','scans':list(range(46,64)),'scan_count':18,'book_total_scans':385,'cumulative_accepted_scans':63,'remaining_scans':322,'next_scan':64,'documentary_source_units':15,'documentary_witnesses':29,'source_pages_sha256':sha(B/'working/adjudicated_pages.json'),'raw_source_sha256':sha(B/'working/readings.json'),'source_approval_sha256':sha(B/'source_approval.json'),'recipe_approval_sha256':sha(B/'recipe_approval.json'),'reviews':[{'path':'../../independent/pesuqei_s46_s63/'+f,'sha256':sha(I/f)}for f in reviews],'artifact_manifest':'qa/accepted_artifacts.json','production_validation':'qa/production_registry.json','validated_production_documents':34,'protected_existing_files':786,'exporter_dependency':actual['exporter_dependency'],'pending_user_questions':[],'unresolved_reading_disputes':[],'scope_notes':['Complete source, guideline, identity, alignment, recitation and presentation gates closed.','All 34 production XML files byte-identical to independently reviewed prospective files; all reviewed exports unchanged.','Hebrew-only Psalm91 ending repeat and absent English Psalm136:25 preserved without adjacent translation drift.','Hodu maps its actual Chronicles16:8–36 extent; no complete-chapter identity invented.','Canonical prayer and Bible URNs reused; repeated context identities do not replace canonical texts.','All27 rite/gender/Shabbat configurations checked; Night compilation remains byte-identical.','Independent PDF scope: six profiles,222 pages,286 scan-link rectangles; four HTML profiles and24 correct independently captured images.','PR349 is independently approved and CI passed; merge it before dependent processor331 and projects110. Acceptance is of the reviewed source/encoding/artifacts, not a statement of merge completion.','Other322 scans remain unaccepted.']};write(B/'acceptance.json',acceptance)
p=B/'checklist.json';d=read(p);d.update(status='accepted',accepted=True,pending_user_questions=[])
for key,g in d['gates'].items():
 g['prior_status']=g['status'];g['status']='passed'
 if key in ['adjudication','encoding','alignment','independent_encoding_order_audit']:g.setdefault('evidence',[]).extend(['human_answer_1023.json','../../independent/pesuqei_s46_s63/question1023_closure.json','source_approval.json','recipe_approval.json'])
 if key=='encoding':g['note']='34 production XML documents generated and schema-validated through the approved importer; every byte matches reviewed output.'
 if key=='acceptance':g.update(evidence=['acceptance.json','qa/accepted_artifacts.json'],note='All batch gates closed. Complete accepted coverage63/385; resume scan64.')
d['acceptance_record']='acceptance.json';write(p,d)
p=B/'ACTIVE_REVIEW.json';d=read(p);d.update(status='accepted',pending_question=None,accepted_complete_scans=63,actual_project_files_written=True,sequence_recipe_sha256=sha(B/'pesuqei_units.json'),remaining_actions=[],acceptance_record='acceptance.json',presentation_manifest='qa/accepted_artifacts.json');d['earlier_working_files_and_rejected_versions']='Historical evidence only. Question1023 confirms the existing provisional maqaf; latest source/recipe approval and acceptance records are authoritative.';d['presentation_status']='All exact reviewed artifacts retained by hash; actual production XML is byte-identical.';write(p,d)
p=S/'progress.json';d=read(p)
for key in ['encoded_scan_pages','accepted_scan_pages','independently_reviewed_scan_pages','source_approved_scan_pages']:d[key]=63
for key in ['accepted_scans','source_reading_approved_scans']:d[key]=list(range(1,64))
for key in ['not_yet_encoded_scan_pages','not_yet_fully_encoded_scan_pages']:d[key]=322
d.update(pending_user_questions=[],encoded_prayer_modules=124,encoded_prayer_witnesses=219,next_scan_page=64,latest_accepted_batch='batches/pesuqei_s46_s63/acceptance.json',active_batch=None,next_work='Start the next substantial batch at scan64, Yehi Khevod. Close all source, encoding and presentation gates before accepting that batch.',independent_review='Scans1–63 accepted through complete source, guideline, alignment/order/condition, mechanical and independent PDF/HTML review. Question1023 is resolved; no pending source readings.',encoded_scope='Front matter1–4, second-night service5–24, morning opening/study25–45 and Pesuqei deZimrah46–63 through Psalm93 accepted. Missing English stays absent.',module_count_scope='Documentary source units47+62+15=124 and219 witnesses; service/provider XML are not additional source units.',pesuqei_review_note='Scans46–63 accepted;15units29witnesses, unchanged reviewed production XML,6PDF/4HTML approvals,27-case matrix. ExporterPR349 ready with CI passed; merge before331/110.');write(p,d)
p=P/'specs/MARMORSTEIN_ROSH_HASHANAH_2_CHECKLIST.md';s=p.read_text(encoding='utf-8');at=s.index('## Pesuqei deZimrah installment: scans46–63');prefix,suffix=s[:at],s[at:];suffix=suffix.replace('- [ ]','- [x]');start=suffix.index('Source gate status and immutable evidence live in');suffix=suffix[:start]+'''Source acceptance and exact artifact hashes are recorded in
`batches/pesuqei_s46_s63/acceptance.json`. The human confirms question1023's
printed maqaf, already present in the provisional text; all34 production XML
files and the reviewed exports remain byte-identical. All source, guideline,
alignment, order and presentation gates are closed. Accepted coverage is63/385,
with322 scans remaining; resume at scan64 (Yehi Khevod).

Exporter PR349 has independent approval and green CI. It removes redundant scan
backlinks across full-width translation gaps; merge349 before processor331 and
projects110. It is still open, not a completed merge. Earlier source proposals,
misframed screenshots and provisional manifests remain historical evidence.
''';p.write_text(prefix+suffix,encoding='utf-8')
shutil.copyfile('/tmp/day2_accept_pesuqei.py',B/'qa/tools/day2_accept_pesuqei.py')
print('ACCEPTED46–63;63/385complete;322remaining;next64;34productionXMLhashesandallreviewedartifactsverified')
