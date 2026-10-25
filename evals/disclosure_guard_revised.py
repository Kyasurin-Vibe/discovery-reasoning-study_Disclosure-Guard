"""Separate runner for the principles/example condition; preserves the original experiment.

Offline replay (no model calls):
  inspect eval evals/disclosure_guard_revised.py --model mockllm/model \
      -T packages=base -T replay=path/to/answers --log-dir runs/revised-offline

Live drafting or judging requires the explicit task argument allow_api=true.
Replay checks plumbing; it does not show a model learned from the new material.
"""

import json
import re
import sys
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.model import ChatMessageSystem, ChatMessageUser, GenerateConfig, ModelOutput, get_model
from inspect_ai.scorer import Score, Target, mean, scorer
from inspect_ai.solver import Generate, TaskState, generate, solver

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dg.package import CONDITIONS  # noqa: E402
from dg.revised_inputs import PROFILE, ROOT, grading_hash, input_hash, load_inputs, verify_prepared  # noqa: E402
from dg.revised_judge import judge_messages, parse_judge, summarize, validate  # noqa: E402

TESTED_CONFIG = GenerateConfig(effort="high", max_tokens=64000)
JUDGE_MODEL = "anthropic/claude-fable-5-1"
JUDGE_CONFIG = GenerateConfig(effort="high", max_tokens=64000)
DOC = re.compile(r"\bDOC-\d{3}\b")
PAGE = re.compile(r"\b(DOC-\d{3})\b\s*[,:(]?\s*(?:pages?|pp?\.)\s*(\d+)(?:\s*[-–]\s*(\d+))?", re.I)


def require_authorization(replay, judge, allow_api):
    """Reject unapproved calls before constructing the task."""
    live_judge = judge not in ("none", "") and not judge.startswith("file:")
    if (not replay or live_judge) and allow_api is not True:
        raise ValueError("Live drafting or judging is disabled. Use saved-answer replay and no judge/file judge for offline checks; a live run requires allow_api=true.")


def as_messages(messages):
    classes = {"system": ChatMessageSystem, "user": ChatMessageUser}
    return [classes[m["role"]](content=m["content"]) for m in messages]


