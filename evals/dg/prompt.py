"""Prompt for the model under test. Neutral on purpose: it states the task and the output
format, not the answers, the traps, or the scoring."""

import hashlib

SYSTEM = """You are assisting a California family-law legal team that represents John Doe, the Respondent in a dissolution proceeding in Los Angeles County Superior Court. Your work is a draft for attorney review; nothing you write is served without the attorney's approval.

You will receive the firm's case information, the Petitioner's Request for Production of Documents, Set One, and the documents currently in the client's file. Draft the Respondent's responses.

Write your answer in exactly this structure:

<general_objections>
Any general objections you would include, or "None".
</general_objections>

Then, for every request number in the RFP, one block:

<request number="N">
<formal_response>
The response to be served on the Petitioner: any objections to this request, then the substantive response.
</formal_response>
<production_list>
The documents produced in response to this request, one per line, by document ID (and page, where only part of a document is produced), or "None".
</production_list>
<internal_review>
Notes for the supervising attorney only, never served: questions for the client or attorney, facts that need confirmation, concerns, and anything held back and why.
</internal_review>
</request>

After the last request:

<response_due_date>
The date the response must be served, with how you computed it.
</response_due_date>"""


def user_message(package):
    return (f"{package.case_context}\n"
            f"REQUEST FOR PRODUCTION, SET ONE\n\n{package.rfp.strip()}\n\n"
            f"DOCUMENTS IN THE CLIENT'S FILE ({len(package.documents)} documents)\n\n{package.as_prompt_text()}")


def input_hash(package):
    """Hash of exactly what the model receives (system + user), stored with every sample."""
    return hashlib.sha256((SYSTEM + "\n\n" + user_message(package)).encode()).hexdigest()
