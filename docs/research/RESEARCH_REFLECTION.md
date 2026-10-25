# Research Reflection: Professional Judgment, AI Evaluation and Engineering Practice

2026-10-24 · Author-led research reflection, drafted with AI assistance · No new experiment or grading standard

## Research position

I bring legal training and practical experience with discovery work. My contribution is not simply knowledge of rules: it is identifying where requests, evidence, professional obligations, client preferences and decision authority must be connected. I want to complement that judgment with an engineering mindset: explicit specifications, reliable interfaces, reproducible tests, failure analysis and measurable trade-offs.

This project uses discovery as a concrete way to demonstrate those interests. It does not define the only problem I want to work on. I am open to broader research on principle application, evaluation, professional decision support and AI risk management, and I would value systematic learning and mentorship from engineers and researchers working on large language models.

## The legal-research contribution behind the outline

Before the model runs, I investigated the discovery principles using LexisNexis Lexis+ Protégé and Westlaw CoCounsel. My questions asked for the rule, elements, exceptions, facts that do not decide the outcome, facts that would change it, and the relevant authorities. I reviewed statutes and opinions and recorded corrections when an AI summary, citation or overbroad statement did not fit the primary source. I then organized the research into an outline that the drafter could apply to new facts. This source-selection and interpretation work is part of the research contribution, not simply a prompt that says “follow principles.”

The [legal-research provenance appendix](LEGAL_RESEARCH_PROVENANCE.md) provides full citations for every case expressly named in the supplied outline and distinguishes broader research-history authorities. The appendix does not redistribute licensed database exports, assert current citator status, or claim that the teaching outline is legally infallible. Its development and the later reference disputes are both part of the record.

## Question and scope

The primary question is whether an AI can apply explicitly supplied professional principles across a complex discovery task, maintain appropriate judgment under client pressure, and identify insufficient evidence or decisions requiring human review. A separate question examines whether an AI judge’s findings are supported, and whether disagreements arise from the drafter, judge or reference materials.

All eight related packages have a completed model answer and initial Fable review. Only Base has completed my request-by-request author adjudication. I plan to continue investigating the variants, with T1, T2 and T7 among the next priorities. These are related versions of one invented case, not independent client matters or proof of performance across discovery practice.

## What I learned from the results

### Opus: useful application, consequential boundaries

The useful feature was not just a polished formal response. Opus connected documents to requests, proposed production, identified uncertainty, and wrote notes for the intended professional reviewer. It distinguished proposed external responses from counsel-only concerns and did not simply accept the client’s request to conceal the box. These are observable behaviors, not proof that the model acquired lasting professional knowledge.

The most consequential failure was R12. The model borrowed the $500 threshold from another request even though this request supplied no such limit. Its resulting inability response addressed a narrower universe of records. I adjudicated scope 0, substance 1 and disposition 2, with a Serious scope finding. Existing document references and review flags earned credit without curing the underlying scope problem. This is not proof that a specific low-value document was actually withheld or that the draft was served.

Other limitations included unnecessary ambiguity objections and incomplete links between response text and follow-up confirmation. A long, apparently careful answer can contain useful components without connecting them adequately. Asking counsel to approve an interpretation is valuable, but it does not automatically make the interpretation supported.

### Fable: detailed review is useful, but not final authority

Fable’s request-level and package-level organization was useful. It examined audience boundaries, production, protection and confirmation needs, and identified some gaps I agreed with. For example, saying a tenant is “believed” to possess a lease is not the same as confirming the basis for that belief.

However, Fable accepted the unsupported R12 threshold and missed a Minor request-index omission in the privilege log. I also disagreed with some deductions involving provisional drafting and a transaction-fact statement. These disagreements need different treatment: R7 and R10 involved requirements that the supplied reference really did contain, so rejecting those deductions in author adjudication does not show that Fable failed to read its key.

Both Fable and I assigned Opus 70/78, but with different request scores, reasons and safety findings. This is why a single total is not enough to evaluate either the drafter or the judge. My assessment of Fable is separately recorded as confirmations, modifications, rejections and missed findings; there is no invented numerical judge-performance score.

### The reference also needs review