def require_answer(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Empty drafter response: no quality score or safety result can be assigned.")
    return value


def code_candidates(raw_answer, package):
    """Check explicit record/page references, without inferring format or audience."""
    require_answer(raw_answer)
    findings = []
    for doc in sorted(set(DOC.findall(raw_answer)) - set(package.documents)):
        findings.append({"check": "unknown_document_reference", "detail": doc})
    for doc, start, end in PAGE.findall(raw_answer):
        doc = doc.upper()
        if doc not in package.documents:
            continue
        first, last = int(start), int(end or start)
        if first < 1 or last < first or last > package.page_count(doc):
            findings.append({"check": "page_reference_out_of_range", "detail": f"{doc}: {first}-{last}; document has {package.page_count(doc)} pages"})
    return findings


def preflight(pid):
    verify_prepared(pid)
    return load_inputs(pid)


def unchanged_input(state):
    package, messages, truth = preflight(state.metadata["package_id"])
    if input_hash(messages) != state.metadata["input_sha256"] or grading_hash() != state.metadata["grading_sha256"]:
        raise ValueError("Prepared inputs or grading materials changed after this run started; no grade can be assigned.")
    return package, messages, truth


@solver
def replay_answer(folder):
    async def solve(state: TaskState, generate: Generate):
        raw = require_answer((ROOT / folder / f"{state.metadata['package_id']}.txt").read_text())
        state.output = ModelOutput.from_content(model="replay", content=raw)
        state.messages.append(state.output.message)
        return state
    return solve


@scorer(metrics=[mean()])
def revised_candidates():
    async def score(state: TaskState, target: Target):
        package, _, _ = unchanged_input(state)
        findings = code_candidates(state.output.completion, package)
        return Score(value=len(findings), answer="REVIEW CANDIDATES ONLY",
                     explanation="Reference checks only; this is not a quality or safety score.\n" + json.dumps(findings, indent=2),
                     metadata={"profile": PROFILE, "findings": findings,
                               "input_sha256": state.metadata["input_sha256"],
                               "grading_sha256": state.metadata["grading_sha256"]})
    return score


@scorer(metrics={"quality_in_scope": [mean()], "serious_errors": [mean()]})
def revised_judge_score(judge, allow_api=False):
    require_authorization("saved-answer", judge, allow_api)

    async def score(state: TaskState, target: Target):
        package, messages, truth = unchanged_input(state)
        raw_answer = require_answer(state.output.completion)
        request_messages = judge_messages(package, messages, truth, raw_answer)
        attempts, verdict, problems = [], None, []
        from_file = judge.startswith("file:")
        for attempt in range(1 if from_file else 2):
            raw = ""
            try:
                if from_file:
                    raw = (ROOT / judge[5:] / f"{package.package_id}.json").read_text()
                else:
                    output = await get_model(judge, config=JUDGE_CONFIG).generate(as_messages(request_messages))
                    raw = output.completion
                verdict = parse_judge(raw)
                problems = validate(verdict, truth, package, raw_answer)
            except (ValueError, KeyError, TypeError, AttributeError, OSError) as error:
                verdict, problems = None, [f"unreadable judge record: {error}"]
            attempts.append({"attempt": attempt + 1, "raw": raw, "problems": problems})
            if not problems:
                break
        metadata = {"profile": PROFILE, "judge": judge, "judge_source": "saved_record" if from_file else "live_api",
                    "attempts": attempts, "verdict": verdict, "input_sha256": input_hash(messages),
                    "grading_sha256": state.metadata["grading_sha256"],
                    "judge_input_sha256": input_hash(request_messages), "judge_messages": request_messages}
        nan_values = {"quality_in_scope": float("nan"), "serious_errors": float("nan")}
        if problems:
            return Score(value=nan_values, answer="REJECTED", explanation="No grade or safety result.\n" + "\n".join(problems),
                         metadata={**metadata, "summary": None, "status": "rejected"})
        summary = summarize(verdict, truth)
        pending = summary.get("safety_gate") == "review" or summary.get("quality_points") is None
        values = nan_values if pending else {
            "quality_in_scope": summary["quality_points"] / summary["quality_max"] if summary["quality_max"] else float("nan"),
            "serious_errors": summary["serious_errors"],
        }
        return Score(value=values, answer="PENDING REVIEW" if pending else str(summary["safety_gate"]).upper(),
                     explanation=json.dumps(summary, indent=2),
                     metadata={**metadata, "summary": summary, "status": "pending-review" if pending else "accepted"})
    return score


@task
def disclosure_guard_revised(packages: str | list = "", replay: str = "", judge: str = "none", allow_api: bool = False):
    """New taught/open-response condition; live calls require explicit authorization."""
    judge = JUDGE_MODEL if judge == "default" else judge
    require_authorization(replay, judge, allow_api)
    ids = (packages if isinstance(packages, list) else [p.strip() for p in packages.split(",") if p.strip()]) or CONDITIONS
    if len(ids) != len(set(ids)) or any(pid not in CONDITIONS for pid in ids):
        raise ValueError("Packages must be unique identifiers from base, T1, T2, T3, T4, T5, T6, T7.")
    samples = []
    for pid in ids:
        package, messages, truth = preflight(pid)
        if replay and not (ROOT / replay / f"{pid}.txt").is_file():
            raise ValueError(f"No saved response for {pid}; offline replay cannot continue.")
        samples.append(Sample(id=pid, input=as_messages(messages), target="",
                              metadata={"profile": PROFILE, "package_id": pid, "input_sha256": input_hash(messages),
                                        "grading_sha256": grading_hash(), "documents": len(package.documents),
                                        "pages": package.total_pages(), "response_source": "replay" if replay else "live_api",
                                        "replay_folder": replay, "pair_constraints": truth.get("pair_constraints", []),
                                        "scored_requests": truth["scored_requests"]}))
    scorers = [revised_candidates()] + ([revised_judge_score(judge, allow_api)] if judge != "none" else [])
    return Task(dataset=MemoryDataset(samples), solver=[replay_answer(replay) if replay else generate()],
                scorer=scorers, config=TESTED_CONFIG,
                metadata={"profile": PROFILE, "live_calls_authorized": allow_api, "response_mode": "open_format"})
