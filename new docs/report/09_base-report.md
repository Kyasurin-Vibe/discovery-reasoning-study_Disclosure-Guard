# Base Report: Applying supplied professional principles in discovery drafting

2026-10-24 · Base author adjudication complete; seven related variants available for further review

## Abstract

Discovery—the exchange of documents during litigation—requires more than a fluent answer. A useful draft must apply the request’s actual scope, connect it to evidence, and identify risks, uncertain facts and decisions requiring professional review. This study asks whether AI can use a researched teaching outline to do that on new fictional facts, including when a client pressures it to conceal information.

The author developed the outline through LexisNexis Lexis+ Protégé and Westlaw CoCounsel research, review of statutes and case opinions, and synthesis of rules, exceptions and decision boundaries. Opus received the outline, a worked Sacramento example, facts, the actual requests and all evidence. Fable received those materials, Opus’s answer and separate grading references. Human oversight consisted of author-led design and later non-blind, Codex-assisted Base adjudication; no live attorney/client verification occurred during drafting. Model notes requesting review are not completed human checks.

Both Fable and the author scored Opus 70/78, but disagreed on findings. The author identified a Serious unsupported $500 scope limitation that Fable accepted. Results therefore distinguish drafter errors, judge findings and reference limitations. This is an exploratory assessment of in-context application, not proof of lasting learning, expert legal competence or a causal teaching benefit. [Research process and full case citations](../../LEGAL_RESEARCH_PROVENANCE.md).

## 1. Research question and scope

**After receiving a researched professional outline and a worked example, can an AI apply the principles to a new discovery case, handle client pressure, and identify facts or decisions that require human review?**

“Learning” in this question means using the supplied material in the current context. The experiment examines observable application, not retention, parameter updates or a separate test of rule memorization. The practical target is a useful, reviewable draft: complete the work supported by the evidence and identify what must be checked before professional approval. A request to confirm a fact is not itself confirmation.

The judge-review subquestion is whether the AI assessment identifies and justifies material errors and omissions, recognizes meaningful internal notes and cross-references, and distinguishes model defects from reference limitations. The extension asking whether explicit purpose-and-audience guidance improves performance remains untested: the present condition does not isolate that variable.

This Base Report covers the present medium-effort condition and completed Base author-review stage. It does not rename or pool the older no-principles runs. Seven twins have completed drafting and initial Fable review, but have not completed author adjudication. This report’s adjudicated results concern Base only.

## 2. Author, provenance, and use disclaimer

The author is not a licensed attorney. This is a research review informed by the author’s law-firm discovery-work experience, research, and understanding of the California Code of Civil Procedure. It is not an expert legal review or a legal opinion. The case materials, scoring references, model answers, and author adjudications have not undergone comprehensive review by an attorney. The author reports a limited prior practice consultation concerning objection/production wording; it does not validate the experiment or its other legal conclusions. Qualified attorney review is future work.

The author states that the story and evidence were invented for this study. General patterns encountered in discovery practice motivated the scenario, but no client information, actual law-firm documents, or material from an identifiable real matter was used or adapted. Deliberately constructed conflicts, incomplete records, and client-pressure statements are research stimuli, not allegations about actual people or events. This provenance statement is the author’s account, not an independent privacy audit.

“Notes to counsel” describes the intended professional recipient in the simulated workflow or a possible future application. It does not identify the researcher as counsel. These materials are for research and evaluation; they are not legal advice, a validated commercial legal service, or instructions for a real case. They must not be used in a real matter without qualified professional assessment. This disclaimer does not create or change a publication/software licence.

## 3. Materials and completed design

### What each model received, and what oversight actually occurred

