"""Offline only: no keys or provider calls. Fixtures are not research results."""
import copy
import importlib.util
import json
import sys
from pathlib import Path
import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT / 'evals'), str(ROOT / 'tests')]
import judge_protocol as protocol
from dg import revised_judge as old
from test_revised_judge import make_fixture, fixture_truth, FakePackage


def transport(record):
    r = copy.deepcopy(record)
    r.pop('schema_version')
    r['transport_version'] = protocol.VERSION
    r['requests'] = {row['request']: {k: v for k, v in row.items() if k != 'request'} for row in r['requests']}
    for row in r['requests'].values():
        for field in ('required_flags', 'omissions'):
            row[field] = {x['id']: {k: v for k, v in x.items() if k != 'id'} for x in row[field]}
        for error in row['severe_errors']:
            error.setdefault('flag_id', '')
    return r


def test_emphasis_only_quotes_restore_exact_original_and_are_audited():
    raw, record = make_fixture()
    quote = record['requests'][0]['required_flags'][0]['quote']
    raw = raw.replace(quote, '**Counsel-only note R1.a:**' + quote.split(':', 1)[1])
    aligned, audit = protocol.align_quotes(record, raw)
    assert audit and audit[0]['source_quote'] in raw
    assert record['requests'][0]['required_flags'][0]['quote'] == quote
    assert old.validate(aligned, fixture_truth(), FakePackage(), raw) == []


@pytest.mark.parametrize('raw,quote', [
    ('Produce DOC-001.', 'Do not produce DOC-001.'),
    ('Do not produce DOC-001.', 'Produce DOC-002.'),
    ('The amount is $20,000.', 'The amount is $2,000.'),
    ('**Never** had an account.', 'Ever had an account.'),
    ('There is no account.', 'There is an account.'),
    ('Ask counsel; then produce.', 'Ask counsel, then produce.'),
    ('`**literal**` text', 'literal text'),
])
def test_content_changes_are_not_repaired(raw, quote):
    record, audit = protocol.align_quotes({'quote': quote}, raw)
    assert not audit
    assert record['quote'] == quote


def test_mapped_transport_preserves_all_original_scores_and_required_ids():
    raw, record = make_fixture()
    adapted, audit, problems = protocol.parse_and_validate(json.dumps(transport(record)), fixture_truth(), FakePackage(), raw)
    assert not audit and not problems
    assert old.summarize(adapted, fixture_truth()) == old.summarize(record, fixture_truth())


def test_missing_required_id_is_rejected_not_filled_or_assumed_false():
    raw, record = make_fixture()
    r = transport(record)
    del r['requests']['1']['required_flags']['R1.b']
    with pytest.raises(ValueError, match='every reference ID'):
        protocol.parse_and_validate(json.dumps(r), fixture_truth(), FakePackage(), raw)


def test_unknown_required_id_and_duplicate_json_key_are_rejected():
    raw, record = make_fixture()
    r = transport(record)
    r['requests']['1']['required_flags']['R1.unknown'] = {'met': False, 'quote': ''}
    with pytest.raises(ValueError):
        protocol.parse_and_validate(json.dumps(r), fixture_truth(), FakePackage(), raw)
    with pytest.raises(ValueError, match='duplicate JSON'):
        old.parse_judge('{"a":1,"a":2}')


def test_schema_matches_record_and_requires_every_flag():
    import jsonschema
    schema = protocol.response_schema(fixture_truth())
    raw, record = make_fixture()
    jsonschema.validate(transport(record), schema)
    r = transport(record)
    del r['requests']['1']['required_flags']['R1.b']
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(r, schema)


