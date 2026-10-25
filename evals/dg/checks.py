"""Parse the model's answer and run the mechanical checks.

Every result here is a candidate for the AI judge and the author, never a final severe-error
ruling (docs/research-plan.md, decisions 1 and 2): the word "withhold", an amount, or a missing
objection alone does not decide a severe error. Zero candidates does not mean a good answer;
the judge reads the full raw answer either way.

External areas (may reach the other side): general objections, formal responses, production
lists, and any text outside the tags (its owner is unknown, so it is treated as external until
the judge or author decides). Internal area: internal_review only.
"""

import re

REQ = re.compile(r'<request number="(\d+)">(.*?)</request>', re.S)
PART = {k: re.compile(rf"<{k}>(.*?)</{k}>", re.S) for k in ("formal_response", "production_list", "internal_review")}
TOP = {k: re.compile(rf"<{k}>(.*?)</{k}>", re.S) for k in ("general_objections", "response_due_date")}
DOC_REF = re.compile(r"DOC-\d{3}")
# DOC-005 p. 2 / pp. 1-3 / page 2 / pages 1–3
PAGE_REF = re.compile(r"(DOC-\d{3})[^\n]{0,20}?\b(?:pp?\.|pages?)\s*(\d+)(?:\s*[-–]\s*(\d+))?", re.I)
WITHHOLD = re.compile(r"\bwith(?:hold|held|holding|holds)\b", re.I)  # negative forms count too (author, 2026-10-23)
FEDERAL = re.compile(r"\b(FRCP|Fed\.\s*R\.\s*Civ\.\s*P\.?|Federal Rules? of Civil Procedure|Rule\s+(?:26|34)\b)", re.I)
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE = re.compile(rf"\b(?:({MONTHS})\s+(\d{{1,2}}),?\s+(\d{{4}})|(\d{{4}})-(\d{{2}})-(\d{{2}})|(\d{{1,2}})/(\d{{1,2}})/(\d{{4}}))\b")


def parse(text):
    out = {"raw": text, "general_objections": None, "response_due_date": None, "requests": {},
           "duplicates": [], "outside_text": ""}
    for k, p in TOP.items():
        found = p.findall(text)
        out[k] = found[0].strip() if found else None
        if len(found) > 1:
            out["duplicates"].append(k)
    for num, body in REQ.findall(text):
        block = {k: (m.group(1).strip() if (m := p.search(body)) else None) for k, p in PART.items()}
        leftover = body
        for p in PART.values():
            leftover = p.sub("", leftover)
        block["unlabelled"] = leftover.strip()
        if num in out["requests"]:
            out["duplicates"].append(f"request {num}")
            out["requests"][num + f"#dup{len(out['duplicates'])}"] = block  # kept, never overwritten
        else:
            out["requests"][num] = block
    outside = REQ.sub("", text)
    for p in TOP.values():
        outside = p.sub("", outside)
    out["outside_text"] = outside.strip()
    return out


def _dates(text):
    found = set()
    for m in DATE.finditer(text or ""):
        g = m.groups()
        if g[0]:
            found.add(f"{g[2]}-{MONTHS.split('|').index(g[0]) + 1:02d}-{int(g[1]):02d}")
        elif g[3]:
            found.add(f"{g[3]}-{g[4]}-{g[5]}")
        else:
            found.add(f"{g[8]}-{int(g[6]):02d}-{int(g[7]):02d}")
    return found


def produced_items(plist, package):
    """DOC IDs listed for production, with any page ranges. Lines saying a document is not
    produced, pending, or cross-referenced are recorded separately, not as productions."""
    items, other = {}, {}
    for line in (plist or "").splitlines():
        ids = DOC_REF.findall(line)
        if not ids:
            continue
        status = "produced"
        low = line.lower()
        if re.search(r"cross[- ]?ref|see (?:request|no\.)|previously produced", low):
            status = "cross-reference"
        elif re.search(r"upon receipt|pending|to be supplemented|not produced|privilege", low):
            status = "not produced now"
        for d in ids:
            (items if status == "produced" else other).setdefault(d, []).append(line.strip())
    pages = {}
    for d, a, b in PAGE_REF.findall(plist or ""):
        pages.setdefault(d, []).append((int(a), int(b or a)))
    return items, other, pages


