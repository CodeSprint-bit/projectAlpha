import re


def extract_aadhaar(text):

    pattern = r"\b\d{4}\s?\d{4}\s?\d{4}\b"

    match = re.search(pattern, text)

    if match:

        aadhaar = match.group()

        aadhaar = aadhaar.replace(" ", "")

        return aadhaar

    return None


def validate_aadhaar(user_aadhaar, extracted_aadhaar):

    if not extracted_aadhaar:
        return "Aadhaar not detected"

    if not user_aadhaar:
        return "Aadhaar not entered"

    user_aadhaar = user_aadhaar.replace(" ", "")

    if extracted_aadhaar == user_aadhaar:
        return "Aadhaar matches"

    return "Aadhaar mismatch"


def validate_aadhaar_format(aadhaar):

    if not aadhaar:
        return False

    pattern = r"^\d{12}$"

    return bool(re.fullmatch(pattern, aadhaar))
