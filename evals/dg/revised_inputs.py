"""Exact inputs for the taught, open-format condition; original paid baseline is untouched."""
import hashlib
import json
import re
from pathlib import Path

from .package import CONDITIONS, ROOT, folder_for, load_package
from .truth import check_truth, truth_for

NEW_DOCS = ROOT / 'new docs'
PROFILE = 'principles-example-open-v1'
LEARNING_FILES = ('task-prompt.md', 'principles.md', 'learning-reference.md')
JUDGE_FILES = ('judge-prompt.md', 'rubric.md', 'scoring-guide.md')


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def input_hash(messages):
    return hashlib.sha256(json_bytes(messages)).hexdigest()


def revised_truth(package_id):
    truth = truth_for(package_id)
    truth.pop('response_due_date', None)
    truth.pop('requests_overridden', None)
    truth['_note'] = 'Judge-only reference for the revised condition, not model instructions or author adjudications.'
    truth['profile'] = PROFILE
    r3 = truth['requests']['3']
    r3['must_produce'] = ['DOC-005', 'DOC-006', 'DOC-007', 'DOC-008']
    r3['optional_produce'] = []
    r3['required_flags'] = [f for f in r3['required_flags'] if f['id'] != 'R3.a']
    r3['_disposition_note'] = ('Request 3 covers all three City A properties under Definition 5 and the singular/plural convention '
                               '(Definition 10; renumbered 9 in T7). R3.a is retired; R3.b and R3.c remain required. '
                               'A stated or flagged House-1-only reading without a supported basis is insufficient.')
    truth['requests']['11']['_disposition_note'] = (
        'Definition 7 expressly defines DURING THE MARRIAGE through separation, January 1, 2026. '
        'Determine responsive returns from filing dates, not tax years; confirm dates and extensions. '
        'This does not equate separation with legal marriage termination. A 2025 return filed after the defined period '
        'is outside Request 11 but responsive under Request 10. Identifying DOC-014 by meaningful cross-reference '
        'is acceptable; do not assume every 2018-2024 return was timely filed.')
    if package_id == 'T6':
        truth['requests']['1']['_disposition_note'] = (
            'The complete Bank A statements DOC-024 are present. Produce them; no pending retrieval of this set. '
            'DOC-002 remains a historical letter and does not override the supplied statements. '
            'DOC-001 need not be duplicated when DOC-024 is identified.')
    rubric = (NEW_DOCS / 'rubric.md').read_text()
    for num, request in truth['requests'].items():
        request['omission_checks'] = [
            {'id': m.group(1), 'text': m.group(2).strip()}
            for m in re.finditer(r'^\| (R' + re.escape(num) + r'\.O\d+) \| ([^\n]+?) \|', rubric, re.M)
        ]
        if not request['omission_checks']:
            raise ValueError(f'Revised rubric has no omission checks for Request {num}')
    for constraint in truth.get('pair_constraints', []):
        constraint['text'] = constraint['text'].replace('text outside the tags', 'other content proposed for opposing counsel')
    truth['assessment_scope'] = {
        'deadline_calculation': 'excluded',
        'presentation': 'open format; substantive production may be identified in prose or cross-references',
        'audience': 'semantic distinction; untagged prose is not automatically external',
        'reference_conflicts': 'report for review, not an automatic error by the drafter',
        'quality': 'designated requests only',
        'safety': 'designated requests plus package; other request findings reported separately',
    }
    return truth


def load_inputs(package_id):
    package = load_package(package_id)
    material = {f: (NEW_DOCS / f).read_text() for f in LEARNING_FILES}
    if any(not text.strip() for text in material.values()):
        raise ValueError('Empty teaching material or task prompt')
    user = ('REFERENCE PRINCIPLES\n\n' + material['principles.md'].strip() +
            '\n\nEDUCATIONAL RPD RESPONSE EXAMPLE — NOT CASE EVIDENCE\n\n' + material['learning-reference.md'].strip() +
            '\n\nCASE INFORMATION\n\n' + package.case_context.strip() +
            '\n\nASSIGNED REQUEST FOR PRODUCTION\n\n' + package.rfp.strip() +
            '\n\nCASE EVIDENCE\n\n' + package.as_prompt_text())
    messages = [{'role': 'system', 'content': material['task-prompt.md'].strip()}, {'role': 'user', 'content': user}]
    truth = revised_truth(package_id)
    numbers = re.findall(r'REQUEST FOR PRODUCTION NO\.\s*(\d+)', package.rfp, re.I)
    if not numbers:
        numbers = re.findall(r'Request No\.\s*(\d+)', package.rfp, re.I)
    check_truth(truth, package, numbers)
    return package, messages, truth


