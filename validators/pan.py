import re


def extract_pan(text):

    pattern = r"[A-Z]{5}[0-9]{4}[A-Z]"

    match = re.search(pattern, text.upper())

    if match:
        return match.group()

    return None


def validate_pan(user_pan, extracted_pan):

    if not extracted_pan:
        return "PAN not detected"

    if not user_pan:
        return "PAN not entered"

    if extracted_pan == user_pan.upper():
        return "PAN matches"

    return "PAN mismatch"


def validate_pan_format(pan):

    if not pan:
        return False

    pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"

    return bool(re.fullmatch(pattern, pan.upper()))
