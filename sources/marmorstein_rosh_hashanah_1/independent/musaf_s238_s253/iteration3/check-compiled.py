from pathlib import Path
from lxml import etree
import copy,json,unicodedata
from opensiddur.exporter.condition_eval import parse_condition_element,evaluate_condition,TriState
p=Path('/tmp/mahzor-s238/iteration3');NS={'tei':'http://www.tei-c.org/ns/1.0','j':'http://jewishliturgy.org/ns/jlptei/2','p':'http://jewishliturgy.org/ns/processing'};N=lambda s:unicodedata.normalize('NFKD',s)
CONDITION_VALUE=None
def words(node):
 n=copy.deepcopy(node)
 for tag in ['note','head','teiHeader']:etree.strip_elements(n,'{'+NS['tei']+'}'+tag,with_tail=False)
 active={};pieces=[]
 class Lookup:
  def get_active_setting(self,fs_type,feature_name):return CONDITION_VALUE
 def visible():return all(v is not TriState.FALSE for v in active.values())
 def walk(el):
  if el.tag=='{'+NS['j']+'}conditional':
   active[el.get('{http://www.w3.org/XML/1998/namespace}id')]=evaluate_condition(parse_condition_element(el),Lookup());return
  if el.tag=='{'+NS['j']+'}endConditional':
   active.pop(el.get('target','').lstrip('#'),None);return
  if el.text and visible():pieces.append(el.text)
  for child in el:
   walk(child)
   if child.tail and visible():pieces.append(child.tail)
 walk(n)
 assert not active,'Unclosed condition in extracted witness'
 return ' '.join(''.join(pieces).split())
def sides(node):
 return {role:' '.join(words(x)for x in node.xpath('.//p:parallelItem[@role="'+role+'"][not(.//p:parallelItem)]',namespaces=NS))for role in ['primary','parallel']}
checks=[]
for state in ['unknown','included','omitted']:
 for dest in ['print','electronic']:
  CONDITION_VALUE=None if state=='unknown' else state=='included'
  r=etree.parse(str(p/f'compiled-{state}-{dest}.xml'))
  h=r.xpath('//p:transclude[starts-with(@target,"urn:x-opensiddur:text:poem:haochez_beyad_middat_mishpat@")] ',namespaces=NS)[0];texts=sides(h)
  assert texts['primary'].count(N('וְכֹל מַאֲמִינִים'))==22,(state,dest,'refrain count',texts['primary'])
  assert texts['parallel'].count('All believe')==22
  if state=='included':assert N('וְהֹוֶה')in texts['primary']and 'He was, is and shall be' in texts['parallel']
  if state=='omitted':assert N('וְהֹוֶה')not in texts['primary']and 'He was and shall be'in texts['parallel']and 'He was, is'not in texts['parallel']
  v=r.xpath('//p:transclude[starts-with(@target,"urn:x-opensiddur:text:poem:v_yeetayu_kol_leavdekha@")] ',namespaces=NS)[0];vt=sides(v)
  assert len(v.xpath('.//tei:milestone[@unit="stanza" and @corresp]',namespaces=NS))==16
  if state=='included':assert N('וְיִזְבְּחוּ')in vt['primary']and 'To Thee will they offer their sacrifices'in vt['parallel']
  if state=='omitted':assert N('וְיִזְבְּחוּ')not in vt['primary']and 'To Thee will they offer their sacrifices'not in vt['parallel']
  first=r.xpath('//p:transclude[starts-with(@target,"urn:x-opensiddur:text:poem:vechayyot_asher_hennah@")] ',namespaces=NS)[0]
  rows=[row for row in first.xpath('./p:parallel',namespaces=NS) if any(sides(row).values())];assert len(rows)==2
  assert sides(rows[0])['primary']and not sides(rows[0])['parallel']
  assert 'Have mercy on the pillars'in sides(rows[1])['parallel']
  checks.append(dict(state=state,destination=dest,all22refrains=True,optional_word_matches_both_languages=True,electronic_conditions_evaluated_with_exporter_predicate=(dest=='electronic'),offering_clause_matches_both_languages=True,eight_existing_stanzas_each_language=True,untranslated_stanzas_unpaired=True))
(p/'compiled-content-checks.json').write_text(json.dumps(dict(scope='Isolated revised-module runtime verification; not full-service or visual acceptance',checks=checks),indent=2)+'\n');print(len(checks),'destination/state cases passed:22refrains,8stanzas,optional-word agreement,partial translation alignment')
