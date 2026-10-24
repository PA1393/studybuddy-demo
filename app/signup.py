from datetime import date

USERS = []


def signup(name: str, email: str, birthday: date, zip_code: str):
    """Create a StudyBuddy account."""
    user = {
        "name": name,
        "email": email,
        "birthday": birthday,
        "zip_code": zip_code,
        "created": date.today(),
    }
    USERS.append(user)
    return user
