"""Free-form Fable review of the saved Opus answers for T1-T7 (author design, 2026-10-24).

Same design and settings as the completed base review (new docs/judge/free-review): the author's
judge prompt (the original sentence plus what each material is) and ten labelled plain-text
materials, all specific to the package: sample answer, rubric, scoring guide, the variant's
case-specific key, principles, learning example (Sacramento excerpt), facts, the actual RFP,
complete evidence, and that package's saved Opus answer (new docs/opus-all-v1/runs/<pid>).
Principles, learning example, facts, RFP and evidence are verified verbatim against what Opus
received for that package. No output template, format gate or new scoring rule; the raw review is
saved verbatim for the author. One call per package, no automatic re-grade. Base is not handled
here (its review already exists) and Opus is never re-run.

Free check (no API):     .venv/bin/python 'new docs/judge/free-review-all-v1/runner.py' --check
Freeze (no API, once):   .venv/bin/python 'new docs/judge/free-review-all-v1/runner.py' --freeze
Live, one package (authorized only; relative paths, from the project root):
  .venv/bin/inspect eval 'new docs/judge/free-review-all-v1/runner.py' --model mockllm/model \
      -T package=T1 -T allow_api=true --max-connections 1 --max-retries 2 \
      --log-dir 'new docs/judge/free-review-all-v1/logs/T1' --display plain
The mock task model is a placeholder; the scorer makes the one real Fable call.
"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'evals' / 'dg').is_dir())  # repository root
sys.path.insert(0, str(ROOT / 'evals'))
from dg.revised_inputs import grading_hash, input_hash, load_inputs, verify_prepared  # noqa: E402

NEW_DOCS = ROOT / 'new docs'
PROMPT = NEW_DOCS / 'judge' / 'free-review' / 'judge-prompt.md'  # the prompt used for the base review
ANSWERS = NEW_DOCS / 'opus-all-v1' / 'runs'
PACKAGES = [f'T{i}' for i in range(1, 8)]
JUDGE = 'anthropic/claude-fable-5-1'
PROFILE = 'free-review-all-v1-full-materials'
FREEZE = HERE / 'FREEZE.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def out_dir(pid):
    if pid not in PACKAGES:
        raise ValueError('only T1-T7; the base review already exists')
    return HERE / 'runs' / pid


def saved_answer(pid):
    folder = ANSWERS / pid
    answer = (folder / f'{pid}.txt').read_text()
    source = json.loads((folder / 'SOURCE.json').read_text())
    if sha(answer.encode()) != source['answer_sha256']:
        raise ValueError(f'{pid}: saved answer does not match its SOURCE.json hash')
    if source.get('package_id') != pid:
        raise ValueError(f'{pid}: saved answer belongs to {source.get("package_id")}')
    if source['stop_reason'] != 'stop':
        raise ValueError(f'{pid}: saved answer did not end normally')
    return answer, source


def materials(pid):
    """The ten labelled materials for one package, each checked against that package."""
    verify_prepared(pid)
    package, messages, truth = load_inputs(pid)
    if truth.get('condition') != pid or package.package_id != pid:
        raise ValueError(f'{pid}: key or package belongs to another condition')
    answer, source = saved_answer(pid)
    if input_hash(messages) != source['input_sha256']:
        raise ValueError(f'{pid}: drafter input changed since the answer was generated')
    seen = messages[-1]['content']  # exactly what Opus received for this package
    sets = NEW_DOCS / 'opus5.5' / 'sets' / pid
    principles, learning = ((NEW_DOCS / f).read_text().strip() for f in ('principles.md', 'learning-reference.md'))
    facts, rfp, evidence = ((sets / f).read_text().strip()
                            for f in ('facts.txt', 'request-for-production.txt', 'evidence-text.txt'))
    for name, text in (('principles', principles), ('learning example', learning), ('facts', facts),
                       ('rfp', rfp), ('evidence', evidence)):
        if text not in seen:
            raise ValueError(f'{pid}: {name} is not verbatim what Opus received')
    key = {k: truth[k] for k in ('condition', 'scored_requests', 'requests', 'privileged_docs',
                                'equivalents', 'expected_change', 'pair_constraints') if k in truth}
    return [('SAMPLE ANSWER', (NEW_DOCS / 'judge' / 'reference-answers.md').read_text().strip()),
            ('RUBRIC', (NEW_DOCS / 'judge' / 'rubric.md').read_text().strip()),
            ('SCORING GUIDE', (NEW_DOCS / 'judge' / 'scoring-guide.md').read_text().strip()),
            ('CASE-SPECIFIC KEY', json.dumps(key, ensure_ascii=False, indent=2)),
            ('PRINCIPLES', principles),
            ('LEARNING EXAMPLE (Sacramento sample discovery response)', learning),
            ('FACTS', facts), ('REQUESTS FOR PRODUCTION (the questions answered)', rfp),
            ('ALL EVIDENCE', evidence), ("OPUS 5.5'S RESPONSE (to be evaluated)", answer.strip())], source


def free_messages(pid):
    parts, source = materials(pid)
    user = '\n\n'.join(f'########## {name} ##########\n\n{text}' for name, text in parts)
    return [{'role': 'system', 'content': PROMPT.read_text().strip()}, {'role': 'user', 'content': user}], source


def request_hash(msgs):
    return sha(json.dumps(msgs, ensure_ascii=False).encode())


def frozen_files():
    names = [HERE / 'runner.py', PROMPT, NEW_DOCS / 'principles.md', NEW_DOCS / 'learning-reference.md',
             NEW_DOCS / 'judge' / 'reference-answers.md', NEW_DOCS / 'judge' / 'rubric.md',
             NEW_DOCS / 'judge' / 'scoring-guide.md']
    for pid in PACKAGES:
        names += [NEW_DOCS / 'opus5.5' / 'sets' / pid / f for f in ('facts.txt', 'request-for-production.txt',
                                                                    'evidence-text.txt', 'model-messages.json')]
        names += [ANSWERS / pid / f'{pid}.txt', ANSWERS / pid / 'SOURCE.json']
    return {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in names}


def verify_freeze():
    if not FREEZE.exists():
        raise ValueError('not frozen yet: run --freeze after a passing --check')
    frozen = json.loads(FREEZE.read_text())
    for name, h in frozen['files'].items():
        if sha((ROOT / name).read_bytes()) != h:
            raise ValueError('frozen file changed: ' + name)
    return frozen


def check():
    ok = True
    base_answer = (NEW_DOCS / 'optimized-v2' / 'runs' / 'base-v2' / 'base.txt').read_text().strip()
    for pid in PACKAGES:
        msgs, source = free_messages(pid)
        system, user = msgs[0]['content'], msgs[1]['content']
        others = [p for p in PACKAGES if p != pid]
        r = {
            'prompt_is_base_review_prompt': system == PROMPT.read_text().strip()
                and 'JSON' not in system and 'Return one' not in system,
            'ten_materials_in_order': re.findall(r'^########## (.+?) ##########$', user, re.M) == [
                'SAMPLE ANSWER', 'RUBRIC', 'SCORING GUIDE', 'CASE-SPECIFIC KEY', 'PRINCIPLES',
                'LEARNING EXAMPLE (Sacramento sample discovery response)', 'FACTS',
                'REQUESTS FOR PRODUCTION (the questions answered)', 'ALL EVIDENCE', "OPUS 5.5'S RESPONSE (to be evaluated)"],
            'key_is_this_variant': f'"condition": "{pid}"' in user,
            'answer_is_this_package': (ANSWERS / pid / f'{pid}.txt').read_text().strip() in user,
            'not_base_answer': base_answer not in user,
            'no_other_variant_answer': not any((ANSWERS / o / f'{o}.txt').read_text().strip()[:2000] in user for o in others),
            'output_folder_free': not out_dir(pid).exists(),
        }
        tokens = int((len(system) + len(user)) * 0.44)
        print(f"{pid}: {'OK' if all(r.values()) else 'FAILED ' + str([k for k, v in r.items() if not v])}"
              f" | ~{tokens:,} input tokens | answer {source['answer_sha256'][:12]} | request {request_hash(msgs)[:12]}")
        ok &= all(r.values())
    # Duplicate guard: an existing output folder must block a live call.
    import tempfile
    global HERE
    real = HERE
    with tempfile.TemporaryDirectory() as tmp:
        HERE = Path(tmp)
        (HERE / 'runs' / 'T1').mkdir(parents=True)
        try:
            blocked = False
            try:
                _guard('T1')
            except ValueError:
                blocked = True
        finally:
            HERE = real
    print('duplicate call blocked when output exists:', blocked)
    try:
        out_dir('base')
        base_blocked = False
    except ValueError:
        base_blocked = True
    print('base refused (already reviewed):', base_blocked)
    ok &= blocked and base_blocked
    print('FREE REVIEW ALL CHECK', 'OK' if ok else 'FAILED')
    return ok


def _guard(pid):
    if (HERE / 'runs' / pid).exists():
        raise ValueError(f'{pid}: a review already exists or is in flight; no duplicate paid call')


if __name__ == '__main__' and ('--check' in sys.argv or '--freeze' in sys.argv):
    passed = check()
    if '--freeze' in sys.argv:
        if not passed:
            sys.exit('check failed; not freezing')
        if FREEZE.exists():
            sys.exit('FREEZE.json exists; refusing to overwrite')
        requests = {pid: request_hash(free_messages(pid)[0]) for pid in PACKAGES}
        FREEZE.write_text(json.dumps({'version': 'free-review-all-v1', 'created_at': datetime.now(timezone.utc).isoformat(),
                                      'judge': JUDGE, 'config': {'effort': 'medium', 'max_tokens': 64000,
                                                                 'cache_prompt': False, 'max_connections': 1, 'max_retries': 2},
                                      'packages': PACKAGES, 'judge_request_sha256': requests,
                                      'grading_sha256': grading_hash(), 'files': frozen_files()}, indent=1) + '\n')
        verify_freeze()
        print('FROZEN:', FREEZE.relative_to(ROOT))
    sys.exit(0 if passed else 1)

from inspect_ai import Task, task  # noqa: E402
from inspect_ai.dataset import MemoryDataset, Sample  # noqa: E402
from inspect_ai.model import ChatMessageSystem, ChatMessageUser, GenerateConfig, ModelOutput, get_model  # noqa: E402
from inspect_ai.scorer import Score, Target, scorer  # noqa: E402
from inspect_ai.solver import solver  # noqa: E402

CONFIG = GenerateConfig(effort='medium', max_tokens=64000, cache_prompt=False, max_connections=1, max_retries=2)


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


@solver
def load_saved(pid):
    async def solve(state, generate):
        answer, _ = saved_answer(pid)
        state.output = ModelOutput.from_content(model=f'saved-{pid}-answer', content=answer)
        state.messages.append(state.output.message)
        return state
    return solve


@scorer(metrics=[])
def free_review(pid):
    async def score(state, target: Target):
        frozen = verify_freeze()
        msgs, source = free_messages(pid)
        if request_hash(msgs) != frozen['judge_request_sha256'][pid]:
            raise ValueError(f'{pid}: judge request differs from the frozen request')
        out = out_dir(pid)
        out.mkdir(parents=True, exist_ok=False)  # never overwrite or repeat a review
        dump(out / 'judge-messages.json', msgs)
        output = await get_model(JUDGE, config=CONFIG).generate(
            [ChatMessageSystem(content=msgs[0]['content']), ChatMessageUser(content=msgs[1]['content'])])
        raw = output.completion or ''
        (out / 'review.md').write_text(raw)  # verbatim, unparsed, unvalidated
        dump(out / 'judge-model-output.json', output.model_dump(mode='json'))
        meta = {'profile': PROFILE, 'package_id': pid, 'judge': JUDGE, 'config': CONFIG.model_dump(exclude_none=True),
                'stop_reason': output.choices[0].stop_reason if output.choices else None,
                'usage': output.usage.model_dump(mode='json') if output.usage else {},
                'answer_sha256': source['answer_sha256'], 'input_sha256': source['input_sha256'],
                'judge_request_sha256': request_hash(msgs), 'freeze_sha256': sha(FREEZE.read_bytes()),
                'saved_at': datetime.now(timezone.utc).isoformat(), 'attempts': 1,
                'format_check': 'none (author reviews the raw text)'}
        dump(out / 'RESULT.json', meta)
        return Score(value=1 if raw.strip() else 0, answer='SAVED FOR AUTHOR REVIEW', explanation=raw[:2000], metadata=meta)
    return score


@task
def review_package(package: str = 'T1', allow_api: bool = False):
    if allow_api is not True:
        raise ValueError('Live judging requires allow_api=true')
    out_dir(package)  # refuses base and anything outside T1-T7
    _guard(package)
    verify_freeze()
    msgs, source = free_messages(package)
    sample = Sample(id=package, input=msgs[1]['content'], target='',
                    metadata={'profile': PROFILE, 'package_id': package, 'answer_sha256': source['answer_sha256']})
    return Task(dataset=MemoryDataset([sample]), solver=[load_saved(package)], scorer=[free_review(package)],
                config=CONFIG, metadata={'profile': PROFILE, 'package_id': package}, version='free-review-all-v1')
