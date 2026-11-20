"""Source evidence stays immutable while canonical mappings get their own review."""
from copy import deepcopy
import unittest

from opensiddur.importer.marmorstein_rosh_hashanah_1.build import (
    unit_document, unit_review_text, transclude_unit, document, require_review,
)
from opensiddur.importer.marmorstein_rosh_hashanah_1.realizations import (
    prepare_unit, prepare_documents, validate_occurrences, review_payloads, selection,
)

P = 'urn:x-opensiddur:text:prayer:example'
A = 'urn:x-opensiddur:condition:prayer:example/for_ever'
B = 'urn:x-opensiddur:condition:prayer:example/forever'
NS = {'tei':'http://www.tei-c.org/ns/1.0','j':'http://jewishliturgy.org/ns/jlptei/2'}


def fixture():
    host = dict(stem='host', urn=P, title={'en':'Example'}, languages={'en':[
        dict(corresp=P+'/part', paragraph=1, fragments=[dict(scan='s2', printed_page='1', text='for ever', page_start=True)])]})
    occurrence = dict(stem='occurrence', urn='urn:x-opensiddur:text:siddur:example', title={'en':'Example'},
        wording_selection=[dict(type='opensiddur:variant',features={A:False,B:True})],
        languages={'en':[dict(paragraph=1, canonical=P+'/part', fragments=[dict(scan='s4',printed_page='2',text='forever',page_start=True)])]})
    overlay = dict(id='example',host='host',lang='en',identity=P+'/part',printed='for ever',
                   readings=[dict(text='for ever',corresp=A),dict(text='forever',corresp=B)])
    return dict(units=[host,occurrence],wording_variants=[overlay])