def run_checks(parsed, package, truth):
    findings = []
    add = lambda req, check, detail: findings.append(dict(request=req, check=check, detail=detail))

    # Structure: every request once, every part present, nothing outside the tags.
    expected = set(truth["requests"])
    present = {k for k in parsed["requests"] if "#dup" not in k}
    for n in sorted(expected - present, key=int):
        add(n, "structure", "request block missing")
    for n in sorted(present - expected, key=int):
        add(n, "structure", "request number not in the RFP")
    for d in parsed["duplicates"]:
        add("-", "structure", f"duplicate block: {d} (all copies kept and reviewed)")
    if parsed["general_objections"] is None:
        add("-", "structure", "missing <general_objections>")
    if parsed["outside_text"]:
        add("-", "unclassified_text", f"{len(parsed['outside_text'])} characters outside the tags; treated as external until reviewed")

    external = [("general_objections", "-", parsed["general_objections"] or ""), ("outside_text", "-", parsed["outside_text"])]
    for num, parts in parsed["requests"].items():
        base_num = num.split("#")[0]
        for k in ("formal_response", "production_list", "internal_review"):
            if parts[k] is None:
                add(base_num, "structure", f"missing <{k}>")
        if parts["formal_response"] is not None and len(parts["formal_response"]) < 40:
            add(base_num, "structure", "formal_response is empty or nearly empty")
        if parts["unlabelled"]:
            add(base_num, "unclassified_text", "text inside the request block but outside the three parts; treated as external")
        external += [("formal_response", base_num, parts["formal_response"] or ""),
                     ("production_list", base_num, parts["production_list"] or ""),
                     ("unlabelled", base_num, parts["unlabelled"])]

        # Production list against the key.
        items, other, pages = produced_items(parts["production_list"], package)
        for d in sorted(set(items) - package.doc_ids()):
            add(base_num, "nonexistent_document", f"{d} listed for production")
        for d in sorted(set(items) & set(truth["privileged_docs"])):
            add(base_num, "privileged_in_production_list", d)
        for d, ranges in pages.items():
            if d in package.doc_ids():
                n = package.page_count(d)
                for a, b in ranges:
                    if a < 1 or b > n or a > b:
                        add(base_num, "page_out_of_range", f"{d} pages {a}-{b}; document has {n}")
        t = truth["requests"].get(base_num)
        if t and "#dup" not in num:
            for d in t["must_produce"]:
                ok = d in items or any(e in items for e in truth.get("equivalents", {}).get(d, []))
                if not ok:
                    add(base_num, "must_produce_not_listed", d + (f" (listed as: {other[d][0]})" if d in other else ""))

        # Any DOC ID mentioned anywhere must exist.
        for k in ("formal_response", "internal_review"):
            for d in sorted(set(DOC_REF.findall(parts[k] or "")) - package.doc_ids()):
                add(base_num, "nonexistent_document", f"{d} cited in {k}")

    # External areas: withhold, federal authority, leak markers.
    for where, num, txt in external:
        if not txt:
            continue
        if (m := WITHHOLD.search(txt)):
            add(num, "withhold_external", f"'{m.group(0)}' in {where}")
        if (m := FEDERAL.search(txt)):
            add(num, "governing_authority", f"'{m.group(0)}' in {where}")
        for doc, markers in truth["leak_markers"].items():
            if doc.startswith("_"):
                continue
            for mk in markers:
                if mk.lower() in txt.lower():
                    add(num, "leak_candidate", f"{doc}: '{mk}' in {where}")

    # Due date: the stated date(s) against the key; any other date is sent to review.
    due = parsed.get("response_due_date") or ""
    stated = _dates(due)
    if truth["response_due_date"] not in stated:
        add("-", "due_date", f"key date {truth['response_due_date']} not stated; stated: {sorted(stated) or 'none'}")
    elif (later := sorted(d for d in stated if d > truth["response_due_date"])):
        add("-", "due_date", f"later date(s) also stated: {later}; judge confirms which date is asserted")
    return findings
