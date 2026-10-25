"""Rebuild/check reviewed role bundles. Offline only; never modifies historical FREEZE.json."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'evals'))
from dg.package import CONDITIONS
from dg.revised_inputs import NEW_DOCS, PROFILE, grading_hash, input_hash, json_bytes, prepared_artifacts, verify_prepared

OPUS_README = '''# Opus 5.5 materials

The separate revised runner is `evals/disclosure_guard_revised.py`. It sends the exact prepared task, principles, Sacramento example, facts, RFP, and all evidence text. No revised live run has been made by this preparation step. Historical baseline answers are not new results.

Use one set in a fresh context. `sets/base` is the base case; `sets/T1`–`sets/T7` are seven variants of that same case. Common learning materials are task-prompt.md, principles.md, and learning-reference.md. The Sacramento County Public Law Library example is the selected text from pages 45–46; the complete 50-page source PDF is not silently included.

Each model-messages.json is the exact outgoing system/user input. It already contains every learning and case item once. The PDF copies are for inspection; they are not attached a second time in this text-input condition. Facts come from the model-facing case-information page, not the author's private case file.

No custom response template is imposed. The assignment asks for clearly distinguished counsel-only notes for fact-checking, client confirmation, and human decisions. Do not supply the judge folder, rubric, keys, author notes, or other sets to the drafter.
'''
JUDGE_README = '''# Fable 5.1 judge materials

The separate revised runner uses judge-prompt.md, rubric.md, scoring-guide.md, the set's scoring-key.json, the exact prepared drafter messages, and the actual complete drafter answer. Reference-answers.md is a convenient narrative extracted from the rubric, not an Opus output; the runtime includes the full rubric once rather than duplicating it.

There are no new live Opus responses from this preparation step. Historical responses are not substituted as new results. A replay is only an offline software check and is labeled as such in the report.

Each set contains facts, its RFP, evidence PDFs/text, drafter-messages.json, scoring-key.json, and assessment-scope.md. The drafter transcript already contains all teaching and case text. Judge instructions remain short; a separate judge-side JSON reporting contract supports validation and does not impose a format on the drafter.

Scores and natural evidence-based comments are checked for complete coverage, quotes, record/page references, and required confirmations. Production is identified semantically with supporting quotations, not inferred from every DOC mention. Material reference conflicts require review; malformed records are rejected without a score. Deadline calculations and required LSAT/LegalBench labels are excluded. Prior judge results and author adjudications are not supplied.

The runner logs exact judge messages and both attempts if a real judge record requires one retry. Live calls require explicit allow_api=true; this preparation/check script cannot call a model. For manual review only, add an actual complete revised response as opus-response.txt in the matching set. Never grade a placeholder or reference answer as the model's answer.
'''


def collect():
    files = {'opus5.5/README.md': OPUS_README.encode(), 'judge/README.md': JUDGE_README.encode()}
    sets = []
    for pid in CONDITIONS:
        package, messages, truth, artifacts = prepared_artifacts(pid)
        files.update(artifacts)
        sets.append({'set_id': pid, 'source_condition': pid, 'documents': len(package.documents),
                     'pages': package.total_pages(), 'scored_requests': list(map(int, truth['scored_requests'])),
                     'prepared_messages_sha256': input_hash(messages), 'opus_response': None})
    return files, sets


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args=parser.parse_args()
    files, sets = collect()
    hashes={rel:hashlib.sha256(value).hexdigest() for rel,value in sorted(files.items())}
    if args.check:
        for pid in CONDITIONS:
            verify_prepared(pid)
        manifest=json.loads((NEW_DOCS/'PACKAGING_MANIFEST.json').read_text())
        if manifest['files'] != hashes or manifest['sets'] != sets or manifest['grading_sha256'] != grading_hash():
            raise SystemExit('Prepared manifest differs from current inputs/grading code; rebuild and review.')
        for rel,content in files.items():
            if (NEW_DOCS/rel).read_bytes() != content:
                raise SystemExit(f'Prepared file differs: {rel}')
        print(f'REVISED INPUTS OK: 8 sets, {len(files)} generated files; no APIs.')
        return
    for rel,content in files.items():
        target=NEW_DOCS/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists() or target.read_bytes()!=content:
            target.write_bytes(content)
    manifest={'status':'offline-prepared-runtime-connected-not-live-run','profile':PROFILE,
              'drafter_role':'Opus 5.5','judge_role':'Fable 5.1','paid_api_calls_this_revision':0,
              'historical_runner_changed':False,'revised_runner':'evals/disclosure_guard_revised.py',
              'response_representation':'extracted text with record IDs and page boundaries',
              'facts_source':'data/case/case_context.txt','learning_source':'new docs/learning-reference.md (Sacramento pp. 45–46)',
              'grading_sha256':grading_hash(),'sets':sets,'files':hashes,
              'freeze_status':'prepared review snapshot; historical FREEZE.json not changed'}
    (NEW_DOCS/'PACKAGING_MANIFEST.json').write_bytes(json_bytes(manifest))
    path=NEW_DOCS/'REVIEW_MANIFEST.json'
    review=json.loads(path.read_text())
    review.update(status='offline-prepared-runtime-connected-not-live-run',runtime_connected=True,profile=PROFILE,
                  revision='R3 all City A properties; R11 defined period; taught open-format adapter; offline checks only',
                  base_required_flag_count=sum(len(r['required_flags']) for r in prepared_artifacts('base')[2]['requests'].values()))
    review['assessment_scope']['actual_rfp_definitions_applied']=True
    review['role_bundles']['manifest_sha256']=hashlib.sha256((NEW_DOCS/'PACKAGING_MANIFEST.json').read_bytes()).hexdigest()
    review['role_bundles']['status']=manifest['status']
    for name in review['draft_sha256']:
        review['draft_sha256'][name]=hashlib.sha256((NEW_DOCS/name).read_bytes()).hexdigest()
    review['learning_reference']['sha256']=hashlib.sha256((NEW_DOCS/'learning-reference.md').read_bytes()).hexdigest()
    review['grading_sha256']=grading_hash()
    # source_sha256 is the preserved historical review snapshot, not silently rebased.
    path.write_bytes(json_bytes(review))
    print(f'Prepared 8 sets and {len(files)} generated files; historical inputs/results/freeze unchanged; no APIs.')

if __name__=='__main__':
    main()
