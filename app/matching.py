def rank_partners(user: dict, candidates: list[dict]) -> list[dict]:
    """Order candidate study partners, best first."""
    def score(candidate):
        same_zip = 1 if candidate["zip_code"] == user["zip_code"] else 0
        return same_zip * 10 + len(set(candidate.get("subjects", [])) & set(user.get("subjects", [])))

    return sorted(candidates, key=score, reverse=True)
