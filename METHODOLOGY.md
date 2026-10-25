# Methodology and Attribution

Publication companion · 2026-10-24 · Describes the existing study; introduces no new grading rules

## Study flow and input boundaries

**Research → teaching outline → application to a fictional case → initial model assessment → author adjudication → retrospective analysis.**

The author used Lexis+ Protégé and Westlaw CoCounsel as research aids, reviewed legal sources, and synthesized rules, conditions, exceptions and decision boundaries into the outline. [Legal research provenance](LEGAL_RESEARCH_PROVENANCE.md) identifies the authorities and qualifications. This preparation is distinct from independent attorney validation.

Opus received the principles, selected Sacramento example, facts, actual document requests and all evidence. It drafted open-format responses, identifiable production and separate counsel-only notes. The task supplied no answer key and no required XML template. “Learning” denotes use of supplied material in context, not a measured parameter update or retention outcome.

Fable received the same learning/case materials plus Opus’s answer, a reference answer, rubric, scoring guide and case key. The retained assessment is free-form. No subsequent author rulings or Codex diagnostic labels were supplied to the initial judge. The author’s later review was non-blind and Codex-assisted; no live attorney/client confirmation occurred during model generation.

## 1. Professional-principle application

The observable task connects request interpretation, issue identification, relevant rules, evidence, a proposed disposition and a practical review question. [Guha et al., LegalBench (2023)](https://arxiv.org/abs/2308.11462) provides vocabulary for distinguishing legal reasoning operations. The project applies that vocabulary to a combined professional task; it does not implement or reproduce LegalBench or establish superiority over its tasks.

The analysis concerns what the draft actually states, identifies or leaves unresolved. It does not diagnose an inaccessible internal mechanism merely from an incorrect answer.

## 2. Quality, severity and human-review handling

The project’s own rubric scores each designated request in three dimensions: objections/scope; substance/evidence; and disposition/human review. Each receives 0, 1 or 2, for six points per request and 78 for Base. The author’s final Base score is 70/78. Serious/Minor classifications are separate research judgments, not statutory severity labels or extra points.

Human-review requirements distinguish client factual confirmation, attorney decisions and notices. The author checks meaningful notes and cross-references across the complete answer; a request to confirm is not a completed confirmation. Review flags do not automatically justify a proposed interpretation. For example, R12 retains production/review credit while its unsupported scope exclusion and incomplete substantive coverage receive separate justified deductions. Do not count overlapping descriptions as independent errors.

## 3. Assessing the judge and reviewing the reference

The author-review procedure records three separate layers:

| Layer | Question |
|---|---|
| Drafter | What did Opus state, produce, omit or refer for human review? |
| Judge | Is Fable’s finding, explanation, score or severity supported, and did it miss an author-established issue? |
| Reference | Is the supplied requirement supported by the task, available evidence and teaching materials, or does a limitation/conflict remain? |

A finding is linked to a requirement, exact text or precisely described omission, supporting evidence, and a disposition: confirm, reject, modify or unresolved. Original model records are not overwritten. R7/R10 reference-applicability disagreements are distinguished from R12’s author-confirmed missed scope error. No numerical Fable-performance scale was defined, so no composite judge score is invented.

[Zheng et al., Judging LLM-as-a-Judge (2023)](https://arxiv.org/abs/2306.05685v4) motivates attention to the limitations of model judging. Its reported biases and agreement figures are not assumed to apply to this case. [Cooper et al., Conceptual Reasoning Index (2026)](https://alignment.anthropic.com/2026/conceptual-reasoning-index/) provides a methodological analogy for rubric-based judgment comparison. This exposed, non-expert author adjudication is not LMCA expert validation or an unbiased estimate of judge accuracy.

## 4. Retrospective reasoning diagnostics

Codex added descriptive labels after the author’s request-level decisions. Their purposes are to explain supported observations and keep analytical layers distinct, not to create penalties.

| Lens | Questions / labels used | Source role |
|---|---|---|
| LSAT-informed | Rule application; missing supporting premise; inference strength; role of a statement; decision-relevant confirmation; inappropriate transfer across patterns | [LSAC Logical Reasoning](https://www.lsac.org/lsat/taking-lsat/test-format/logical-reasoning) and the author-selected [LSAT Hacks question-type guide](https://lsathacks.com/logical-reasoning-question-types/) inspire the project’s adapted LR tags. |
| Performance-Test-informed | Relevant/reliable facts, applying principles, ethical issues, action planning and professional communication | The [State Bar of California’s description](https://www.calbar.ca.gov/admissions/examinations/california-bar-examination/california-bar-exam-grading) informs adapted PT tags. It is not a new professional examination or an imported grading scale. |

These labels can describe accepted performance as well as problems, and can overlap. A missing organizational cross-reference need not be a formal logical fallacy. The [final Base review](new%20docs/judge/author-review/base-final-review.md) attributes labels to Codex and connects them to the author’s findings. No model-internal causal inference, official exam score or independent expert endorsement follows.

## 5. Paired variants: consistency and correctness

T1–T7 change specified conditions in one fictional case family. Some changes should leave a decision stable; others should change what can be produced or which justification is supported. Consistency and correctness must be considered separately: two consistent answers can both be wrong.

The design draws methodological inspiration from ACCoRD in the [Conceptual Reasoning Index](https://alignment.anthropic.com/2026/conceptual-reasoning-index/), which tests consistency constraints on related conceptual judgments. The legal pairs are an adaptation, not a reproduction of its probability/preference tasks. All variant drafts and initial reviews exist, but their author adjudication and final pair outcomes remain pending. This document reports no new twin result and does not treat related variants as independent cases.

## 6. Traceability, explanations and implementation checks

The project preserves actual inputs, evidence identifiers/pages, original model outputs, configurations, hashes, original judge judgments and subsequent author rulings. The sanitized publication copy has separate checksums and documented privacy/packaging changes. Hash validation and release scans establish particular integrity/privacy checks, not the truth of the legal analysis.

[Chen et al., Reasoning Models Don’t Always Say What They Think (2025)](https://assets.anthropic.com/m/71876fabef0f0ed4/original/reasoning_models_paper.pdf) motivates caution about treating model explanations as faithful accounts of internal causes. This study does not reproduce those experiments or infer a faithfulness rate for Opus or Fable. Evidence-linked notes are inspectable justifications, not access to hidden reasoning.

Technical development included input mismatches, truncation and assessment-format issues. These are recorded as different workflow/configuration stages rather than pooled as equivalent replicates. The current successful Base assessment is free-form; do not describe historical strict-schema validation as a required mechanism of this final run.

## 7. Educational example and original contributions

The supplied worked example is attributed to [Sacramento County Public Law Library, Sample Discovery Documents](https://saclaw.org/wp-content/uploads/2023/05/Sample-Discovery-Documents.pdf), using pages 45–46 of the retained source. It illustrates response practice; its facts do not become evidence in the fictional case and it is not a mandatory blank answer template.

The project-specific contributions are the author-led source synthesis, constructed case/pair specifications, grading references and explicit adjudication choices, developed with AI assistance. The original experimental artifacts establish which materials each role actually saw. This methodology text is later publication documentation, not a new prompt, rubric or claim that every referenced concept was independently validated.

See the [Base Report](new%20docs/report/09_base-report.md), [research reflection](RESEARCH_REFLECTION.md) and [disclaimer](DISCLAIMER.md). Independent legal and engineering review remain future work; no source organization is represented as endorsing or funding this project.
