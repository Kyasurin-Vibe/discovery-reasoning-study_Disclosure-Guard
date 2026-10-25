# Verifying this repository

Everything below runs offline. It makes no model, API or network calls.

## 1. Check the published files

From the repository root:

```bash
python3 verify_release.py
# Also decode PDF metadata and content (requires the pypdf version in requirements.txt):
python3 verify_release.py --deep
```

`verify_release.py` compares every file in this repository, including the website in `docs/`, with `MANIFEST.sha256`. It reports missing, extra or changed files, scans text, JSON, PDFs and compressed logs for local paths and credential-shaped values, and checks local links. The top-level `.git` directory of a clone is Git's own metadata and is not checked; every other file must appear in the manifest.

## 2. Three kinds of hashes

| Where | What the hash identifies |
|---|---|
| `MANIFEST.sha256` | The files in this repository as published, including `docs/`. Use it to check that your copy is complete and unchanged. The manifest does not list itself. |
| `RELEASE_PROVENANCE.json` | The mapping from each original experiment file to its released copy. Where a file was redacted or reformatted for publication, the original and released hashes differ, and `REDACTIONS.json` records why. |
| Hashes inside experiment records and `provenance/` | Historical values from the original, private experiment record. They identify the original files, not the sanitized copies here, so they are not expected to match these files. |

A matching hash shows that a file is identical to the published version. It does not show that the content is legally or scientifically correct.

## 3. The website

The interactive research website is the static site in `docs/`, served by GitHub Pages from the `main` branch's `/docs` folder. It uses only relative links. To view it locally, open `docs/index.html` in a browser. The research documents under `docs/research/` are copies of files at the repository root, kept so the website can link to them; the root files are the reference copies.

## 4. Tests and rebuilt inputs

The offline tests run without model access:

```bash
python3 -m pytest tests "new docs/optimized-v2/test_optimized.py"
```

The drafter inputs can be rebuilt from the published materials, and they match the recorded input hashes. For the judge, one rubric heading was shortened for concision in this publication, so a rebuilt judge request will not match the recorded request hash. No other judge input, model output or score was changed.

Some scripts are kept as historical records of the original runs. `new docs/optimized-v2/check.py` and `new docs/frozen/revised-2026-10-24-004057/verify_snapshot.py` need a preparation archive that is not published, so they stop with a missing-file error here; the README in each folder explains this. The review runners also refuse to overwrite an existing recorded review, so their `--check` mode reports that output already exists.

## 5. Reproducing the experiment

Re-running the models requires your own model-provider access and incurs usage charges. See `README.md`, `METHODOLOGY.md` and `EXPERIMENT_RECORDS.md` for what each run received, and `LICENSE` for the permission covering assessment and reproduction.