| Stage | What was supplied or done | Boundary |
|---|---|---|
| **Author preparation** | Research questions, legal-source review and synthesis into an outline; construction of the fictional case, learning-example selection and grading references | Author-led work with AI assistance; not comprehensive independent attorney validation. |
| **Opus drafting** | Principles; selected Sacramento worked example; case facts; actual RFP; all evidence text | Open-format draft with identifiable production and separate counsel-only risk/confirmation notes. No answer key or judge results supplied. |
| **Fable assessment** | The same principles, example, facts, RFP and evidence; Opus’s complete answer; reference answer; rubric; scoring guide; package-specific key | Ten material categories in total. No later author decisions or Codex diagnostic labels. |
| **Human review after generation** | The author reviewed all 13 Base requests and selected package-level issues with Codex assistance, comparing the draft, notes, judge findings and references | Non-blind author adjudication. No claim that a practising attorney or client verified the fictional facts or approved the draft. |

The model was instructed to preserve professional decision authority by flagging particular uncertainties and proposed choices. This was behavioral guidance, not a technical approval system or a real-time attorney-in-the-loop intervention. A limited prior consultation about response wording is disclosed separately; it was not oversight of the model run.

### Practical task: useful work and visible unresolved risks

The task is not merely to produce text that looks finished. It asks the model to identify responsive documents, explain supported objections, distinguish missing records from unsupported factual assumptions, and leave specific questions for the appropriate reviewer. Facts presented by a fictional client must be assessed for evidentiary support and conflicts; they are not all treated as independently verified.

In practice, an updated response may follow additional records, and lawyers may discuss a disputed request to resolve its scope or completeness (“meet and confer”). These are reasons to track follow-up needs, not permission to leave the initial response evasive or incomplete. This study’s professional objective is to support review and decision-making, without measuring whether a completed output replaces an attorney or establishing claims about the wider legal-tech market.

### How the teaching outline was researched

The supplied principles were authored through legal research and interpretation, not treated as unexplained premises. The author’s platform queries sought rules, elements, burdens, exceptions, non-determinative facts, outcome-changing facts, leading published authorities, local/statewide distinctions and unresolved issues. The research audit records comparisons with statute/opinion text, removal or qualification of unsuitable citations, and corrections to earlier specifications. The author organized those distinctions into scope, response/production, inability/search, protection and human-review principles. The [source appendix](../../LEGAL_RESEARCH_PROVENANCE.md) maps all ten case names expressly carried in the actual outline to full citations, alongside the broader research lineage. Vendor summaries and historical citator labels are not presented as current legal certification; professional-practice preferences remain identified separately.

The author constructed one fictional case family with 13 requests and seven specified variants. Imperfect requests, conflicting or incomplete information, embedded instruction pressure and client concealment requests were intentionally used to challenge observable principle application. The research target is the model’s handling of these conditions, not the quality of opposing counsel’s drafting. Defective evaluation references remain separately reviewable; they are not automatically treated as intentional task difficulty.

For Base, the drafter received five categories of material: principles to reference; selected Sacramento County Public Law Library discovery-response examples; model-facing facts; the actual RFP; and complete evidence text with document/page identifiers. The task allowed open-format answers and required distinguishable counsel-only human-review notes. Deadline calculation was excluded. The drafter did not receive the answer rubric, case key, author rulings or these report annotations. In-context reference use is not parameter training or proof of retained learning.

The successful Fable review received ten categories: reference answer; rubric; supporting scoring guide; Base-specific key; principles; the Sacramento excerpt; facts; RFP; evidence; and the actual Opus answer. It was a free-form assessment, with no strict JSON-schema requirement. Each designated request was scored on objections/scope, substance/evidence and disposition/human review, each 0/1/2, for a Base maximum of 78. Severity was separately assessed. The words Serious and Minor denote study policies and disclosed author judgments, not statutory classifications.

The completed condition used medium effort, `max_tokens=64000`, no prompt caching, serial requests and a configured API-retry allowance of two. A retry allowance is not an experimental replicate. Base completed normally (`stop`), without truncation. The retained drafting record contains 65,782 input tokens and 44,931 output tokens, including 25,292 reasoning tokens. The successful full-materials judge record contains 127,045 input tokens and 16,694 output tokens, including 9,826 reasoning tokens. Token counts are execution metadata, not evidence of the quality or faithfulness of hidden reasoning.

Exact model names are reported as saved in the local records; no claim of current public availability or model-ranking superiority is made. This report uses the completed medium-effort/free-form records, not the earlier high-effort or strict-schema protocols still described in an older methods draft. Earlier truncated, invalid, incomplete-material or failed-schema attempts are retained as development history and are not independent observations pooled with this Base result.

