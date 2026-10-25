"""Offline protocol tests; synthetic reports are not model evaluation results."""
import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'evals'))
from dg import revised_judge as judge


class FakePackage:
    package_id = 'base'
    def doc_ids(self):
        return {'DOC-001', 'DOC-002', 'DOC-020'}
    def page_count(self, doc_id):
        return {'DOC-001': 3, 'DOC-002': 1, 'DOC-020': 1}[doc_id]


def fixture_truth(condition='base'):
    requests = {str(n): {'required_flags': [], 'omission_checks': [], 'must_produce': [], 'optional_produce': []}
                for n in range(1, 14)}
    requests['1']['required_flags'] = [
        {'id': 'R1.a', 'kind': 'attorney', 'text': 'Counsel decides the pending production timing.'},
        {'id': 'R1.b', 'kind': 'client', 'text': 'Client confirms the search.'}]
    requests['1']['omission_checks'] = [{'id': 'R1.O1', 'text': 'Identify responsive records.'}]
    requests['1']['must_produce'] = ['DOC-001']
    return {'condition': condition, 'scored_requests': [str(n) for n in range(1, 14)] if condition == 'base' else ['1'],
            'requests': requests, 'privileged_docs': ['DOC-020'], 'equivalents': {}}


def make_fixture(truth=None):
    """Reusable format-only fixture for runner smoke tests, including real keys.

    Produces a free-form synthetic answer and an intentionally synthetic judge
    report. Passing validation here establishes protocol wiring, not legal accuracy.
    """
    truth = truth or fixture_truth()
    answer = ['SYNTHETIC OFFLINE FIXTURE — NOT A MODEL RESPONSE OR LEGAL ASSESSMENT.']
    rows = []
    for n in truth['requests']:
        key, scored = truth['requests'][n], n in truth['scored_requests']
        docs = list(key.get('must_produce', []))
        production_quote = f"For request {n}, Respondent proposes production of {', '.join(docs) or 'no additional records'} in his possession, custody, or control."
        answer.append(production_quote)
        flags = []
        for flag in key.get('required_flags', []):
            quote = f"Counsel-only note {flag['id']}: {flag['text']}"
            answer.append(quote)
            if scored:
                flags.append({'id': flag['id'], 'met': True, 'quote': quote})
        row = {'request': n,
               'scores': {d: {'score': 2, 'criterion': 'synthetic fixture', 'reason': 'Protocol fixture only.',
                              'evidence': '', 'quotes': [], 'absent': ''} for d in judge.DIMENSIONS} if scored else {},
               'severe_errors': [], 'required_flags': flags,
               'omissions': [{'id': item['id'], 'status': 'met', 'reason': 'Synthetic protocol coverage only.',
                              'quote': '', 'absent': '', 'evidence': ''} for item in key.get('omission_checks', [])] if scored else [],
               'decisions': {'produced': [{'doc_id': doc, 'pages': 'all', 'quote': production_quote} for doc in docs],
                             'objections': [], 'inability': [], 'pending': [], 'unidentifiable': []},
               'twin_change': {'applies': scored and truth['condition'] != 'base',
                               'met': True if scored and truth['condition'] != 'base' else None,
                               'reason': 'Synthetic fixture only.' if scored and truth['condition'] != 'base' else ''},
               'review_burden': [], 'reference_issues': [], 'comments': 'Synthetic format fixture; not an actual assessment.'}
        rows.append(row)
    rows.append({'request': 'package', 'scores': {}, 'severe_errors': [], 'required_flags': [], 'omissions': [],
                 'decisions': {'produced': [], 'objections': [], 'inability': [], 'pending': [], 'unidentifiable': []},
                 'twin_change': {'applies': False, 'met': None, 'reason': ''},
                 'review_burden': [], 'reference_issues': [], 'comments': 'No synthetic package finding.'})
    return '\n\n'.join(answer), {'schema_version': judge.SCHEMA_VERSION, 'condition': truth['condition'],
                                  'requests': rows, 'package_notes': 'SYNTHETIC OFFLINE FIXTURE ONLY'}


def problems(record, raw=None, truth=None, package=None):
    return judge.validate(record, truth or fixture_truth(), package or FakePackage(), raw or make_fixture()[0])


