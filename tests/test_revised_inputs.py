"""Protect actual supplied teaching content and case-specific scope, offline."""
import json
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'evals'))
from dg import revised_inputs as ri
from dg.package import CONDITIONS
from dg.revised_judge import judge_messages

@pytest.mark.parametrize('pid', CONDITIONS)
def test_runtime_and_review_folder_are_identical(pid):
    ri.verify_prepared(pid)
    package,messages,truth=ri.load_inputs(pid)
    assert len(truth['requests'])==13
    assert messages[0]['role']=='system'
    assert messages[1]['role']=='user'
    for filename in ('principles.md','learning-reference.md'):
        assert messages[1]['content'].count((ri.NEW_DOCS/filename).read_text().strip())==1
    assert messages[1]['content'].count('===== DOC-')==package.total_pages()
    assert json.loads((ri.NEW_DOCS/f'opus5.5/sets/{pid}/model-messages.json').read_text())==messages
    assert '# Answer Rubric: RPD Set One' not in messages[1]['content']
    assert 'objections_scope' not in messages[1]['content']
    assert 'Write your answer in exactly this structure' not in messages[0]['content']
    assert '<response_due_date>' not in messages[0]['content']

@pytest.mark.parametrize('pid', CONDITIONS)
def test_actual_rfp_scope_is_applied_without_old_r3_choice(pid):
    _,_,truth=ri.load_inputs(pid)
    key=truth['requests']['3']
    assert key['must_produce']==['DOC-005','DOC-006','DOC-007','DOC-008']
    assert [f['id'] for f in key['required_flags']]==['R3.b','R3.c']
    assert 'Definition 7' in truth['requests']['11']['_disposition_note']
    assert 'response_due_date' not in truth
    assert len(key['omission_checks'])==5


def test_t6_arrival_does_not_inherit_pending_retrieval_permission():
    _,_,truth=ri.load_inputs('T6')
    assert truth['requests']['1']['must_produce']==['DOC-003','DOC-024']
    note=truth['requests']['1']['_disposition_note']
    assert 'present' in note and 'wait for Bank' not in note
    assert len(ri.load_inputs('base')[2]['requests']['3']['required_flags'])==2


def test_judge_receives_exact_drafter_materials_not_prior_results():
    package,messages,truth=ri.load_inputs('base')
    answer='Response to Request 3: Produce DOC-005, DOC-006, DOC-007 and DOC-008. Counsel: confirm House 3 loan status.'
    output=judge_messages(package,messages,truth,answer)
    body=json.loads(output[1]['content'])
    assert body['exact_drafter_messages']==messages
    assert body['drafter_complete_response']==answer
    assert body['case_specific_key']['requests']['3']['must_produce']==truth['requests']['3']['must_produce']
    assert not any(k in body for k in ('author_findings','adjudications','lsat_diagnostics','previous_scores'))


def test_stale_prepared_inputs_block_execution(monkeypatch,tmp_path):
    monkeypatch.setattr(ri,'NEW_DOCS',tmp_path)
    monkeypatch.setattr(ri,'prepared_artifacts',lambda pid: (None,None,None,{'opus5.5/task-prompt.md':b'approved'}))
    path=tmp_path/'opus5.5/task-prompt.md';path.parent.mkdir();path.write_bytes(b'stale')
    with pytest.raises(ValueError,match='stale'):
        ri.verify_prepared('base')