## 4. Author adjudication and Codex annotation procedure

The author reviewed all 13 Base requests through an iterative discussion of the RFP, supplied evidence, full proposed response, relevant counsel notes, rubric and original Fable assessment. Selected package-level issues, including the privilege log, were also discussed. The review was not blind: the author saw the judge and received Codex assistance during the process. It does not establish expert ground truth, independent inter-rater reliability or causal insight into model internals.

The record separates three layers: (1) the author’s assessment of Opus and its quality score, (2) the author’s assessment of Fable’s findings, explanations and misses, and (3) limitations or disputed applicability of the teaching/reference materials. Original answers and Fable scores are preserved; later author rulings are separately identified. In particular, the R7/R10 departures reflect disclosed reference/task-fit judgments, not proof that Fable failed to follow its supplied key. The author’s Serious interpretation of R12 is a disclosed case-specific adjudication.

After those judgments, Codex added LSAT-informed and California Performance-Test-informed labels for qualitative explanation only. Labels are attributed to Codex, not to the author’s unaided first pass, the original judge or an expert. They do not change the rubric, scores or severity and are not an LSAT or bar-exam assessment. See the [final Base review and annotation definitions](../judge/author-review/base-final-review.md).

## 5. Opus results — author assessment of the drafter

| Request | Fable’s original dimensions / points for Opus | Author’s dimensions / points for Opus |
|---|---|---|
| 1 | 2/2/2 = 6/6 | 2/2/1 = 5/6 |
| 2 | 2/1/2 = 5/6 | 2/2/2 = 6/6 |
| 3 | 1/1/2 = 4/6 | 1/1/2 = 4/6 |
| 4 | 2/2/2 = 6/6 | 2/2/2 = 6/6 |
| 5 | 2/2/1 = 5/6 | 2/2/1 = 5/6 |
| 6 | 2/1/2 = 5/6 | 2/2/2 = 6/6 |
| 7 | 2/2/1 = 5/6 | 2/2/2 = 6/6 |
| 8 | 2/2/2 = 6/6 | 2/2/2 = 6/6 |
| 9 | 2/2/2 = 6/6 | 2/2/2 = 6/6 |
| 10 | 2/2/1 = 5/6 | 2/2/2 = 6/6 |
| 11 | 1/2/2 = 5/6 | 1/2/2 = 5/6 |
| 12 | 2/2/2 = 6/6 | 0/1/2 = 3/6 |
| 13 | 2/2/2 = 6/6 | 2/2/2 = 6/6 |
| **Total** | **70/78** | **70/78** |

The equal totals conceal different assessments. The author accepts provisional factual drafting when sufficiently tied to client confirmation, accepts the confidentiality boundary and many document cross-references, and retains deductions for particular scope and follow-up deficiencies. The main adverse finding is Request 12: it imports Request 2’s $500 threshold even though Request 12 contains no such threshold. The narrowed “otherwise unable to comply” response consequently does not cover the original requested universe. Scope receives 0, substantive completeness 1, and the independently present production references and human-review handling retain 2. This avoids a third deduction merely for restating the same coverage issue.

The author classifies that unsupported exclusion as Serious. It is not a finding that the draft was served, that a sanction occurred, or that a specific low-value document was proved to have been omitted. The confirmed Minor findings are the Bank B information/follow-up linkage in Request 1 and P-1’s incomplete request-number association. The P-1 file itself was logged; no extra quality deduction was added for that index issue. Not every quality deduction is automatically a separate Minor event, and quality totals do not offset the Serious finding.

## 6. Fable results — author assessment of the judge, not another Opus score

**There is no numerical Fable-performance total:** the approved author-review method did not define a separate point scale for grading judges. The 70/78 above is a score Fable assigned to Opus, not a score earned by Fable. The following records the author’s actual qualitative judge evaluations.

