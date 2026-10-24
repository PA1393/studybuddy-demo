from openai import OpenAI

client = OpenAI()


def suggest_partners(user: dict, message: str, candidates: list[dict]) -> str:
    """
    Ask the LLM (OpenAI chat completion) to suggest study partners for a user.

    Prompt structure
    ----------------
    The prompt sent to the model contains:
      - The requesting user's full name and email address.
      - The user's free-text message describing what they are looking for.
      - A newline-separated list of candidate names and email addresses.
    The model is asked to return a plain-text recommendation of the best matches.

    Personal data used
    ------------------
    * user['name']       – full name of the requesting student
    * user['email']      – email address of the requesting student
    * candidates[*]['name']  – full name of each candidate student
    * candidates[*]['email'] – email address of each candidate student

    Privacy considerations
    ----------------------
    This function transmits students' names and email addresses to the OpenAI
    API. If any of the students are minors, the caller must ensure that:
      1. Appropriate consent or legal authority exists before sending their
         personal data to a third-party AI service.
      2. The minimum necessary data set is used (consider passing only
         anonymised or pseudonymised identifiers if the model does not need
         real names/emails to make useful suggestions).
      3. Data retention and processing terms with the AI provider are
         compatible with applicable privacy regulations (e.g. COPPA, FERPA,
         GDPR) for the user population.

    Safeguards and limitations
    --------------------------
    * No built-in output filtering is applied to the model's response.
      Callers are responsible for validating or sanitising the returned text
      before displaying it to users.
    * The function does not log or persist the prompt or the model's response;
      logging must be handled by the caller if an audit trail is required.
    * Candidate selection (who appears in `candidates`) is controlled entirely
      by the caller; this function does not apply any access-control checks.
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
