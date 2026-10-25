"""Load a document package (BASE or a twin) as the text the model under test sees.

Every condition is read the same way from its frozen snapshot in data/twins/<COND>/:
discovery_files/*.pdf (evidence), reviewer_only/document_manifest.json (IDs and titles only),
and rfp-set-one.md (the condition's own RFP). Nothing else in the folder enters the prompt:
CHANGES.md and the rest of reviewer_only/ describe the manipulation and stay author-only.
A missing file is an error; no condition silently falls back to another condition's files.
"""

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
TWINS = ROOT / "data" / "twins"
CASE_CONTEXT = ROOT / "data" / "case" / "case_context.txt"
CONDITIONS = ["base", "T1", "T2", "T3", "T4", "T5", "T6", "T7"]
TITLE_SUFFIX = " | Fictional Evaluation Record"  # PDF metadata suffix; dropped for every condition alike


@dataclass
class Package:
    package_id: str
    rfp: str
    case_context: str
    documents: dict  # DOC ID -> {"title", "pages": [text, ...], "sha256"}

    def doc_ids(self):
        return set(self.documents)

    def page_count(self, doc_id):
        return len(self.documents[doc_id]["pages"])

    def total_pages(self):
        return sum(len(d["pages"]) for d in self.documents.values())

    def as_prompt_text(self):
        parts = []
        for doc_id in sorted(self.documents):
            d = self.documents[doc_id]
            for i, page in enumerate(d["pages"], start=1):
                parts.append(f"===== {doc_id} | {d['title']} | page {i} of {len(d['pages'])} =====\n{page.strip()}")
        return "\n\n".join(parts)


def folder_for(package_id):
    if package_id not in CONDITIONS:
        raise ValueError(f"unknown package '{package_id}'; expected one of {CONDITIONS}")
    return TWINS / ("BASE" if package_id == "base" else package_id)


def _require(path):
    if not path.exists():
        raise FileNotFoundError(f"package file missing: {path.relative_to(ROOT)}")
    return path


def clean_rfp(text):
    """Same formatting for every condition: drop Markdown headings and bold markers."""
    text = re.sub(r"^#+\s*", "", text, flags=re.M).replace("**", "")
    return text.strip() + "\n"


def load_package(package_id="base"):
    folder = folder_for(package_id)
    manifest = json.loads(_require(folder / "reviewer_only" / "document_manifest.json").read_text())
    rfp = clean_rfp(_require(folder / "rfp-set-one.md").read_text())
    documents = {}
    for entry in manifest:
        pdf = _require(folder / "discovery_files" / entry["filename"])
        data = pdf.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        if sha != entry["sha256"]:
            raise ValueError(f"{pdf.relative_to(ROOT)} does not match its manifest hash")
        title = entry["title"].removesuffix(TITLE_SUFFIX)
        documents[entry["document_id"]] = {"title": title, "sha256": sha,
                                           "pages": [p.extract_text() or "" for p in PdfReader(str(pdf)).pages]}
    on_disk = {p.name for p in (folder / "discovery_files").glob("*.pdf")}
    extra = on_disk - {e["filename"] for e in manifest}
    if extra:
        raise ValueError(f"{package_id}: PDFs not in the manifest: {sorted(extra)}")
    return Package(package_id, rfp, _require(CASE_CONTEXT).read_text().strip() + "\n", documents)