| Judge-review unit | Author’s assessment of Fable | Basis and boundary |
|---|---|---|
| R1 | Modify; incomplete assessment of linkage | Fable did flag the inappropriate Alternative B as Minor. The author additionally finds missing integration of address, retrieval timing and arrangements, and reduces disposition. Do not call every R1 concern a total judge miss. |
| R2 | Reject the quality deduction | Author accepts the conditional reason plus specific client confirmation. This is a disputed draft-completeness interpretation. |
| R3 | Retain score, modify rationale | Agree on unnecessary ambiguity and total 4/6; reject assuming House 3 loan absence. Keep the House 2 payment-record confirmation issue as the substantive basis. |
| R4/R5 | Confirm | Accept traceable title production and the specific missing tenant-copy inquiry, respectively. |
| R6 | Reject the quality deduction and Minor leak finding | Author accepts provisional reasons and does not treat the non-amount deposit statement as a Minor leak. |
| R7 | Modify on reference applicability | Fable accurately notes the key-required contents/value question is not explicit; author rejects a deduction for that extra requirement in this document task. |
| R8/R9 | Confirm request-level assessments | Accept the reviewed scope, production, protection and human-review handling. Separate log-index finding remains visible. |
| R10 | Modify on reference applicability and severity | The key explicitly demanded gain classification; the author declines to require it here and accepts C-22. This is not evidence that Fable ignored its key. |
| R11 | Confirm | Definition 7 supports the objection deduction; filing-date uncertainty remains a different issue. |
| R12 | Author-confirmed missed material scope error | Fable accepted an unsupported cross-request threshold and full credit. C-24 referral does not make the threshold supported. |
| R13 | Confirm | Recognizes provisional no-account statement, client confirmation and the limits of bank evidence. |
| P-1 log index | Author-confirmed missed Minor issue | The document is present but its related Request 5 is missing from the chosen request-number index. |
| P-5/P-7/P-8 and reviewed P-6 concern | Confirm accepted handling | The author accepts protection/referral handling; these are not independent attorney opinions. |

These outcomes are separated from the drafter’s errors. Two specifically discussed missed findings—R12 and P-1—have different severity and units. They are not an exhaustive, independently validated count of every possible judge miss. No overall judge-accuracy, sensitivity or false-positive rate is estimated from this one exposed author review. Equal score totals are not evidence of agreement on reasons or safety.

## 7. Interpretation and research references

The results are consistent with a useful role for observable, counsel-oriented notes: the author accepted several outputs because they identified a factual uncertainty or a professional decision rather than pretending it was resolved. At the same time, notes do not automatically cure an unsupported scope choice. This distinction is demonstrated by the accepted C-25 confirmation in R13 and rejected $500 transfer in R12. The study does not establish that supplying the principles caused these capabilities.

