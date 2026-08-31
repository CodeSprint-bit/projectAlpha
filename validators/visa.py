import re


def extract_visa_number(text):

    patterns = [
        r"visa\s*(?:number|no\.?)\s*[:\-]?\s*([A-Z0-9]+)",
        r"document\s*(?:number|no\.?)\s*[:\-]?\s*([A-Z0-9]+)",
    ]

    text_upper = text.upper()

    for pattern in patterns:

        match = re.search(pattern, text_upper)

        if match:
            return match.group(1)

    return None


def validate_visa(user_visa, extracted_visa):

    if not extracted_visa:
        return "VISA number not detected"

    if not user_visa:
        return "VISA number not entered"

    if extracted_visa.upper() == user_visa.upper():
        return "VISA number matches"

    return "VISA number mismatch"


def validate_visa_format(visa):

    if not visa:
        return False

    pattern = r"^[A-Z0-9]{5,20}$"

    return bool(re.fullmatch(pattern, visa.upper()))