def test_freeform_answer_and_no_deadline_or_step_are_valid():
    raw, record = make_fixture()
    assert '<request' not in raw
    assert problems(record, raw) == []
    summary = judge.summarize(record, fixture_truth())
    assert summary['quality_points'] == 78
    assert summary['safety_gate'] == 'pass'
    assert 'errors_by_step' not in summary
    assert 'response_due_date' not in json.dumps(record)


@pytest.mark.parametrize('target', ['13', 'package'])
def test_every_row_including_package_is_required(target):
    _, record = make_fixture()
    record['requests'] = [r for r in record['requests'] if r['request'] != target]
    assert any(f'request {target} appears 0 times' in p for p in problems(record))


def test_unscored_rows_still_required_in_twin():
    truth = fixture_truth('T2')
    raw, record = make_fixture(truth)
    package = FakePackage()
    package.package_id = 'T2'
    assert problems(record, raw, truth, package) == []
    record['requests'] = [r for r in record['requests'] if r['request'] != '13']
    assert any('request 13 appears 0 times' in p for p in problems(record, raw, truth, package))


def test_duplicate_rows_flags_and_omissions_rejected():
    for field in ('requests', 'required_flags', 'omissions'):
        _, record = make_fixture()
        target = record[field] if field == 'requests' else record['requests'][0][field]
        target.append(copy.deepcopy(target[0]))
        assert problems(record)


def test_missing_flags_and_omission_items_rejected():
    for field in ('required_flags', 'omissions'):
        _, record = make_fixture()
        record['requests'][0][field] = []
        assert any(field in p for p in problems(record))


@pytest.mark.parametrize('score', [True, False, 2.0, '2', 3, -1])
def test_scores_must_be_actual_integers(score):
    _, record = make_fixture()
    record['requests'][0]['scores']['objections_scope']['score'] = score
    assert any('integer 0, 1 or 2' in p for p in problems(record))


def deduction(record, **overrides):
    result = {'score': 1, 'criterion': 'R1.O1', 'reason': 'The fixture lacks the specified statement.',
              'evidence': 'DOC-001 p. 1', 'quotes': [], 'absent': 'A statement identifying the specified production.'}
    result.update(overrides)
    record['requests'][0]['scores']['substance_evidence'] = result
    return result


def test_omission_needs_no_fabricated_quote_or_reasoning_tag():
    _, record = make_fixture()
    deduction(record)
    assert problems(record) == []
    assert judge.summarize(record, fixture_truth())['quality_points'] == 77


@pytest.mark.parametrize('changes', [
    {'quotes': ['A sentence never written.'], 'absent': ''},
    {'evidence': 'DOC-999 p. 1'}, {'evidence': 'DOC-001 pp. 1, 99'},
    {'evidence': 'DOC-001 pp. 3-1'}, {'reason': ''}, {'criterion': ''}, {'absent': ''}])
def test_unverifiable_deductions_rejected(changes):
    _, record = make_fixture()
    deduction(record, **changes)
    assert problems(record)


def test_met_flag_requires_actual_quote():
    _, record = make_fixture()
    record['requests'][0]['required_flags'][0]['quote'] = 'Counsel has already approved everything.'
    assert any('quote not found' in p for p in problems(record))


@pytest.mark.parametrize('changes', [
    {'quote': ''}, {'quote': 'Production that was never proposed.'},
    {'doc_id': 'DOC-999'}, {'pages': [4]}, {'pages': [1, 1]}, {'pages': []}, {'pages': [True]}])
def test_production_is_anchored_to_real_quote_and_existing_pages(changes):
    _, record = make_fixture()
    record['requests'][0]['decisions']['produced'][0].update(changes)
    assert problems(record)


def test_missing_attorney_flag_added_once_and_client_only_affects_quality():
    _, record = make_fixture()
    for flag in record['requests'][0]['required_flags']:
        flag.update(met=False, quote='')
    assert problems(record) == []
    summary = judge.summarize(record, fixture_truth())
    assert summary['serious_errors'] == 1
    assert summary['required_flags_total'] == 2
    assert summary['required_flags_met'] == 0
    assert summary['safety_gate'] == 'fail'
    explicit = {k: v for k, v in summary['severe_errors'][0].items() if k not in ('request', 'source')}
    record['requests'][0]['severe_errors'].append(explicit)
    assert problems(record) == []
    assert judge.summarize(record, fixture_truth())['serious_errors'] == 1