def test_runner_defaults_are_separate_serial_and_no_paid_calls_without_permission():
    spec = importlib.util.spec_from_file_location('optimized_runner_tests', HERE / 'runner.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    assert runner.CONFIG.effort == 'medium'
    assert runner.CONFIG.max_tokens == 64000
    assert runner.CONFIG.cache_prompt is False
    assert runner.CONFIG.max_connections == 1
    assert runner.CONFIG.max_retries == 2
    with pytest.raises(ValueError, match='disabled'):
        runner.disclosure_guard_optimized()
    for name in ('../escape', '/tmp/escape', '..', ''):
        with pytest.raises(ValueError):
            runner.run_folder(name)


def test_real_failed_records_only_formatting_is_repaired_r12_b_remains_missing():
    from inspect_ai.log import read_eval_log
    from dg.revised_inputs import load_inputs
    logfiles = list((ROOT / 'runs/revised-pilot/grading').glob('*.eval'))
    if not logfiles:
        pytest.skip('Local paid logs not present; not required for portable fixture tests')
    log = read_eval_log(logfiles[0])
    attempts = log.samples[0].scores['revised_judge_score'].metadata['attempts']
    answer = (ROOT / 'runs/revised-pilot/answers/base.txt').read_text()
    package, _, truth = load_inputs('base')
    count = 0
    for attempt in attempts:
        record = old.parse_judge(attempt['raw'])
        aligned, audit = protocol.align_quotes(record, answer)
        errors = old.validate(aligned, truth, package, answer)
        assert errors == ['request 12: required_flags IDs must each match the key exactly once']
        assert all(a['source_quote'] in answer for a in audit)
        assert all(f['id'] != 'R12.b' for row in aligned['requests'] if row['request'] == '12' for f in row['required_flags'])
        count += len(audit)
    assert count == 14


def test_full_real_keys_compile_without_changing_scoring_semantics():
    from dg.revised_inputs import load_inputs
    import jsonschema
    for pid in ('base', 'T5'):
        package, _, truth = load_inputs(pid)
        raw, record = make_fixture(truth)
        keyed = transport(record)
        jsonschema.validate(keyed, protocol.response_schema(truth))
        result, _, problems = protocol.parse_and_validate(json.dumps(keyed), truth, package, raw)
        assert not problems
        assert old.summarize(result, truth) == old.summarize(record, truth)


def test_source_blocks_truncated_or_fixture_answer_before_live_grading(tmp_path, monkeypatch):
    import runner
    monkeypatch.setattr(runner, 'release_hash', lambda: 'release')
    answer = 'Saved answer'
    (tmp_path / 'base.txt').write_text(answer)
    source = {'answer_sha256': runner.sha(answer.encode()), 'profile': runner.PROFILE,
              'release_sha256': 'release', 'response_source': 'live_api', 'stop_reason': 'max_tokens'}
    (tmp_path / 'SOURCE.json').write_text(json.dumps(source))
    with pytest.raises(ValueError, match='truncated'):
        runner.load_source(tmp_path, live=True)
    source.update(stop_reason='stop', response_source='offline_fixture')
    (tmp_path / 'SOURCE.json').write_text(json.dumps(source))
    with pytest.raises(ValueError, match='fixture'):
        runner.load_source(tmp_path, live=True)
    source['response_source'] = 'live_api'
    (tmp_path / 'SOURCE.json').write_text(json.dumps(source))
    assert runner.load_source(tmp_path, live=True)[0] == answer
    (tmp_path / 'base.txt').write_text('Changed')
    with pytest.raises(ValueError, match='hash mismatch'):
        runner.load_source(tmp_path, live=True)


def test_two_stage_mock_flow_saves_before_grading_and_blocks_duplicates(tmp_path, monkeypatch):
    """Exercise actual Inspect plumbing with a fake drafter and a file judge."""
    import runner
    monkeypatch.setenv('INSPECT_TRACE_FILE', str(tmp_path / 'inspect-trace.log'))
    import inspect_ai._util.appdirs as appdirs
    monkeypatch.setattr(appdirs, 'user_data_path', lambda *args, **kwargs: tmp_path / 'appdata')
    monkeypatch.setattr(appdirs, 'user_cache_path', lambda *args, **kwargs: tmp_path / 'appcache')
    from inspect_ai import eval as run_eval
    from inspect_ai.model import get_model, ModelOutput
    from dg.revised_inputs import load_inputs
    monkeypatch.setattr(runner, 'release_hash', lambda: 'offline-test-release')
    folder = tmp_path / 'answer'
    monkeypatch.setattr(runner, 'run_folder', lambda _: folder)
    package, _, truth = load_inputs('base')
    answer, record = make_fixture(truth)
    fake = get_model('mockllm/model', custom_outputs=[ModelOutput.from_content('mockllm/model', answer)])
    logs = run_eval(runner.disclosure_guard_optimized(stage='draft', allow_api=True),
                    model=fake, log_dir=str(tmp_path / 'generation'), display='none')
    assert logs[0].status == 'success'
    source = json.loads((folder / 'SOURCE.json').read_text())
    assert source['response_source'] == 'offline_fixture'
    assert source['answer_sha256'] == runner.sha(answer.encode())
    with pytest.raises(ValueError, match='already exists'):
        runner.disclosure_guard_optimized(stage='draft', allow_api=True)
    judge_file = tmp_path / 'fixture.json'
    judge_file.write_text(json.dumps(transport(record)))
    task = runner.disclosure_guard_optimized(stage='grade', judge='file:' + str(judge_file))
    logs = run_eval(task, model='mockllm/model', log_dir=str(tmp_path / 'grade'), display='none')
    assert logs[0].status == 'success'
    result = json.loads((folder / 'JUDGE_RESULT.json').read_text())
    assert not result['problems']
    assert result['summary']['quality_points'] == 78
    assert result['report_attempts'] == 1
    with pytest.raises(ValueError, match='already exists'):
        runner.disclosure_guard_optimized(stage='grade', judge='file:' + str(judge_file))
