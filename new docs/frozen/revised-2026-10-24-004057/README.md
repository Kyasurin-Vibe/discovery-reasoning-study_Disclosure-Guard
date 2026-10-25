# Historical freeze record

`FREEZE_REVISED.json` and `verify_snapshot.py` are kept as part of the experiment record. They document the input snapshot used to prepare the runs.

`verify_snapshot.py` checks a preparation archive (`snapshot.zip`) that is not included in this repository, because its contents are already published here as individual files. Run in this repository, it stops with a missing-file error. That is expected and does not indicate damaged files.

To check this repository, use `verify_release.py` and the test suite instead. See [VERIFY.md](../../../VERIFY.md).
