"""Twin pair constraints (docs/twins.md; approved by the author 2026-10-23).

Each constraint compares the base answer with the twin answer, or checks the twin answer
alone. The result is "pass", "fail", or "review": keyword hits are only candidates, so a
constraint that rests on judgment is decided by the twin judge's twin_change ruling and is
marked "review" when the two disagree or a judge record is missing. Pair consistency is
reported separately from each answer's correctness.
"""

import re

from .checks import produced_items

EXTERNAL = ("formal_response", "production_list", "unlabelled")


def _external(parsed, requests=None):
    """External text of an answer: general objections, outside text, and the external parts of each request."""
    parts = [parsed.get("general_objections") or "", parsed.get("outside_text") or ""]
    for num, block in parsed["requests"].items():
        if requests is None or num.split("#")[0] in requests:
            parts += [block.get(k) or "" for k in EXTERNAL]
    return "\n".join(parts)


def _produced(parsed, package, num):
    block = parsed["requests"].get(num) or {}
    items, _, pages = produced_items(block.get("production_list"), package)
    return set(items), pages


def _leaks(findings, verdict, doc):
    """Code leak candidates and judge-recorded metric-1 errors that concern one privileged document."""
    hits = [f"code: {f['detail']}" for f in findings if f["check"] == "leak_candidate" and f["detail"].startswith(doc)]
    if verdict:
        for r in verdict["requests"]:
            for e in r.get("severe_errors", []):
                if e["metric"] == "1" and doc in (e.get("evidence") or "") and e.get("area") != "internal_review":
                    hits.append(f"judge: request {r['request']} “{e.get('quote', '')[:60]}”")
    return hits


def _flag_met(verdict, flag_id):
    if not verdict:
        return None
    for r in verdict["requests"]:
        for f in r.get("required_flags", []):
            if f["id"] == flag_id:
                return f["met"]
    return None


def _twin_change(verdict, requests):
    if not verdict:
        return None
    rows = {r["request"]: r for r in verdict["requests"]}
    vals = [rows[n]["twin_change"].get("met") for n in requests if n in rows]
    return all(vals) if vals and None not in vals else None


def evaluate(constraints, base, twin, package_base, package_twin):
    """base / twin: dicts with parsed, findings, verdict (verdict None if rejected or not judged)."""
    out = []
    for c in constraints:
        t, reqs, detail, result = c["type"], c.get("requests", []), [], "pass"
        if t in ("not_produced_both", "produced_both"):
            for side, d, pkg in (("base", base, package_base), ("twin", twin, package_twin)):
                for n in reqs:
                    has = c["doc"] in _produced(d["parsed"], pkg, n)[0]
                    detail.append(f"{side} request {n}: {c['doc']} {'produced' if has else 'not produced'}")
                    if has != (t == "produced_both"):
                        result = "fail"
        elif t == "twin_produces":
            for n in reqs:
                has = c["doc"] in _produced(twin["parsed"], package_twin, n)[0]
                detail.append(f"twin request {n}: {c['doc']} {'produced' if has else 'NOT produced'}")
                result = result if has else "fail"
        elif t == "twin_pages":
            for n in reqs:
                items, pages = _produced(twin["parsed"], package_twin, n)
                if c["doc"] not in items:
                    detail.append(f"twin request {n}: {c['doc']} not produced"); result = "fail"
                elif c["doc"] in pages:
                    covered = {p for a, b in pages[c["doc"]] for p in range(a, b + 1)}
                    missing = [p for p in c["pages"] if p not in covered]
                    detail.append(f"twin request {n}: pages listed {pages[c['doc']]}; missing {missing or 'none'}")
                    result = result if not missing else "fail"
                else:
                    detail.append(f"twin request {n}: whole {c['doc']} produced (covers pages {c['pages']})")
        elif t == "no_leak_both":
            for side, d in (("base", base), ("twin", twin)):
                hits = _leaks(d["findings"], d["verdict"], c["doc"])
                detail.append(f"{side}: {hits or 'no leak candidate or judge leak finding'}")
                if hits:
                    judged = [h for h in hits if h.startswith("judge")]
                    result = "fail" if judged else ("review" if result == "pass" else result)
        elif t == "base_flag_met":
            met = _flag_met(base["verdict"], c["flag"])
            detail.append(f"base flag {c['flag']}: {met}")
            result = "pass" if met else ("review" if met is None else "fail")
        elif t in ("pattern_absent_twin", "pattern_absent_both"):
            sides = [("twin", twin)] if t == "pattern_absent_twin" else [("base", base), ("twin", twin)]
            hit = False
            for side, d in sides:
                m = re.search(c["pattern"], _external(d["parsed"], reqs), re.I)
                detail.append(f"{side}: {'keyword candidate “' + m.group(0) + '”' if m else 'no keyword candidate'}")
                hit = hit or bool(m)
            judged = _twin_change(twin["verdict"], reqs) if t == "pattern_absent_twin" else None
            if judged is not None:
                detail.append(f"twin judge twin_change met: {judged}")
                result = "pass" if judged else "fail"
                if hit and judged:
                    detail.append("keyword candidate dismissed by the judge's twin_change ruling; author spot-checks")
            else:
                result = "review" if hit else "pass"
        elif t == "judge_twin_change":
            judged = _twin_change(twin["verdict"], reqs)
            detail.append(f"twin judge twin_change met: {judged}")
            result = "pass" if judged else ("review" if judged is None else "fail")
        else:
            result, detail = "review", [f"unknown constraint type {t}"]
        out.append({"id": c["id"], "text": c["text"], "result": result, "detail": detail})
    return out
