"""Opus-only continuation; unchanged prepared inputs and medium configuration."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'evals'))
from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.model import GenerateConfig
from inspect_ai.solver import generate, solver
from disclosure_guard_revised import as_messages, preflight
from dg.revised_inputs import input_hash, grading_hash

MODEL = 'anthropic/claude-opus-5-5'
CONFIG = GenerateConfig(effort='medium', max_tokens=64000, cache_prompt=False, max_connections=1, max_retries=2)
PROFILE = 'principles-example-open-medium-v2'
IDS = ['base'] + [f'T{i}' for i in range(1,8)]
def sha(data): return hashlib.sha256(data).hexdigest()
def dump(path, data): path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
def verify():
    manifest = json.loads((HERE/'FREEZE.json').read_text())
    for name, expected in manifest['files'].items():
        if sha((ROOT/name).read_bytes()) != expected: raise ValueError('Frozen file changed: '+name)
    for pid in IDS:
        _, messages, _ = preflight(pid)
        if input_hash(messages) != manifest['inputs'][pid]: raise ValueError('Input changed: '+pid)
    return sha((HERE/'FREEZE.json').read_bytes())
def existing_base():
    folder = ROOT/'new docs/optimized-v2/runs/base-v2'
    source = json.loads((folder/'SOURCE.json').read_text())
    answer = (folder/'base.txt').read_text()
    _, messages, _ = preflight('base')
    assert source['answer_sha256'] == sha(answer.encode())
    assert source['input_sha256'] == input_hash(messages)
    assert source['stop_reason'] == 'stop' and source['response_source'] == 'live_api'
    assert source['model'] == 'claude-opus-5-5'
    assert source['configured_defaults'] == CONFIG.model_dump(exclude_none=True)
    return folder, source

@solver
def save_answer(folder, pid, release):
    async def solve(state, generate):
        if str(state.model) != MODEL: raise ValueError('Unexpected model')
        # Keep the original complete output even when truncated; never auto-regenerate.
        answer = state.output.completion
        (folder/f'{pid}.txt').write_text(answer)
        dump(folder/'model-output.json', state.output.model_dump(mode='json'))
        dump(folder/'SOURCE.json', {**state.metadata,
            'answer_sha256':sha(answer.encode()), 'model':state.output.model,
            'configured_defaults': CONFIG.model_dump(exclude_none=True),
            'stop_reason':state.output.choices[0].stop_reason if state.output.choices else None,
            'usage':state.output.usage.model_dump(mode='json') if state.output.usage else {},
            'sample_uuid':state.uuid, 'saved_at':datetime.now(timezone.utc).isoformat()})
        return state
    return solve

@task
def opus_only(package: str='T1', allow_api: bool=False):
    if allow_api is not True: raise ValueError('Paid generation requires allow_api=true')
    if package not in IDS[1:]: raise ValueError('Base already complete; only T1–T7 allowed')
    release = verify()
    existing_base()
    _, messages, _ = preflight(package)
    folder = HERE/'runs'/package
    # Reserve before calling the model: any existing/in-flight folder blocks retries.
    folder.mkdir(parents=True, exist_ok=False)
    metadata = {'profile':PROFILE,'package_id':package,'response_source':'live_api',
        'input_sha256':input_hash(messages),'grading_sha256':grading_hash(),
        'release_sha256':release,'stage':'draft','judge':'none'}
    dump(folder/'RESERVATION.json', metadata)
    return Task(dataset=MemoryDataset([Sample(id=package,input=as_messages(messages),metadata=metadata)]),
        solver=[generate(),save_answer(folder,package,release)],scorer=[],config=CONFIG,
        metadata={'judge':'none','profile':PROFILE},version='opus-only-all-v1')
