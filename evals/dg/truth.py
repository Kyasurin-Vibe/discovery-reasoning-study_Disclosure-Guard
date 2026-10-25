"""Author-only answer key for one condition: base.json plus the twin's overrides.

Overrides merge field by field inside each request, so a twin that changes Request 5 never
erases the rules for Requests 1-4 and 6-13. Top-level maps (leak_markers, equivalents) merge
per key. check_truth() fails loudly when the key and the package disagree.
"""

import copy
import json
from pathlib import Path

GROUND_TRUTH = Path(__file__).resolve().parents[1] / "ground_truth"
REQUEST_FIELDS = {"must_produce", "optional_produce", "required_flags", "forbidden", "_disposition_note"}


def truth_for(package_id):
    truth = json.loads((GROUND_TRUTH / "base.json").read_text())
    truth["condition"] = package_id
    if package_id == "base":
        return truth
    twin = json.loads((GROUND_TRUTH / f"{package_id}.json").read_text())
    truth["requests_overridden"] = twin.get("requests", {})
    for num, fields in twin.get("requests", {}).items():
        unknown = set(fields) - REQUEST_FIELDS
        if unknown:
            raise ValueError(f"{package_id} request {num}: unknown fields {sorted(unknown)}")
        truth["requests"][num].update(copy.deepcopy(fields))
    for key in ("leak_markers", "equivalents"):
        truth[key] = {**truth.get(key, {}), **twin.get(key, {})}
    for key in ("scored_requests", "expected_change", "pair_constraints"):
        if key in twin:
            truth[key] = twin[key]
    return truth


def check_truth(truth, package, rfp_request_numbers):
    """Integrity preflight: every rule points at a real request and a real document."""
    problems = []
    if set(truth["requests"]) != set(rfp_request_numbers):
        problems.append(f"key requests {sorted(truth['requests'], key=int)} != RFP requests {sorted(rfp_request_numbers, key=int)}")
    for num in truth["scored_requests"]:
        if num not in truth["requests"]:
            problems.append(f"scored request {num} not in key")
    ids = package.doc_ids()
    for num, r in truth["requests"].items():
        for d in r["must_produce"] + r["optional_produce"]:
            if d not in ids:
                problems.append(f"request {num}: {d} not in package")
    for d in truth["privileged_docs"]:
        if d not in ids:
            problems.append(f"privileged {d} not in package")
    if problems:
        raise ValueError(f"{truth['condition']}: answer key does not match package: {problems}")