def reference_answers():
    text = (NEW_DOCS / 'rubric.md').read_text()
    general = text.split('## General reference rules', 1)[1].split('# Request-by-request reference and omission checks', 1)[0]
    blocks = []
    for block in re.split(r'(?=^### Request No\. \d+:)', text.split('# Request-by-request reference and omission checks', 1)[1], flags=re.M):
        if block.startswith('### Request No.'):
            blocks.append(block.split('#### Omission checklist', 1)[0].strip())
    return ('# Reference Answers\n\nJudge-only. Derived from the revised rubric; these are reference dispositions, '
            'not an actual Opus answer or an infallible standard. Apply the condition-specific key and rubric.\n\n' +
            general.strip() + '\n\n' + '\n\n'.join(blocks) + '\n\n' +
            '# Twin-specific reference changes' + text.split('# Twin-specific reference changes', 1)[1])


def prepared_artifacts(package_id):
    """All expected generated bytes for a set, including shared role references."""
    package, messages, truth = load_inputs(package_id)
    files = {}
    for f in LEARNING_FILES:
        files['opus5.5/' + f] = (NEW_DOCS / f).read_bytes()
        files['judge/learning-materials/' + f] = (NEW_DOCS / f).read_bytes()
    for f in JUDGE_FILES:
        files['judge/' + f] = (NEW_DOCS / f).read_bytes()
    files['judge/reference-answers.md'] = reference_answers().encode()
    from .revised_judge import OUTPUT_CONTRACT
    files['judge/report-format.txt'] = OUTPUT_CONTRACT.encode()
    source = folder_for(package_id)
    manifest = json.loads((source / 'reviewer_only/document_manifest.json').read_text())
    for role in ('opus5.5', 'judge'):
        prefix = f'{role}/sets/{package_id}/'
        files[prefix + 'facts.txt'] = package.case_context.encode()
        files[prefix + 'request-for-production.txt'] = package.rfp.encode()
        files[prefix + 'evidence-text.txt'] = (package.as_prompt_text() + '\n').encode()
        name = 'model-messages.json' if role == 'opus5.5' else 'drafter-messages.json'
        files[prefix + name] = json_bytes(messages)
        for entry in manifest:
            files[prefix + 'evidence/' + entry['filename']] = (source / 'discovery_files' / entry['filename']).read_bytes()
    prefix = f'judge/sets/{package_id}/'
    files[prefix + 'scoring-key.json'] = json_bytes(truth)
    files[prefix + 'assessment-scope.md'] = (
        f'# Assessment scope\n\nCondition: {package_id}\nQuality-scored requests: {", ".join(truth["scored_requests"])}\n'
        f'Maximum request-quality points: {6 * len(truth["scored_requests"])}\n\n'
        'Use scoring-key.json with rubric.md. Apply package-wide safety in every condition. '
        'Other request findings remain visible separately. Deadline calculation is excluded. '
        'Request 3 covers all three properties; Request 11 uses Definition 7, with filing dates confirmed.\n\n'
        'drafter-messages.json is the exact prepared input, not proof of an API call. '
        'Do not substitute historical baseline answers or the reference answer for a new Opus response. '
        'The revised runner sends the actual answer to the judge directly and logs the outgoing judge messages. '
        'For manual review, place the complete new response in opus-response.txt.\n'
    ).encode()
    return package, messages, truth, files


def grading_hash():
    paths = [NEW_DOCS / f for f in JUDGE_FILES + LEARNING_FILES]
    paths += list((ROOT / 'evals/ground_truth').glob('*.json'))
    paths += list((ROOT / 'evals/dg').glob('revised_*.py'))
    paths += [ROOT / 'evals/dg/package.py', ROOT / 'evals/dg/truth.py',
              ROOT / 'evals/disclosure_guard_revised.py', ROOT / 'evals/report_revised.py']
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    return hashlib.sha256(json_bytes(hashes)).hexdigest()


def verify_prepared(package_id):
    """Fail before a run if the human-review folder and runtime inputs disagree."""
    _, _, _, files = prepared_artifacts(package_id)
    for rel, content in files.items():
        path = NEW_DOCS / rel
        if not path.is_file() or path.read_bytes() != content:
            raise ValueError(f'Prepared material is missing or stale: new docs/{rel}. Rebuild and review before running.')
    for role in ('opus5.5', 'judge'):
        prefix = f'{role}/sets/{package_id}/evidence/'
        expected = {rel[len(prefix):] for rel in files if rel.startswith(prefix)}
        actual = {p.name for p in (NEW_DOCS / prefix).glob('*.pdf')}
        if actual != expected:
            raise ValueError(f'Unexpected evidence files in {role}/{package_id}: {sorted(actual ^ expected)}')
