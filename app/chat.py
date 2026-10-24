"""Study Partner Suggester — app/chat.py

This module implements the Study Partner Suggester feature.

Behavior
--------
The ``suggest_partners`` function constructs a plain-text prompt that includes:
  - The requesting user's display name and email address.
  - A free-text message from that user.
  - The display names and email addresses of candidate study partners.

The assembled prompt is sent to the OpenAI chat completions API (model selected
by the OpenAI client default, typically ``gpt-3.5-turbo`` or the caller-configured
model).  The API response text is returned verbatim to the caller.

Personal-data handling
----------------------
Names and email addresses of both the requesting user and all candidates are
included in the prompt text transmitted to OpenAI.  Callers are responsible for
ensuring that:
  1. Users have been informed that their name and email will be shared with
     the OpenAI API for the purpose of study-partner matching.
  2. Only the minimum necessary personal data is passed in the ``user`` and
     ``candidates`` arguments.
  3. Data-retention and deletion obligations are satisfied upstream of this
     function; this module does not persist any data.

Privacy note
------------
Because this feature may process data belonging to minors, integrating teams
must verify applicable privacy regulations (e.g., COPPA, FERPA, GDPR) before
deploying this functionality in production.
"""

from openai import OpenAI

client = OpenAI()


def suggest_partners(user: dict, message: str, candidates: list[dict]) -> str:
    """Ask the AI to suggest study partners for this user.

    Constructs a prompt from the user's name, email, and message together with
    the name and email of each candidate, then calls the OpenAI chat completions
    API and returns the model's plain-text suggestion.

    Parameters
    ----------
    user : dict
        Must contain ``'name'`` (str) and ``'email'`` (str) for the requesting
        user.  Both values are sent to the OpenAI API.
    message : str
        The user's free-text request or description used to guide partner
        selection.  This text is sent verbatim to the OpenAI API.
    candidates : list[dict]
        Each element must contain ``'name'`` (str) and ``'email'`` (str).
        All names and emails are included in the prompt sent to the OpenAI API.

    Returns
    -------
    str
        The model's suggestion text as returned by the OpenAI API.
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
