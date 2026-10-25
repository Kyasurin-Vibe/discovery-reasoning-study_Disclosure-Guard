"""Separate medium-effort pilot. No calls unless allow_api=true; base only."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'evals'))
from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.model import GenerateConfig, ModelOutput, ResponseSchema, get_model
from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import solver, generate
from inspect_ai.util import JSONSchema
from disclosure_guard_revised import as_messages, preflight, require_authorization
from dg.revised_inputs import input_hash, grading_hash
from judge_protocol import VERSION, response_schema, judge_messages, parse_and_validate
from dg.revised_judge import summarize

PROFILE = 'principles-example-open-medium-v2'
DRAFTER = 'anthropic/claude-opus-5-5'
JUDGE = 'anthropic/claude-fable-5-1'
# Medium is a new experimental configuration, not a proven equivalent to high.
CONFIG = GenerateConfig(effort='medium', max_tokens=64000, cache_prompt=False,
                        max_connections=1, max_retries=2)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def release_hash():
    manifest = json.loads((HERE / 'VERSION.json').read_text())
    for name, expected in manifest['files'].items():
        path = ROOT / name
        if not path.is_file() or sha(path.read_bytes()) != expected:
            raise ValueError('Optimized release mismatch: ' + name)
    return sha((HERE / 'VERSION.json').read_bytes())


def run_folder(name):
    if not isinstance(name, str) or not name or Path(name).name != name or name in ('.', '..'):
        raise ValueError('run_name must be a single new folder name')
    directory = HERE / 'runs' / name
    if not directory.resolve().is_relative_to((HERE / 'runs').resolve()):
        raise ValueError('Run folder cannot escape optimized-v2/runs')
    return directory


def load_source(directory, live=False):
    answer = (directory / 'base.txt').read_text()
    source = json.loads((directory / 'SOURCE.json').read_text())
    if not answer.strip() or source['answer_sha256'] != sha(answer.encode()):
        raise ValueError('Saved answer hash mismatch or empty answer')
    if source['profile'] != PROFILE or source['release_sha256'] != release_hash():
        raise ValueError('Saved answer belongs to another configuration/release')
    if live and source['response_source'] != 'live_api':
        raise ValueError('A fixture cannot substitute for a fresh live response')
    if source['stop_reason'] in ('max_tokens', 'model_length', 'refusal', 'tool_calls', 'content_filter'):
        raise ValueError('Draft is truncated or did not end normally; saved, but paid judging is blocked')
    if not source['stop_reason']:
        raise ValueError('Missing generation stop reason')
    return answer, source


@solver
def save_draft(directory):
    async def solve(state, generate):
        # Persist before any grading, even if the output was truncated.
        answer = state.output.completion
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError('Empty draft; no grading permitted')
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'base.txt').write_text(answer)
        dump(directory / 'model-output.json', state.output.model_dump(mode='json'))
        reason = state.output.choices[0].stop_reason if state.output.choices else None
        usage = state.output.usage.model_dump(mode='json') if state.output.usage else {}
        source = {**state.metadata, 'answer_sha256': sha(answer.encode()),
                  'model': state.output.model, 'requested_model': str(state.model),
                  'configured_defaults': CONFIG.model_dump(exclude_none=True),
                  'stop_reason': reason, 'usage': usage,
                  'saved_at': datetime.now(timezone.utc).isoformat(), 'sample_uuid': state.uuid}
        if str(state.model).startswith('mockllm/'):
            source['response_source'] = 'offline_fixture'
        dump(directory / 'SOURCE.json', source)
        state.metadata.update(answer_sha256=source['answer_sha256'], stop_reason=reason)
        return state
    return solve


@solver
def load_draft(directory, live):
    async def solve(state, generate):
        answer, source = load_source(directory, live)
        for field in ('input_sha256', 'grading_sha256', 'release_sha256'):
            if source[field] != state.metadata[field]:
                raise ValueError('Saved draft/source mismatch: ' + field)
        state.output = ModelOutput.from_content(model='saved-fresh-v2-answer', content=answer)
        state.messages.append(state.output.message)
        state.metadata.update(answer_sha256=source['answer_sha256'], generation_source=source)
        return state
    return solve


@scorer(metrics=[])
def optimized_judge(directory, judge):
    async def score(state, target: Target):
        package, messages, truth = preflight('base')
        if input_hash(messages) != state.metadata['input_sha256'] or grading_hash() != state.metadata['grading_sha256']:
            raise ValueError('Materials changed during execution')
        if release_hash() != state.metadata['release_sha256']:
            raise ValueError('Optimized release changed during execution')
        outfile = directory / 'judge-raw.txt'
        if outfile.exists():
            raise ValueError('Judge attempt already saved; no automatic paid re-grade')
        request_messages = judge_messages(package, messages, truth, state.output.completion)
        schema = response_schema(truth)
        dump(directory / 'judge-messages.json', request_messages)
        dump(directory / 'judge-schema.json', schema)
        usage = {}
        if judge.startswith('file:'):
            raw = Path(judge[5:]).read_text()
            judge_stop_reason = 'offline_fixture'
        else:
            cfg = CONFIG.model_copy(update={'response_schema': ResponseSchema(
                name='discovery_judge_v2', json_schema=JSONSchema.model_validate(schema), strict=True)})
            output = await get_model(judge, config=cfg).generate(as_messages(request_messages))
            raw = output.completion
            judge_stop_reason = output.choices[0].stop_reason if output.choices else None
            usage = output.usage.model_dump(mode='json') if output.usage else {}
            dump(directory / 'judge-model-output.json', output.model_dump(mode='json'))
        # Persist before parsing/validation. There is ONE report attempt, not two.
        outfile.write_text(raw)
        record, audit, problems = None, [], []
        try:
            record, audit, problems = parse_and_validate(raw, truth, package, state.output.completion)
        except (ValueError, KeyError, TypeError, AttributeError) as error:
            problems = [str(error)]
        if judge_stop_reason in ('max_tokens', 'model_length'):
            problems.append('judge reached output cap')
        summary = None if problems else summarize(record, truth)
        metadata = {'profile': PROFILE, 'transport_version': VERSION, 'judge': judge,
                    'input_sha256': state.metadata['input_sha256'],
                    'grading_sha256': state.metadata['grading_sha256'],
                    'release_sha256': state.metadata['release_sha256'],
                    'judge_input_sha256': input_hash(request_messages),
                    'answer_sha256': state.metadata['answer_sha256'],
                    'raw_judge_file': outfile.name, 'quote_alignments': audit,
                    'problems': problems, 'summary': summary, 'verdict': record,
                    'usage': usage, 'stop_reason': judge_stop_reason, 'report_attempts': 1}
        dump(directory / 'JUDGE_RESULT.json', metadata)
        status = 'REJECTED' if problems else 'PENDING REVIEW' if summary['status'] == 'REVIEW_REQUIRED' else 'PROPOSED'
        # This value is record validity only, never a legal/safety pass or quality score.
        return Score(value=0 if problems else 1, answer=status,
                     explanation=json.dumps({'problems': problems, 'summary': summary}), metadata=metadata)
    return score


@task
def disclosure_guard_optimized(stage: str = 'draft', run_name: str = 'base-v2',
                               judge: str = 'none', allow_api: bool = False):
    if stage not in ('draft', 'grade'):
        raise ValueError('stage must be draft or grade')
    if stage == 'draft' and judge != 'none':
        raise ValueError('Draft and save first. Grade separately to prevent loss or duplication.')
    if stage == 'grade' and judge == 'none':
        raise ValueError('Specify judge=default or an offline file: report')
    judge = JUDGE if judge == 'default' else judge
    require_authorization('saved-answer' if stage == 'grade' else '', judge, allow_api)
    release = release_hash()
    package, messages, truth = preflight('base')
    directory = run_folder(run_name)
    if stage == 'draft' and directory.exists():
        raise ValueError('Run folder already exists; inspect saved work, do not duplicate drafting')
    if stage == 'grade':
        load_source(directory, live=not judge.startswith('file:'))
        if (directory / 'judge-raw.txt').exists() or (directory / 'JUDGE_RESULT.json').exists():
            raise ValueError('Judge record already exists; no automatic duplicate grade')
    metadata = {'profile': PROFILE, 'original_input_profile': 'principles-example-open-v1',
                'package_id': 'base', 'stage': stage, 'input_sha256': input_hash(messages),
                'grading_sha256': grading_hash(), 'release_sha256': release,
                'response_source': 'live_api' if stage == 'draft' else 'saved_fresh_v2_answer',
                'configuration_change': 'medium effort; no prompt cache; serial; one judge report attempt'}
    sample = Sample(id='base', input=as_messages(messages), target='', metadata=metadata)
    return Task(dataset=MemoryDataset([sample]),
                solver=[generate(), save_draft(directory)] if stage == 'draft' else [load_draft(directory, not judge.startswith('file:'))],
                scorer=[] if stage == 'draft' else [optimized_judge(directory, judge)],
                config=CONFIG, metadata={'profile': PROFILE, 'stage': stage, 'live_calls_authorized': allow_api},
                version='optimized-v2')