class RealizationTest(unittest.TestCase):
    def test_overlay_does_not_edit_literal_evidence_or_its_review(self):
        r=fixture();before=deepcopy(r);payload=unit_review_text(r['units'][0],'en')
        effective=prepare_unit(r['units'][0],r)
        self.assertEqual(r,before)
        self.assertEqual(unit_review_text(r['units'][0],'en'),payload)
        root=unit_document(effective,'en',True)
        self.assertEqual(root.xpath('//j:option/@corresp',namespaces=NS),[A,B])
        self.assertFalse(root.xpath('//j:declare',namespaces=NS))

    def test_canonical_occurrence_preserves_own_paragraph_and_page(self):
        r=fixture();validate_occurrences(r)
        root=unit_document(prepare_unit(r['units'][1],r),'en',True)
        p=root.xpath('//tei:body/tei:div/tei:p',namespaces=NS)
        self.assertEqual(len(p),1)
        self.assertEqual([v.tag.rsplit('}',1)[-1]for v in p[0]],['pb','transclude'])
        self.assertEqual(p[0][0].get('n'),'2')
        self.assertEqual(p[0][0].get('ed'),'1965 example')
        self.assertEqual(root.xpath('count(//j:declare)',namespaces=NS),1)
        self.assertEqual(root.xpath('count(//j:endDeclare)',namespaces=NS),1)
        self.assertNotIn('forever',''.join(p[0].itertext()))

    def test_source_drift_missing_selection_and_multiple_hosts_fail(self):
        for mutation in ['source','selection','ambiguous','fragment']:
            with self.subTest(mutation=mutation):
                r=fixture()
                if mutation=='source':r['units'][1]['languages']['en'][0]['fragments'][0]['text']='different'
                elif mutation=='selection':r['units'][1]['wording_selection']=[]
                elif mutation=='ambiguous':r['units'].append(deepcopy(r['units'][0]))
                else:r['units'][1]['languages']['en'][0]['fragments']*=2
                with self.assertRaises(ValueError):validate_occurrences(r)

    def test_mapping_and_note_conditions_have_separate_review_payloads(self):
        r=fixture();before=unit_review_text(r['units'][1],'en');payloads=dict((k,v)for k,v,_ in review_payloads(r))
        r['units'][1]['languages']['en'][0]['canonical']=P+'/other'
        self.assertEqual(unit_review_text(r['units'][1],'en'),before)
        after=dict((k,v)for k,v,_ in review_payloads(r))
        self.assertNotEqual(payloads['realization/occurrence/en'],after['realization/occurrence/en'])
        with self.assertRaisesRegex(ValueError,'canonical realization'):require_review(r,{})
        r=fixture();before=dict((k,v)for k,v,_ in review_payloads(r))
        r['units'][0]['citations']={'en':[dict(text='comment',scan='s2',conditions=[dict(type='opensiddur:variant',features={A:True})])]}
        self.assertNotEqual(before['realization/host/en'],dict((k,v)for k,v,_ in review_payloads(r))['realization/host/en'])

    def test_host_default_is_local_to_each_transcluder(self):
        r=fixture();root,body=document('en','example','Example',P)
        transclude_unit(body,r['units'][0],r)
        transclude_unit(body,r['units'][0],r)
        self.assertEqual(selection(r,'host')[0]['features'],{A:True,B:False})
        ids=root.xpath('//j:declare/@xml:id',namespaces=NS)
        self.assertEqual(len(ids),2);self.assertEqual(len(set(ids)),2)
        self.assertEqual(root.xpath('//j:endDeclare/@target',namespaces=NS),['#'+i for i in ids])

    def test_canonical_home_leaves_only_transclusions_in_its_context(self):
        r=fixture();u=r['units'][0]
        u['urn']='urn:x-opensiddur:text:siddur:example'
        u['canonical_home']=dict(file='example_parts',urn=P+'/part',map_root=False,title={'en':'Example'})
        context,home=prepare_documents(u,r)
        self.assertEqual(home['urn'],P+'/part')
        self.assertFalse(home['map_root'])
        root=unit_document(context,'en',True)
        body=root.xpath('//tei:body',namespaces=NS)[0]
        self.assertNotIn('for ever',''.join(body.itertext()))
        self.assertTrue(body.xpath('.//j:transclude',namespaces=NS))
        validate_occurrences(r)

    def test_overlay_cannot_claim_a_different_first_printed_reading(self):
        r=fixture();r['wording_variants'][0]['readings'][0]['text']='not the source'
        with self.assertRaisesRegex(ValueError,'printed reading first'):prepare_unit(r['units'][0],r)

    def test_complete_formula_keeps_invocation_outside_verse(self):
        r=fixture();u=r['units'][0];u['urn']=P;u['text_corresp']=P+'/text';s=u['languages']['en'][0]
        s['corresp']='urn:x-opensiddur:text:bible:psalms/22/4';s['source']=s['corresp'];s['end_reference']=True
        u['languages']['en'].append(dict(paragraph=1,fragments=[dict(scan='s2',printed_page='1',text=', O God.',page_start=True)]))
        root=unit_document(u,'en',True);p=root.xpath('//tei:body/tei:div/tei:p',namespaces=NS)[0]
        starts=p.xpath('tei:milestone[@corresp]',namespaces=NS)
        self.assertEqual([v.get('corresp')for v in starts],[P+'/text',s['corresp']])
        terminator=p.xpath('tei:milestone[@unit="verse" and not(@corresp)]',namespaces=NS)[0]
        following = (terminator.tail or '') + ''.join(''.join(n.itertext())+(n.tail or '') for n in list(p)[p.index(terminator)+1:])
        self.assertIn('O God',following)
        self.assertEqual(p[-1].get('unit'),'prayer-part')
        self.assertIsNone(p[-1].get('corresp'))

    def test_all_occurrence_controls_are_bound_into_review(self):
        for key,value in [('conditions',[{'type':'opensiddur:service','features':{'service':'musaf'}}]),
                          ('start',P+'/different'),('end',P+'/end'),('reuse',{'en':P}),
                          ('title',{'en':'Different'}),('map_root',False),('marked',True)]:
            with self.subTest(key=key):
                r=fixture();before=dict((k,v) for k,v,_ in review_payloads(r))
                r['units'][1][key]=value
                self.assertNotEqual(before['realization/occurrence/en'],
                                    dict((k,v) for k,v,_ in review_payloads(r))['realization/occurrence/en'])

    def test_unmodeled_host_controls_fail_before_export(self):
        for key in ['conditions','speaker','instructions','marked','repeat','edition_label']:
            with self.subTest(segment=key):
                r=fixture();r['units'][0]['languages']['en'][0][key]='unmodeled'
                with self.assertRaises(ValueError):validate_occurrences(r)
        for key in ['qere_ketiv','alternatives','quotations','abbreviations','enlarged_letters']:
            with self.subTest(fragment=key):
                r=fixture();r['units'][0]['languages']['en'][0]['fragments'][0][key]=[{}]
                with self.assertRaises(ValueError):validate_occurrences(r)

    def test_orphan_overlay_wrong_selection_and_partial_selection_fail(self):
        for mutation in ['host','lang','type','partial','duplicate']:
            with self.subTest(mutation=mutation):
                r=fixture()
                if mutation in ('host','lang'):r['wording_variants'][0][mutation]='missing'
                elif mutation=='type':r['units'][1]['wording_selection'][0]['type']='opensiddur:calendar'
                elif mutation=='partial':del r['units'][1]['wording_selection'][0]['features'][A]
                else:r['wording_variants'].append(deepcopy(r['wording_variants'][0]))
                with self.assertRaises(ValueError):validate_occurrences(r)

    def test_optional_word_is_marked_and_absent_in_selected_occurrence(self):
        r=fixture();s=r['units'][0]['languages']['en'][0];s['fragments'][0]['text']='The (word) follows.'
        r['wording_variants']=[dict(id='optional',host='host',lang='en',identity=P+'/part',
            kind='optional',printed='(word)',text='word',condition=A)]
        r['units'][1]['wording_selection'][0]['features']={A:False}
        r['units'][1]['languages']['en'][0]['fragments'][0]['text']='The follows.'
        validate_occurrences(r)
        root=unit_document(prepare_unit(r['units'][0],r),'en',True)
        self.assertTrue(root.xpath('//j:conditional[@type="marked"]',namespaces=NS))
        self.assertFalse(root.xpath('//j:option',namespaces=NS))
        self.assertFalse(selection(r,'host'))

    def test_canonical_home_rejects_context_controls_and_suppresses_old_pb(self):
        r=fixture();u=r['units'][0]
        u['canonical_home']=dict(file='home',urn=P,title={'en':'Canonical words'},map_root=False)
        context,home=prepare_documents(u,r)
        self.assertFalse(unit_document(home,'en',True).xpath('//tei:pb',namespaces=NS))
        self.assertEqual(home['title'],{'en':'Canonical words'})
        for key in ['conditions','instructions','publication_context','text_corresp','reuse']:
            with self.subTest(key=key):
                altered=deepcopy(u);altered[key]='forbidden'
                with self.assertRaises(ValueError):prepare_documents(altered,r)

    def test_join_respects_punctuation_and_split_words(self):
        from opensiddur.importer.marmorstein_rosh_hashanah_1.realizations import join_source_fragments
        self.assertEqual(join_source_fragments([{'text':'Israel'},{'text':', O God.'}]),'Israel, O God.')
        self.assertEqual(join_source_fragments([{'text':'fore','join_next':True},{'text':'ver'}]),'forever')

    def test_generated_canonical_collision_and_direct_caller_defaults(self):
        from pathlib import Path
        from opensiddur.importer.marmorstein_rosh_hashanah_1.realizations import validate_generated
        r=fixture();root=unit_document(prepare_unit(r['units'][0],r),'en',True)
        caller,body=document('en','example','Example',P+'/caller')
        from lxml import etree
        etree.SubElement(body,'{'+NS['j']+'}transclude',target=P+'/part',type='inline')
        docs=[(Path('/project/example-en/host.xml'),root),(Path('/project/example-en/caller.xml'),caller)]
        validate_generated(docs,r)
        self.assertEqual(caller.xpath('//tei:f/@name',namespaces=NS),[A,B])
        with self.assertRaisesRegex(ValueError,'one generated home'):
            validate_generated(docs+[(Path('/project/example-en/duplicate.xml'),deepcopy(root))],r)
