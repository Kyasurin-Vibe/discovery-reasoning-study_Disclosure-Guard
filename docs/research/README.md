# Discovery Reasoning Study

> **Research in progress — not legal advice.** This is an experimental AI-reasoning study using fictional discovery materials, not a validated legal-service product. The author is not a licensed attorney, and the work has not undergone comprehensive independent attorney review or peer review. Methods, references, findings and interpretations remain provisional and subject to further review; only Base has completed author adjudication. Any future discovery tool remains proposed development requiring technical and professional evaluation. Nothing here creates an attorney-client relationship or should be relied on for a real legal matter. See the [full disclaimer](DISCLAIMER.md).

**[Interactive research website](https://Kyasurin-Vibe.github.io/discovery-reasoning-study_Disclosure-Guard/)** · [Verification instructions](https://github.com/Kyasurin-Vibe/discovery-reasoning-study_Disclosure-Guard/blob/main/VERIFY.md)

Professional judgment can fail quietly: an answer may look right while missing an issue the governing principles required it to identify. This project studies where principle application breaks down in AI, both when a model drafts professional work and when another model evaluates it, using California discovery as a high-stakes test domain.

In a pilot, the drafter received a principles outline yet imported a threshold from an adjacent request, an error that motivates a hypothesis about inappropriate pattern transfer rather than principle application. An AI judge ratified the error. The judge and the author gave the same total (70/78) while disagreeing on which requests failed: **outcome scores concealed an oversight failure.**

A proposed next stage would use newly invented rules and opinions to reduce dependence on memorized jurisdiction-specific law, although general pretrained knowledge may still play a role. It would compare whether models apply principles better when given a distilled outline, cases alone, or cases from which they must induce their own outline, as law students do. The goal is evaluation and oversight methods that reveal what outcome scores hide, and that can inform risk management for high-stakes AI use.

Independent research using fictional records. **Not legal advice; no comprehensive attorney review.**

## Motivation

In my legal training, the emphasis was not on memorizing cases or rules but on distilling them into an applicable outline and applying it to new facts. The Carnegie Foundation's study of legal education found that law school develops a distinctive habit of legal thinking quickly, and criticized how weakly that thinking is integrated with practice and professional ethics ([Sullivan et al., *Educating Lawyers: Preparation for the Profession of Law*, 2007; Foundation summary](https://archive.carnegiefoundation.org/publications/pdfs/elibrary/elibrary_pdf_632.pdf)). Lawyers also take on work in fields they did not study; the ABA Model Rules recognize that a lawyer can become competent in a novel field through necessary study or by associating with an experienced lawyer ([Model Rule 1.1, Comment [2]](https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_1_1_competence/comment_on_rule_1_1/)). This raises a question I have not seen answered: is the path from legal training to competent practice driven by exposure to enough cases, or by repeated training in applying principles to facts?

**Why this matters for AI.** An AI system can absorb far more cases from a practice area than any person. But if we assume that an AI learns the way a human attorney does, that assumption is itself a risk. Humans also differ in how deeply they learn and how well they apply what they learn. I want to study this gap directly: when a model is given principles distilled from cases, does it apply them to unfamiliar facts, or does it reproduce surface patterns from nearby examples?

**What the pilot shows.** In the Base condition, the drafter received a principles outline yet imported a $500 threshold from an adjacent request into a request that contained no such limit (R12). An AI judge accepted it. This single instance is consistent with pattern transfer rather than principle application. It is a hypothesis, not a finding.

## Research question

In rule-governed professional domains such as law, knowing the applicable rules is not the same as applying them correctly to specific facts. A decision may appear reasonable while overlooking a material issue that the governing principles required it to identify.

The same gap matters for AI evaluation. An AI system may produce a plausible answer, or assign a seemingly reasonable score, without identifying every material omission in the work it evaluates. When AI evaluates AI, omissions can compound: a judge that misses a drafter's omission ratifies it. A correct-looking final judgment, or agreement on an aggregate score, does not establish that the relevant principles were applied.

> **When an AI applies explicitly stated principles—to draft professional work or to evaluate it—which material issues does it fail to identify, at what step of principle application does the failure occur, and can an outcome-level score reveal it?**

| Sub-question | Base evidence |
|---|---|
| **Drafter:** which material issues does the initial answer omit, and at which step (reading the request, spotting the issue, applying the rule)? | R12: a $500 cutoff imported from another request |
| **Judge:** given principles, rubric and reference, does an AI judge detect the drafter's omissions? | R12 accepted at full credit; a privilege-log index omission (P-1) missed |
| **Measurement:** does agreement on a total imply agreement on the judgment? | Both totals 70/78, with different findings |
| **Reference:** can an apparent judge error originate in the reference standard? | R7/R10 reference-applicability disputes |
| **Designed, not yet adjudicated:** do judgments stay stable under irrelevant labels or client pressure, and consistent across paired variants? | T1–T7 outputs and initial reviews exist; author review pending |

**Material omission:** an issue that the stated principles and evaluation criteria required to be identified, whether or not the reference answer lists it, and whose absence could materially affect the evaluation, its justification, or the assessment of the underlying work.

*Scope: one fictional California discovery case; one condition (Base) fully adjudicated by the author, non-blind. A method demonstration and hypothesis source, not a measured error rate.*

## Overview

Discovery is the exchange of information and documents during litigation. A useful draft must identify what can be provided, what is missing, which requests need objections, and which facts or decisions need a person’s review. A polished answer can still be wrong about what was requested.

I researched California discovery law using **LexisNexis Lexis+ Protégé and Westlaw CoCounsel**, reviewed statutes and opinions, and organized rules, exceptions and decision boundaries into a source-linked teaching outline. The experiment asks how a model **uses that outline on new fictional facts**, not just whether it can recite legal rules. [Research process and case citations](LEGAL_RESEARCH_PROVENANCE.md).

Here, “learning” means using material supplied in context. Lasting learning or model-parameter training was not measured.

## What each model received

| Role | Materials provided | Task |
|---|---|---|
| **Opus: drafter** | Researched principles; a Sacramento worked example; case facts; the actual document requests; all evidence | Draft responses and identifiable production, with separate private notes identifying risks, missing facts and decisions for human review. No prescribed answer template. |
| **Fable: reviewer** | Everything Opus saw, plus Opus’s answer, a reference answer, rubric, scoring guide and package-specific key | Assess the answer and explain findings. It did not receive my later adjudications or Codex’s diagnostic labels. |
| **Author, with Codex assistance** | Original answer, Fable assessment, references and evidence | Review each Base request; separately assess Opus, Fable and limitations in the references. This review was not blind. |

**Model IDs, as recorded in the run files:** drafter `claude-opus-5-5` (requested as `anthropic/claude-opus-5-5`); judge `anthropic/claude-fable-5-1`. Both used medium effort. All retained runs date from 2026-10-24 (UTC). The judge call is made inside the scorer, so the judge's Inspect logs show the placeholder task model `mockllm/model`; the judge ID is recorded in each `RESULT.json`. Where records differ, the run logs and run files control.

There was **no live attorney or client confirmation during drafting**. The notes propose future human checks; they do not prove those checks occurred. I designed the materials and reviewed Base afterward. A limited earlier consultation about wording was not comprehensive attorney validation.

## Base findings

Both Fable and I gave Opus **70/78**, but identified different problems. Opus produced useful document references and human-review questions, yet imported another request’s **$500 cutoff** into a request with no such limit. I classified that narrowing as **Serious**. Fable accepted it. Equal totals concealed a consequential disagreement.

| Layer | Useful behavior | Main limitation observed |
|---|---|---|
| **Opus** | Connects evidence to production; flags uncertainty; keeps sensitive notes separate; resists the concealment request | Unsupported scope transfer, unnecessary objections, and incomplete links between answers and follow-up checks |
| **Fable** | Detailed request-level and overall review; identifies some specific confirmation gaps | Missed the scope error and a Minor log-index omission; other disagreements arose from how the reference applied |
| **References** | Make decisions inspectable | Some expected answers over-specified the task or favored facts not established by the evidence |

These are single-case observations, not general model rankings. Fable’s 70/78 is its score **for Opus**, not a score earned by Fable.

## Practical motivation

The intended use is to help a professional see **what needs attention before acting**. Documents can be missing; client statements can require verification; lawyers may need a follow-up discussion to resolve a dispute (“meet and confer”) or an updated response when additional records arrive. Those possibilities do not excuse an incomplete current answer. The system must complete supported work and make unresolved issues visible.

## Risk governance

Before building the study, I studied the EU AI Act ([Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)) and the Council of Europe Framework Convention on Artificial Intelligence ([CETS No. 225](https://rm.coe.int/0900001680afae3c)), and used them, together with the California Rules of Professional Conduct, as voluntary design references. They shaped the outline's safe-behavior layer (S1–S10: decision boundaries, evidence as non-instruction, client pressure, traceability, proportionate review and human authority). The model received those principles, not the legal instruments.

Some of the study's checks have conceptual parallels with the Act's requirements for high-risk systems: identifying material omissions resembles risk identification (Art. 9); preserved records relate to record-keeping (Art. 12), although hashes establish file identity, not lifecycle event logging; reserved decisions reflect human oversight (Art. 14); and the paired variants address one aspect of robustness (Art. 15), stability under changed facts. These are selected parallels, not implemented statutory controls. The study makes no determination of whether either instrument applies to it and makes no classification or compliance claim; a formal mapping is future work. A June 2025 Congressional Research Service report described no enacted U.S. federal legislation establishing broad regulatory authority over AI ([CRS R48555](https://www.congress.gov/crs_external_products/R/PDF/R48555/R48555.4.pdf)), which is why a comprehensive framework from another jurisdiction served as a reference.

## Research status

- **All eight packages:** model answers and initial Fable reviews completed.
- **Base:** author review completed, 70/78; R12 = 0/1/2, Serious.
- **T1–T7:** author review pending; T1, T2 and T7 are next priorities.
- **Next experiments:** proposed, not performed; see [Scope and future work](#scope-and-future-work).
- **Seeking:** expert review, engineering and research collaboration, and API funding; see [What this work needs](#what-this-work-needs).

I bring legal training and discovery experience and want to develop engineering methods for reliable, testable AI systems. Discovery is a demonstration project; I am open to other research problems. Future work includes an attorney-supervised tool, evidence-linked risk management, and controlled teaching/feedback experiments—not a claim that these have been validated. [My research reflection](RESEARCH_REFLECTION.md).

## Scope and future work

**Scope.** This study measures one stage of principle application: using an author-distilled outline on new facts. The model received no case opinions, and was not asked to induce principles itself. Because models are pretrained on large legal corpora, the study also cannot separate supplied principles from prior knowledge.

**Future work (proposed).** A fictional jurisdiction with invented rules and opinions would reduce reliance on memorized jurisdiction-specific law, though not on general pretrained knowledge. Conditions could compare (A) outline only, (B) cases only, (C) cases from which the model writes its own outline before answering, mirroring legal education, and (D) both, while varying the number of cases. A further condition could test whether one round of corrective feedback improves performance on new problems. All comparisons are in-context; no model training is proposed.

### What this work needs

| Need | Purpose |
|---|---|
| **Legal practitioners and subject-matter reviewers** | Practitioners and scholars across litigation and other legal fields to review the method, challenge its assumptions, and discuss adaptation to their practice. Reviewers familiar with California discovery can assess the current legal materials; a separate blinded reviewer could assess agreement on the judgments. |
| **LLM engineers and evaluation researchers** | Feedback on experimental design, judge reliability, statistical analysis across repeated runs, and reproducible infrastructure. A dedicated collaborator could co-design the fictional-jurisdiction study. |
| **API funding or credits** | The proposed design multiplies model calls: four conditions, several case counts, paired variants, repeated runs to measure variance, and a judge call for each answer. Funding would make these comparisons large enough to report uncertainty rather than single observations. |
| **Venues for feedback** | Presenting the method for critique at AI-and-law and evaluation venues, such as ICAIL, JURIX or the Natural Legal Language Processing (NLLP) workshop. No submission or acceptance is claimed. |

I welcome discussion with practitioners across different legal fields, as well as engineers and evaluation researchers. The current case is a starting point for examining professional principle application; I am interested in which reasoning and review methods could transfer across practice areas, and which would require different rules, evidence and professional expertise. Such transfer has not yet been demonstrated by this study.

Interested contributors can propose a review, identify a reproducible problem, or discuss a new practice-area application through a GitHub issue once this repository is published. No funding, collaboration or review is represented as already secured.

## Evaluation and analysis

| Method | Role in this study |
|---|---|
| **Principle application** | Connect the researched outline to the actual request, evidence and proposed action; informed by LegalBench’s reasoning vocabulary. |
| **Three quality dimensions + separate severity** | Score scope, substance/evidence and disposition/human review at 0/1/2 each. Serious/Minor findings remain separate. This is the project’s rubric, not an LSAT or bar-exam scale. |
| **Review of the reviewer** | Assess Fable’s evidence, omissions and reasoning; keep drafter errors, judge findings and reference limitations in separate columns. |
| **LSAT / Performance-Test-informed analysis** | Codex-added, retrospective descriptions of inference, assumptions, rule application and professional-task handling; no additional penalties. |
| **Paired variants** | Compare what should remain stable and what should change when one condition changes. Inspired by consistency-based evaluation; author analysis of T1–T7 is pending. |
| **Evidence-linked audit trail** | Preserve actual inputs, original outputs, versions and later decisions. An explanation is not proof of hidden reasoning; a matching hash establishes identity, not legal correctness. |

[Methodology and attribution](METHODOLOGY.md) distinguishes implemented procedures, retrospective analysis and proposed comparisons. No numerical judge-performance score or causal teaching effect is inferred.

## Research references

| Source | What this project draws from it |
|---|---|
| [California cases and statutes — full source map](LEGAL_RESEARCH_PROVENANCE.md) | Legal grounding for the author-researched outline; database summaries were research aids, not substitutes for primary authority. |
| [Sacramento County Public Law Library, Sample Discovery Documents](https://saclaw.org/wp-content/uploads/2023/05/Sample-Discovery-Documents.pdf) | A worked discovery-response example supplied to Opus, using the retained source’s pages 45–46; sample facts were not case evidence. |
| [Guha et al., LegalBench (2023)](https://arxiv.org/abs/2308.11462) | Vocabulary for legal reasoning, including identifying issues and applying rules; the present task combines several operations rather than implementing LegalBench. |
| [Cooper et al., Conceptual Reasoning Index (2026)](https://alignment.anthropic.com/2026/conceptual-reasoning-index/) | Methodological inspiration for rubric-based judgment review and consistency constraints across related questions. This study does not reproduce LMCA/ACCoRD or claim their expert validation. |
| [Chen et al., Reasoning Models Don’t Always Say What They Think (2025)](https://assets.anthropic.com/m/71876fabef0f0ed4/original/reasoning_models_paper.pdf) | Motivation for checking evidence, decisions and outputs rather than treating a model’s explanation as proof of its internal reasoning. |
| [Zheng et al., Judging LLM-as-a-Judge (2023)](https://arxiv.org/abs/2306.05685v4) | Motivation for preserving and reviewing judge findings; its reported biases are not assumed proven in this case. |
| [LSAC Logical Reasoning](https://www.lsac.org/lsat/taking-lsat/test-format/logical-reasoning), [LSAT Hacks](https://lsathacks.com/logical-reasoning-question-types/) and [California Performance Test guidance](https://www.calbar.ca.gov/admissions/examinations/california-bar-examination/california-bar-exam-grading) | References for later, Codex-added descriptive labels—not original grading rules or official exam scores. |

These sources are credited for their specific roles, not endorsement of the study. T1–T7 consistency outcomes remain pending author review. Source attribution does not itself establish permission to redistribute third-party material.

## Related studies

- [CaseGen (Li et al., 2025)](https://arxiv.org/abs/2502.17943): Chinese legal-document generation benchmark (500 cases); LLM judge validated against human annotation.
- [oab-bench (Pires, Malaquias Junior and Nogueira, 2025), *Automatic Legal Writing Evaluation of LLMs*](https://arxiv.org/abs/2504.21202): Brazilian bar-exam writing (105 questions); reports strong correlation between frontier-model judges and human grades on the approved exam answers studied.
- [PRBench (Scale AI, 2025)](https://arxiv.org/abs/2511.11562): expert-rubric tasks in law and finance.
- [APEX (Vidgen et al., Mercor, 2025)](https://arxiv.org/abs/2509.25721v6): professional tasks including legal work; v1.0 used a panel of LLM judges, while the current extended version (v6) uses a single judge.
- [HAQQ Legal AI Benchmark (2026)](https://www.haqq.ai/blog/legal-ai-benchmark-2026): vendor-reported; LLM-judge disagreements escalated to blind lawyer review.
- [Dual-Judge Evaluation Protocol (2026)](https://arxiv.org/abs/2608.24258): separates a quality score from equivalence to a reference answer.
- [Pandita, Korn, Welty and Homan, *Forest vs Tree: The (N, K) Trade-off in Reproducible ML Evaluation* (AAAI-26)](https://ojs.aaai.org/index.php/AAAI/article/view/39659): how to allocate an annotation budget between items and raters per item; this study has one author adjudicator and does not estimate inter-expert agreement.

## Documentation

- [Base Report](new%20docs/report/09_base-report.md)
- [Final Base review: separate Opus, Fable and reference findings](new%20docs/judge/author-review/base-final-review.md)
- [Legal research and full case citations](LEGAL_RESEARCH_PROVENANCE.md)
- [Records](EXPERIMENT_RECORDS.md), [privacy changes](REDACTIONS.json), [offline checks](RELEASE_CHECKS.json)

## Acknowledgments

**Research design and legal grounding.** The author led the research questions, legal-source investigation, synthesis of the teaching outline, case-design decisions and final Base adjudications. Legal training and discovery-work experience informed this work; research, material preparation and review were developed with AI assistance rather than independently expert-validated.

**AI-assisted development and evaluation.** Claude and OpenAI/Codex assistants supported implementation, fictional-document preparation, drafting, comparison and documentation. In the retained experiment, Opus served as drafter and Fable as the initial judge. Codex supported the author-review process and added the explicitly attributed retrospective diagnostic labels. These roles are distinct; AI assistance does not constitute independent attorney review. See [AI use in this study](AI_USE.md) for who did what.

**Educational and research resources.** Credit is due to Sacramento County Public Law Library for the worked example, and to the researchers and organizations linked in Research references for the specific concepts described there. Full legal-source citations appear in the provenance appendix. No institutional endorsement, sponsorship or external expert validation is claimed.

## License

This is a **noncommercial, source-available research release**. It is not offered under the MIT License or CC BY 4.0.

- **Author-controlled code** (`evals/`, `scripts/`, `tests/`, `verify_release.py`, and other author-controlled Python source): [PolyForm Noncommercial License 1.0.0](LICENSE-CODE.md).
- **Author-controlled documentation and data** (reports, rubric, scoring guide, principles outline, fictional case materials, reference answers and author-review annotations): [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/). Attribute the Discovery Reasoning Study and indicate changes when reusing these materials.
- **Assessment and research verification:** the additional permission in [LICENSE](LICENSE) allows reviewers and researchers, including those at commercial organizations, to run the code and reproduce experiments for application assessment or independent verification. They may configure the environment, record necessary changes and report verification findings with attribution. This does not itself authorize commercial products, commercial deployment, paid services based on these materials or model training for commercial use.
- **Third-party material and dependencies are excluded** from these grants and retain their own terms. This includes the Sacramento County Public Law Library excerpt, third-party publications and any rights not controlled by the author. Public-domain material remains public domain.
- **Model outputs** remain preserved research records. No rights beyond those the author holds are granted; applicable provider and third-party terms remain relevant.

Uses outside these permissions require separate permission from the relevant rights holder. The author retains the ability to present and discuss their own work, submit applications and grant separate permissions for rights they control. See [LICENSE](LICENSE) for scope and terms.

## Limitations and verification

The author is **not a licensed attorney**. This is non-expert research informed by legal training, research and discovery-work experience. All case materials are invented, with no client information or actual law-firm case documents used. [Full disclaimer](DISCLAIMER.md).

Offline verification from this directory (no API/network):

```bash
python3 verify_release.py
# Include decoded PDF checks when the recorded pypdf dependency is installed:
python3 verify_release.py --deep
```

Use this release’s [manifest](https://github.com/Kyasurin-Vibe/discovery-reasoning-study_Disclosure-Guard/blob/main/MANIFEST.sha256); original hashes in records are provenance values.
