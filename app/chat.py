"""Study Partner Suggester — chat module.

This module sends user personal information to an external OpenAI language model
in order to rank and suggest compatible study partners.

Data transmitted to the external AI service
-------------------------------------------
* Requesting user : display name and email address (``user['name']``, ``user['email']``).
* Candidate users : display name and email address for every entry in ``candidates``.
* User message    : the free-text message supplied by the requesting user.

Privacy safeguards expected from callers
-----------------------------------------
* Only call this function after obtaining appropriate consent from (or on behalf of)
  all individuals whose data is included, including minors.
* Do not pass more candidates than necessary (data-minimisation).
* The OpenAI API is subject to OpenAI's data-processing terms; ensure those terms
  are compatible with your privacy policy and applicable law before deployment.
"""
from openai import OpenAI

client = OpenAI()


def suggest_partners(user: dict, message: str, candidates: list[dict]) -> str:
    """Ask the AI to suggest study partners for this user.

    Sends a prompt to the configured OpenAI model containing the requesting
    user's name and email, the user's free-text message, and the name and
    email of every candidate in ``candidates``.  The model returns a
    natural-language recommendation.

    Args:
        user:       Dict with at least ``'name'`` (str) and ``'email'`` (str)
                    for the requesting user.
        message:    Free-text message from the requesting user describing what
                    they are looking for in a study partner.
        candidates: List of dicts, each with at least ``'name'`` (str) and
                    ``'email'`` (str), representing the pool of potential
                    study partners.

    Returns:
        A string containing the model's study-partner suggestion.

    Privacy note:
        All name and email values — including those of minors — are included
        verbatim in the prompt sent to the external OpenAI API.  Callers must
        ensure valid consent and data-handling agreements are in place before
        invoking this function.
    """
    candidate_text = "\n".join(f"{c['name']} <{c['email']}>" for c in candidates)
    prompt = (
        f"User {user['name']} ({user['email']}) says: {message}\n"
        f"Possible partners:\n{candidate_text}\n"
        "Suggest the best study partners."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
