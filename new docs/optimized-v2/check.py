"""Read-only verification or explicit new-release snapshot creation. No APIs."""
import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ORIGINAL = ROOT / 'new docs/frozen/revised-2026-10-24-004057'
sha = lambda data: hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze', action='store_true')
    args = parser.parse_args()
    original = json.loads((ORIGINAL / 'FREEZE_REVISED.json').read_text())
    # Verify original bytes, including principles/rubric, before doing anything.
    subprocess.run([sys.executable, str(ORIGINAL / 'verify_snapshot.py')], cwd=ROOT, check=True)
    manifest_path = HERE / 'VERSION.json'
    if args.freeze:
        if manifest_path.exists():
            raise SystemExit('Release already exists. Do not overwrite; create a new version for changes.')
        names = list(original['files']) + [str((HERE / n).relative_to(ROOT)) for n in
            ('runner.py', 'judge_protocol.py', 'test_optimized.py', 'check.py', 'README.md', 'NEW_AGENT_PROMPT.txt')]
        files = {name: sha((ROOT / name).read_bytes()) for name in sorted(names)}
        archive = HERE / 'snapshot.zip'
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for name in files:
                z.writestr(name, (ROOT / name).read_bytes())
        manifest = {'version': 'optimized-v2', 'profile': 'principles-example-open-medium-v2',
                    'created_at': datetime.now(timezone.utc).isoformat(),
                    'original_grading_sha256': original['grading_sha256'],
                    'model_input_sha256': original['model_input_sha256'],
                    'principles_sha256': files['new docs/principles.md'],
                    'rubric_sha256': files['new docs/rubric.md'],
                    'files': files, 'snapshot_zip_sha256': sha(archive.read_bytes()),
                    'offline_only_preparation': True,
                    'changes': ['medium effort both roles; 64000 output cap retained',
                                'no prompt caching for isolated long calls; serial; max_retries=2',
                                'one judge-report attempt; keyed structured schema',
                                'formatting-only quote alignment with exact-source audit',
                                'save before grading; block paid grading of truncated drafts',
                                'base only; no automatic duplicate generation or grading']}
        manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    if not manifest_path.exists():
        raise SystemExit('No optimized release. Prepare and explicitly freeze it first.')
    manifest = json.loads(manifest_path.read_text())
    errors = [name for name, expected in manifest['files'].items()
              if not (ROOT / name).is_file() or sha((ROOT / name).read_bytes()) != expected]
    archive = HERE / 'snapshot.zip'
    if sha(archive.read_bytes()) != manifest['snapshot_zip_sha256']:
        errors.append('snapshot.zip hash')
    with zipfile.ZipFile(archive) as z:
        if set(z.namelist()) != set(manifest['files']):
            errors.append('snapshot file inventory')
        for name, expected in manifest['files'].items():
            if name not in z.namelist() or sha(z.read(name)) != expected:
                errors.append('snapshot: ' + name)
    if errors:
        raise SystemExit('OPTIMIZED RELEASE MISMATCH\n' + '\n'.join(errors))
    print(f"OPTIMIZED V2 OK: {len(manifest['files'])} source files; original inputs/rubric unchanged; no APIs.")


if __name__ == '__main__':
    main()
