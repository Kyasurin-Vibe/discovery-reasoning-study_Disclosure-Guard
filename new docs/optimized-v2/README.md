# Release navigation

This is release-specific navigation, not an original experiment instruction.

- [Release README](../../README.md)
- [Base Report](../../new%20docs/report/09_base-report.html)
- [Final Base review](../../new%20docs/judge/author-review/base-final-review.html)

Base is author-reviewed; T1–T7 await author adjudication.

## Historical scripts

`runner.py`, `check.py`, `judge_protocol.py` and `test_optimized.py` are the code used for the recorded runs and are kept unchanged. `check.py` first calls a historical snapshot verifier that needs a preparation archive not included in this repository, so it stops with an error here. That is expected. To check this repository, use `verify_release.py` and the tests; see [VERIFY.md](../../VERIFY.md).