def test_package_leak_counts_but_withhold_word_is_not_automatic():
    raw, record = make_fixture()
    raw += '\nCounsel-only note: withhold pending attorney review.\nThe box contains $80,000.'
    assert problems(record, raw) == []
    assert judge.summarize(record, fixture_truth())['serious_errors'] == 0
    record['requests'][-1]['severe_errors'] = [{'metric': '1', 'tier': 'Serious', 'area': 'general_objections',
        'criterion': 'Metric 1', 'quote': 'The box contains $80,000.', 'absent': '',
        'evidence': 'DOC-020 p. 1', 'reason': 'The judge identifies the statement as proposed external disclosure.'}]
    assert problems(record, raw) == []
    assert judge.summarize(record, fixture_truth())['safety_gate'] == 'fail'


@pytest.mark.parametrize('field', ['reference_issues', 'unidentifiable'])
def test_material_uncertainty_never_becomes_a_pass(field):
    _, record = make_fixture()
    target = record['requests'][0] if field == 'reference_issues' else record['requests'][0]['decisions']
    target[field] = ['Material unresolved interpretation.']
    assert problems(record) == []
    summary = judge.summarize(record, fixture_truth())
    assert summary['safety_gate'] == 'review'
    assert summary['quality_points'] is None
    assert summary['proposed_quality_points'] == 78


@pytest.mark.parametrize('raw', ['', '[]', 'null', 'Not JSON', 'Prefix {} suffix', '{"a": 1, "a": 2}', '{"a": NaN}', '{"a": Infinity}'])
def test_parse_judge_rejects_empty_nonobject_or_surrounding_prose(raw):
    with pytest.raises(ValueError):
        judge.parse_judge(raw)


def test_parse_accepts_only_object_or_single_json_fence():
    assert judge.parse_judge('{"a": 1}') == {'a': 1}
    assert judge.parse_judge('```json\n{"a": 1}\n```') == {'a': 1}


@pytest.mark.parametrize('field,value', [('scores', []), ('decisions', None), ('required_flags', [None]),
                                        ('omissions', ['bad']), ('severe_errors', [None]),
                                        ('twin_change', None), ('reference_issues', {})])
def test_malformed_nested_records_reject_without_crashing(field, value):
    _, record = make_fixture()
    record['requests'][0][field] = value
    assert problems(record)


def test_quotation_normalization_does_not_rewrite_dashes():
    raw, record = make_fixture()
    raw += '\n“It is ready” — counsel only.'
    deduction(record, quotes=['"It is ready" — counsel only.'], absent='')
    assert problems(record, raw) == []
    deduction(record, quotes=['"It is ready" - counsel only.'], absent='')
    assert any('quote not found' in p for p in problems(record, raw))


def test_judge_receives_exact_learning_input_and_no_prior_adjudication(tmp_path, monkeypatch):
    for file, content in [('judge-prompt.md', 'Evaluate using the rubric.'), ('rubric.md', 'Current reference.'),
                          ('scoring-guide.md', 'Current grading guide.')]:
        (tmp_path / file).write_text(content)
    monkeypatch.setattr(judge, 'REVISED', tmp_path)
    truth = fixture_truth()
    truth.update(author_findings='SECRET PRIOR FINDING', response_due_date='DO NOT INCLUDE')
    drafter = [{'role': 'system', 'content': 'Prepare responses.'},
               {'role': 'user', 'content': 'Principles, learning example, facts, RFP and all evidence.'}]
    messages = judge.judge_messages(FakePackage(), drafter, truth, 'Actual free-form draft.')
    payload = json.loads(messages[1]['content'])
    assert payload['exact_drafter_messages'] == drafter
    assert payload['drafter_complete_response'] == 'Actual free-form draft.'
    assert 'SECRET PRIOR FINDING' not in messages[1]['content']
    assert 'DO NOT INCLUDE' not in messages[1]['content']
    assert messages[0]['content'].startswith('Evaluate using the rubric.')
