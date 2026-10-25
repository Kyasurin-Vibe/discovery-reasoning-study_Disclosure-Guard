"""Free-form judge review of the saved optimized-v2 base answer (author decision, 2026-10-24).

Author's design: the judge (Fable 5.1) receives the author's judge prompt (judge-prompt.md in this
folder: the original sentence plus what each supplied material is) and, as plain labelled text:
the sample answer, the rubric, the scoring guide, the case-specific key, the principles, the
learning example (Sacramento sample), the facts, the assigned RFP, all evidence, and Opus 5.5's
complete saved answer. Principles, learning example, facts, RFP and evidence are the exact text Opus
received. No JSON contract or schema. No format check decides whether the review has value: the raw
review is saved verbatim for the author. One call, no automatic re-grade. Opus is not re-run.

Free check (no API):  .venv/bin/python 'new docs/judge/free-review/runner.py' --check
Live (authorized only):
  .venv/bin/inspect eval 'new docs/judge/free-review/runner.py' --model mockllm/model -T allow_api=true \
      --max-connections 1 --max-retries 2 --log-dir 'new docs/judge/free-review/logs' --display plain
The mock task model is a placeholder; the scorer makes the one real Fable call.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'evals' / 'dg').is_dir())  # repository root
sys.path.insert(0, str(ROOT / 'evals'))
import dg.revised_judge as original  # noqa: E402
from dg.revised_inputs import grading_hash, input_hash, load_inputs, verify_prepared  # noqa: E402

ANSWER_DIR = ROOT / 'new docs' / 'optimized-v2' / 'runs' / 'base-v2'
OUT = HERE / 'runs' / 'base-v2-free'
JUDGE = 'anthropic/claude-fable-5-1'
PROFILE = 'free-review-v2-full-materials'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def saved_answer():
    answer = (ANSWER_DIR / 'base.txt').read_text()
    source = json.loads((ANSWER_DIR / 'SOURCE.json').read_text())
    if sha(answer.encode()) != source['answer_sha256']:
        raise ValueError('saved answer does not match its SOURCE.json hash')
    if source['stop_reason'] != 'stop':
        raise ValueError(f"saved answer did not end normally: {source['stop_reason']}")
    return answer, source


def free_messages():
    """The author's judge materials, as labelled plain text."""
    verify_prepared('base')
    package, messages, truth = load_inputs('base')
    answer, source = saved_answer()
    if input_hash(messages) != source['input_sha256']:
        raise ValueError('drafter input changed since the answer was generated')
    seen = messages[-1]['content']  # exactly what Opus received
    revised = original.REVISED
    sets = revised / 'opus5.5' / 'sets' / 'base'
    principles, learning = ((revised / f).read_text().strip() for f in ('principles.md', 'learning-reference.md'))
    facts, rfp, evidence = (
        (sets / f).read_text().strip() for f in ('facts.txt', 'request-for-production.txt', 'evidence-text.txt'))
    for name, text in (('principles', principles), ('learning example', learning), ('facts', facts),
                       ('rfp', rfp), ('evidence', evidence)):
        if text not in seen:
            raise ValueError(f'{name} is not verbatim what Opus received')
    key = {k: truth[k] for k in ('condition', 'scored_requests', 'requests', 'privileged_docs',
                                'equivalents', 'expected_change', 'pair_constraints') if k in truth}
    parts = [('SAMPLE ANSWER', (revised / 'judge' / 'reference-answers.md').read_text().strip()),
             ('RUBRIC', (revised / 'judge' / 'rubric.md').read_text().strip()),
             ('SCORING GUIDE', (revised / 'judge' / 'scoring-guide.md').read_text().strip()),
             ('CASE-SPECIFIC KEY', json.dumps(key, ensure_ascii=False, indent=2)),
             ('PRINCIPLES', principles),
             ('LEARNING EXAMPLE (Sacramento sample discovery response)', learning),
             ('FACTS', facts), ('REQUESTS FOR PRODUCTION (the questions answered)', rfp),
             ('ALL EVIDENCE', evidence), ("OPUS 5.5'S RESPONSE (to be evaluated)", answer.strip())]
    user = '\n\n'.join(f'########## {name} ##########\n\n{text}' for name, text in parts)
    prompt = (HERE / 'judge-prompt.md').read_text().strip()
    return [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': user}], answer, source


def check():
    msgs, answer, source = free_messages()
    system, user = msgs[0]['content'], msgs[1]['content']
    revised = original.REVISED
    seen = load_inputs('base')[1][-1]['content']
    report = {
        'system_is_author_prompt': system == (HERE / 'judge-prompt.md').read_text().strip(),
        'no_json_or_format_instruction': 'JSON' not in system and 'Return one' not in system,
        'has_sample_answer': (revised / 'judge' / 'reference-answers.md').read_text().strip() in user,
        'has_rubric': (revised / 'judge' / 'rubric.md').read_text().strip() in user,
        'has_scoring_guide': (revised / 'judge' / 'scoring-guide.md').read_text().strip() in user,
        'has_case_key': '########## CASE-SPECIFIC KEY ##########' in user and '"required_flags"' in user,
        'has_principles_and_learning_example_as_opus_saw_them': all(
            (revised / f).read_text().strip() in user and (revised / f).read_text().strip() in seen
            for f in ('principles.md', 'learning-reference.md')),
        'has_facts_rfp_evidence_as_opus_saw_them': all(
            (revised / 'opus5.5/sets/base' / f).read_text().strip() in user
            for f in ('facts.txt', 'evidence-text.txt', 'request-for-production.txt')),
        'has_full_opus_answer': answer.strip() in user,
        'report_format_not_sent': 'Top-level keys' not in user,
        'output_folder_free': not OUT.exists(),
    }
    print(json.dumps(report, indent=1))
    print('judge input: %d characters (~%d tokens)' % (len(system) + len(user), (len(system) + len(user)) * 0.47))
    print('answer_sha256', source['answer_sha256'], '| judge_request_sha256', sha(json.dumps(msgs, ensure_ascii=False).encode()))
    ok = all(report.values())
    print('FREE REVIEW CHECK', 'OK' if ok else 'FAILED')
    return ok


if __name__ == '__main__' and '--check' in sys.argv:
    sys.exit(0 if check() else 1)

from inspect_ai import Task, task  # noqa: E402
from inspect_ai.dataset import MemoryDataset, Sample  # noqa: E402
from inspect_ai.model import ChatMessageSystem, ChatMessageUser, GenerateConfig, ModelOutput, get_model  # noqa: E402
from inspect_ai.scorer import Score, Target, scorer  # noqa: E402
from inspect_ai.solver import solver  # noqa: E402

CONFIG = GenerateConfig(effort='medium', max_tokens=64000, cache_prompt=False, max_connections=1, max_retries=2)


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


@solver
def load_saved():
    async def solve(state, generate):
        _, answer, _ = free_messages()
        state.output = ModelOutput.from_content(model='saved-base-v2-answer', content=answer)
        state.messages.append(state.output.message)
        return state
    return solve


@scorer(metrics=[])
def free_review():
    async def score(state, target: Target):
        msgs, _, source = free_messages()
        OUT.mkdir(parents=True, exist_ok=False)  # never overwrite or repeat a review
        dump(OUT / 'judge-messages.json', msgs)
        output = await get_model(JUDGE, config=CONFIG).generate(
            [ChatMessageSystem(content=msgs[0]['content']), ChatMessageUser(content=msgs[1]['content'])])
        raw = output.completion or ''
        (OUT / 'review.md').write_text(raw)  # verbatim, unparsed, unvalidated
        dump(OUT / 'judge-model-output.json', output.model_dump(mode='json'))
        meta = {'profile': PROFILE, 'judge': JUDGE, 'config': CONFIG.model_dump(exclude_none=True),
                'stop_reason': output.choices[0].stop_reason if output.choices else None,
                'usage': output.usage.model_dump(mode='json') if output.usage else {},
                'answer_sha256': source['answer_sha256'], 'input_sha256': source['input_sha256'],
                'grading_sha256': grading_hash(), 'judge_request_sha256': sha(json.dumps(msgs, ensure_ascii=False).encode()),
                'answer_run_id_source': str(ANSWER_DIR / 'SOURCE.json'), 'saved_at': datetime.now(timezone.utc).isoformat(),
                'attempts': 1, 'format_check': 'none (author reviews the raw text)'}
        dump(OUT / 'RESULT.json', meta)
        return Score(value=1 if raw.strip() else 0, answer='SAVED FOR AUTHOR REVIEW', explanation=raw[:2000], metadata=meta)
    return score


@task
def free_review_base(allow_api: bool = False):
    if allow_api is not True:
        raise ValueError('Live judging requires allow_api=true')
    if OUT.exists():
        raise ValueError('A free review already exists; inspect it instead of repeating the paid call')
    msgs, _, source = free_messages()
    sample = Sample(id='base', input=msgs[1]['content'], target='',
                    metadata={'profile': PROFILE, 'answer_sha256': source['answer_sha256']})
    return Task(dataset=MemoryDataset([sample]), solver=[load_saved()], scorer=[free_review()],
                config=CONFIG, metadata={'profile': PROFILE}, version='free-review-v1')