The reference answer is not perfect. House 3’s evidence did not establish loan absence, and some reference questions reached beyond what I considered necessary for the immediate document-production task. My later adjudications are disclosed alongside the original standards; they do not retroactively turn this into a blinded or unchanged reference evaluation.

This three-layer distinction matters: a draft can be wrong, a judge can be wrong, and the reference can be incomplete or inapplicable. Human judgment is also reviewable. My author decisions are a transparent research record, not authoritative legal truth.

## What I learned about running the experiment

### A research idea must become an executable input contract

My intended question involved applying supplied principles. In the earlier paid condition, the principles outline was not actually supplied to the drafting model. Those outputs therefore did not answer my intended teaching-material question. They remain development history and a distinct condition, not equivalent observations that can be pooled with the completed Base result.

The lesson is to specify and verify what the agent must do before any paid dispatch: which task and version to use, exactly which learning materials and evidence each role receives, which materials must be excluded, where outputs are saved, and when it must stop. Describing a research goal to an agent is not a substitute for checking the actual assembled request.

A stronger preflight would verify required content, package identity, model/settings, hashes, output paths and existing-run status. I also need to distinguish my approval of a workflow from an assumption that every intended input was transmitted. This is a lesson about the research orchestration, not a claim that the drafting model refused to use material it received.

### API engineering is part of research design

The development process included truncation, quotation-validation problems, a rejected structured-output schema and a judge attempt with incomplete materials. These are different failure types and configurations, not repeated measurements of the same unchanged experiment. The retained Base report uses the successful medium-effort, full-materials, free-form records.

Output budgets must account for reasoning and visible-answer tokens. Concurrency and rate limits must be considered before launching several large packages. Transport retries must be distinguished from a paid second grading attempt. Saving a completed draft before grading and checking for existing work can prevent accidental duplication. Format validation should not mistake harmless Markdown differences for fabricated evidence, but relaxing validation must not silently turn missing assessments into full credit.

These experiences consumed time and paid API usage. I have not used this reflection to invent an audited total for all development expenditure. Nor does one high-effort truncation followed by one medium-effort completion prove that a particular setting is generally cheaper or better. Future operational studies should measure completeness, cost, latency, technical failures and reviewer burden under explicitly fixed conditions.

## Future work and collaboration

One possible application is a discovery assistant that links each request to its scope, evidence, proposed production and unresolved human questions. It would be an attorney-supervised workflow, not autonomous legal representation. Development would require expert review, usability work, engineering review and testing on fresh cases.

The same design could inform a proposed risk-management framework: unsupported scope exclusions, protected-content exposure, unverified factual claims, judge misses, reference conflicts, human authorization and an auditable correction history. This could later be examined in relation to general AI governance and EU AI Act research. The present study does not establish regulatory applicability, risk classification or compliance. The official legislation is a future research reference, not an implemented standard in this experiment: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng).

Further work could separate principles, examples and purpose/audience guidance into controlled comparisons; test predefined feedback and correction; and assess whether revisions introduce new errors. Those experiments have not been performed. No reinforcement-learning update, professional qualification test or deployment validation is claimed.

I am seeking qualified legal reviewers, evaluation collaborators, engineering feedback and mentorship. Research funding or API credits would support additional model runs and independent review. T1–T7 are included for interested researchers to examine, but public availability should not be claimed until publication actually occurs. An interactive presentation with evidence-linked examples may later help readers explore the study; its visual design and implementation remain separate future work.

## Authorship and limitations

This reflection is AI-assisted writing based on the author’s recorded experiences, judgments and stated goals. The author led the research and supplied the final adjudications through an AI-assisted discussion; AI systems also assisted material preparation, programming, drafting and review organization. Codex’s retrospective LSAT/Performance-Test labels are diagnostic descriptions, not official exam scores or new deductions.

The author is not a licensed attorney. This is not an expert legal review, legal advice, representation or a validated commercial legal tool. There has been no comprehensive attorney review; a limited prior consultation about response wording does not validate other conclusions. The story and evidence were invented from general patterns motivating the research, with no client information or actual law-firm case material used. Author review was non-blind and subject to personal judgment and shared AI-assisted assumptions. See the [Base Report](new%20docs/report/09_base-report.md), [final Base review](new%20docs/judge/author-review/base-final-review.md) and [disclaimer](DISCLAIMER.md) for the retained findings and boundaries.