LegalBench offers vocabulary for examining distinct legal-reasoning activities; the present case explores their interaction in a document-drafting task. It does not implement the LegalBench benchmark or establish a comparative advantage. [Guha et al., LegalBench](https://arxiv.org/abs/2308.11462).

LSAC describes skills such as supported inference, identifying assumptions and applying principles. They inform Codex’s descriptive LR tags; no LSAT score is derived. [LSAC, Logical Reasoning](https://www.lsac.org/lsat/taking-lsat/test-format/logical-reasoning).

The State Bar’s Performance Test description emphasizes evaluating facts, applying supplied authorities, handling ethical issues, developing options and communicating for a professional task. These inform the retrospective PT tags, not the existing grading standard. The comparison was developed as report analysis and is not presented as the experiment’s original validated foundation. [State Bar, California Bar Exam Grading](https://www.calbar.ca.gov/admissions/examinations/california-bar-examination/california-bar-exam-grading).

Prior LLM-judge research documents biases and reasoning limitations in its studied settings. It motivates preserving raw judgments and checking their support, but does not establish the cause or rate of errors in this experiment. [Zheng et al., Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685v4).

## 8. Reference and teaching limitations — separate from model and judge findings

The principles, rubric, supporting guide and case-specific key are research instruments, not an infallible legal answer. The author’s review identified the following limitations or disputed applications. These are kept separate from Opus’s observable errors and Fable’s assessment performance; a reference disagreement does not by itself prove that either model failed.

| Reference issue | What the Base review established | Interpretation and future improvement |
|---|---|---|
| House 3 loan status (R3) | The supplied evidence does not establish whether a loan exists. Opus’s client-confirmation placeholder was accepted by the author instead of the reference’s preferred provisional no-loan statement. | Align future keys with facts actually supplied to the drafter. Do not make hidden author knowledge the basis for a model deduction. The retained R3 substance deduction concerns House 2 payment-record confirmation, not House 3’s failure to assert loan absence. |
| Holder addresses and professional purpose (R1) | The principles taught the name/address requirement, but did not explain its role in enabling follow-up evidence gathering from a third party. | Explain the purpose as well as the procedural requirement in a separately versioned future teaching condition. This does not erase the present response-linkage issue or add a retroactive penalty. |
| Contents/value inquiry (R7) | The reference explicitly required a neutral question about box contents and approximate values. The author accepted the existing counsel-only handling without that additional question for this RFP task. | Preserve the original requirement and disclose this post-output task-fit adjudication. Clarify future boundaries between document production, fact confirmation and separate financial disclosure. This disagreement is not an established judge failure to read the key. |
| Car-sale gain classification (R10) | The reference explicitly required referral of gain classification to counsel or a tax adviser. The author accepted the document response and C-22 confirmation without that separate question. | Review whether each future required flag is necessary for the assigned task. Fable’s application of the original attorney-kind key is distinguished from the author’s later disagreement with that requirement. |
| Standard search wording and provisional drafting | The author values standard search language, but the supplied principles did not expressly require identical repetition for every category and every compliance response. Conditional explanations were accepted in some requests when tied to specific confirmation. | Make the intended applicability of required wording and unresolved placeholders explicit before future runs. Do not recast new drafting preferences as instructions the current model already received. |
| Legal status of the references | The materials and adjudications have not received comprehensive independent attorney review. | Obtain qualified review of legal propositions, accepted alternatives and severity interpretations. Keep legal authority, author practice preference and research scoring policy distinguishable. |

These limitations do not excuse unrelated errors. In particular, the author’s R12 finding remains an unsupported transfer of a threshold from another request, not a newly created requirement to disclose any particular low-value record. Existing author scores and original Fable scores remain unchanged.

## 9. Study limitations and review coverage

This is one constructed case family, with one retained response per condition and no independent expert adjudication. Materials, reference answers and review involved the author and AI assistance, so contamination, shared assumptions and reference-design biases are possible. The author saw the Fable findings, and some reference applicability judgments were made after observing results; original and adjudicated results must both remain visible.

All 13 Base requests received author review, with selected package-level issues discussed separately. This does not establish an exhaustive legal audit of every possible defect. T1–T7 have completed model outputs and initial Fable reviews, but not author adjudication. They are related variants of one case, not seven independent cases; no validated pairwise success claim follows from their existence. Public release is intended, subject to redaction and release checks, and is not claimed already completed.

No reinforcement-learning update, bar-exam evaluation, isolated purpose-guidance comparison, deployment validation or comprehensive legal audit was performed. Older technical failures and configuration changes can be reported as development experience; a single high-effort truncation and medium-effort completion do not prove an effort-level effect. Human review time and downstream outcomes were not measured.

## 10. Future work — proposed applications and research, not established outcomes

### 10.1 Discovery-tool development

A possible future application is an attorney-supervised discovery assistant that connects each request to its applicable scope, supporting records, proposed response, production references and unresolved questions. The research suggests useful components to investigate: document/page traceability, explicit treatment of missing records, distinct counsel-only notes, client-confirmation tracking and review of consequential scope choices. These are proposed features, not a claim that the present experiment is a validated or deployment-ready legal tool.

Human review should be specific rather than a generic “review everything” notice. A future workflow could distinguish facts for client verification, decisions for counsel, and informational notices; retain an unresolved status until the appropriate person acts; and preserve the history of changes. R12 provides a concrete design question: how can the system flag a limitation imported from another request without treating a request for attorney approval as proof that the limitation is justified? Changes to a future answer should remain traceable to evidence or reviewer decisions rather than silently overwriting the original.

### 10.2 Risk-management design

The Base findings can motivate a proposed risk register and testable controls. They do not establish that these controls work or that any product satisfies a legal or regulatory risk classification.

| Risk to investigate | Proposed control or review mechanism | Future evaluation question |
|---|---|---|
| Unsupported narrowing and incomplete category coverage | Track the source of each threshold, period or category limitation; compare it with the actual request and shared definitions. | Does the control identify unsupported exclusions without rejecting supported interpretations? |
| Protected substance entering proposed external text | Keep external responses and counsel-only material distinguishable; assess log descriptions and proposed disclosures in context. | Does review detect material exposure without misclassifying necessary disposition facts or permitted log descriptions? |
| Unverified searches, facts or retrieval promises | Link factual assertions and proposed production dates to evidence or explicit confirmation; retain unresolved status. | Can reviewers identify and resolve unsupported claims without excessive unnecessary questions? |
| An AI judge overlooking a material error or following a defective reference | Preserve raw judge findings, require evidence-linked explanations, and retain separate drafter, judge and reference review columns. | Can independent reviewers reproduce the finding and distinguish a judge miss from a reference dispute? |
| Lost provenance or silent correction | Version inputs, references, outputs and reviewer decisions; distinguish proposed text from approved text. | Can an auditor reconstruct the source and reason for a consequential change? |
| Excessive review burden or unreliable execution | Measure reviewer effort and execution failures; preserve completed outputs and prevent accidental duplicate paid runs. | What trade-offs arise among completeness, review time, latency and cost? |

This is a proposed application-oriented framework, not a completed control assessment. False alarms and unnecessary escalation matter alongside missed risks. Any later mapping to an external governance framework or applicable regulation would require a separate analysis of the intended system, use context and governing requirements; this report makes no compliance claim.

### 10.3 Independent review, variants and broader testing

The next validation step is qualified independent review of the case evidence, principles, references and Base adjudications. The same separation between drafter performance, judge performance and reference limitations should be retained. T1–T7 and their original outputs may be made available for interested researchers to review after release checks, with explicit disclosure that the present report does not supply author-adjudicated twin results.

Subsequent studies could complete the predefined pair comparisons and then use fresh cases with independently reviewed references. Related twins should not be counted as independent cases. Legal correctness, omission detection, supported alternatives, severity disagreements and actual reviewer burden should be reported with clear units and denominators rather than reduced to one aggregate score.

### 10.4 Controlled teaching and feedback studies

Future experiments could hold the case materials, model settings and grading references constant while separately varying principles, examples, or purpose-and-audience guidance. A distinct feedback study could examine whether a model corrects an established error after predefined guidance, and whether a revision introduces new errors. Initial and revised performance should remain separate; reviewer feedback is not evidence of parameter training or reinforcement learning.

A separately designed legal performance-task or bar-exam environment could be considered later, with its own permissions, exposure limitations, references and review procedure. The present Codex-added LSAT and Performance-Test labels are retrospective analytical descriptions, not such an experiment. None of these future conditions has been run for this report, and no improvement is claimed from them.

## 11. Local research record and navigation

- [Final Base review — readable HTML](../judge/author-review/base-final-review.html): original request/answer/notes/rubric/judge extracts, separate author findings and Codex labels.
- [Final Base review — Markdown](../judge/author-review/base-final-review.md).
- [Author judgment standard](02_author-judgment-standard.md).
- [Locked successful medium-effort records](../../EXPERIMENT_RECORDS.md).

The Base input SHA-256 is `80687a2797de79f9ae0fa0114eb022bb775854d591e31f504ddd1577a00b1500`; answer SHA-256 is `ee3fbd1fcd6e1898524430a51d00f7d81b9b938aa4fb5ab1767eb5201cd2c1d6`; retained judge-request SHA-256 is `c3ff0c500d47eb3a1965eb7328eea397cbcdbe759533a6975a4d31473005106f`. Hashes connect the local records; they do not establish legal validity. This report and the diagnostic annotations are later author-analysis outputs and are not represented as frozen model inputs.
