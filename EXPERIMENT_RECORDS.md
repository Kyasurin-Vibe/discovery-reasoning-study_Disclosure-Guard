# Experiment records in the sanitized copy

The private successful medium-effort record was locked separately and remains unchanged. This release uses one canonical project-relative tree, avoiding a duplicate private snapshot directory.

- Base draft: new docs/optimized-v2/runs/base-v2/
- Base full-materials Fable review: new docs/judge/free-review/runs/base-v2-free/
- T1–T7 drafts: new docs/opus-all-v1/runs/T1 through T7/
- T1–T7 Fable reviews: new docs/judge/free-review-all-v1/runs/T1 through T7/
- Actual inputs, evidence PDFs/text, teaching materials and case keys: new docs/opus5.5/sets/ and new docs/judge/sets/, with recorded shared materials.
- Successful logs: original relative log folders, in sanitized .eval archives.
- Final author work: new docs/judge/author-review/base-final-review.* and new docs/report/09_base-report.*

Original hashes in model records, original manifests and freeze/version files are provenance values, not claims about sanitized bytes. RELEASE_PROVENANCE.json records the source-to-release hash mapping. The current MANIFEST.sha256 and verify_release.py cover this sanitized copy, including its own documentation and metadata, but the manifest does not hash itself.

Excluded: .git and its history; .env and credentials; virtual environments and caches; operating-system metadata; earlier failed/truncated/incomplete-material runs; unrelated drafts; redundant preparation ZIPs after necessary members were expanded and scanned. The 16 successful .eval archives remain included and are recursively checked.

Read-only private records were not edited. Non-readable provider-redacted payloads are omitted from the public copy where present; visible prompts, evidence, answers, reviews and scores are preserved. Privacy redactions and documentation/link packaging changes are listed separately in REDACTIONS.json. All eight visible answer/review pairs are compared with their private originals during preparation.

Author review status is Base complete; T1–T7 pending. Public release, independent attorney validation, external link availability and full runtime reproduction remain outside this preparation step.

## Final publication cleanup

Superseded Base/T1–T7 comparison aids, the earlier workbook, duplicate summary and redundant disclaimer draft are not included in this public tree. The complete source answers, assessments, actual inputs, evidence, case keys, code and final Base adjudication remain. Chronological author notes are audit records, not current score summaries. Recorded input-stage copies are retained where needed for provenance and code dependencies; they are not obsolete drafts.

The author's working adjudication notes are personal records and are not published; the final Base review and Base Report contain the published adjudications.
