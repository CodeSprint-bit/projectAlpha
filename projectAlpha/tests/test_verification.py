from utils import verify_document


def test_pan_match():

    result = verify_document(
        "pan",
        "Rahul Kumar",
        "ABCDE1234F",
        "INCOME TAX DEPARTMENT Rahul Kumar PAN ABCDE1234F"
    )

    assert result["success"] is True

    assert result["document"]["number_match"] is True

    assert result["document"]["detected_number"] == "ABCDE1234F"


def test_pan_mismatch():

    result = verify_document(
        "pan",
        "Rahul Kumar",
        "AAAAA1111A",
        "INCOME TAX DEPARTMENT Rahul Kumar PAN ABCDE1234F"
    )

    assert result["success"] is True

    assert result["document"]["number_match"] is False


def test_pan_not_detected():

    result = verify_document(
        "pan",
        "Rahul Kumar",
        "ABCDE1234F",
        "INCOME TAX DEPARTMENT Rahul Kumar"
    )

    assert result["success"] is True

    assert result["document"]["detected_number"] is None

    assert result["document"]["number_match"] is False


def test_name_similarity():

    result = verify_document(
        "pan",
        "Rahul Kumar",
        "ABCDE1234F",
        "INCOME TAX DEPARTMENT Rahul Kumar PAN ABCDE1234F"
    )

    assert result["identity"]["name_similarity"] >= 85


def test_invalid_document_type():

    result = verify_document(
        "passport",
        "Rahul Kumar",
        "ABC123",
        "Some document text"
    )

    assert result["success"] is False