from app import app


def test_invalid_document_type():

    client = app.test_client()

    response = client.post("/api/verify",
                           data={
                               "documentType": "passport",
                               "name": "Rahul Kumar",
                               "document": "ABC123"
                           })

    assert response.status_code == 400

    result = response.get_json()

    assert result["success"] is False


def test_missing_name():

    client = app.test_client()

    response = client.post("/api/verify",
                           data={
                               "documentType": "pan",
                               "document": "ABCDE1234F"
                           })

    assert response.status_code == 400

    result = response.get_json()

    assert result["success"] is False

    assert result["error"] == "Name is required"


def test_missing_document_number():

    client = app.test_client()

    response = client.post("/api/verify",
                           data={
                               "documentType": "pan",
                               "name": "Rahul Kumar"
                           })

    assert response.status_code == 400

    result = response.get_json()

    assert result["success"] is False

    assert result["error"] == "Document number is required"


def test_missing_file():

    client = app.test_client()

    response = client.post("/api/verify",
                           data={
                               "documentType": "pan",
                               "name": "Rahul Kumar",
                               "document": "ABCDE1234F"
                           })

    assert response.status_code == 400

    result = response.get_json()

    assert result["success"] is False

    assert result["error"] == "No file uploaded"


def test_health():

    client = app.test_client()

    response = client.get("/api/health")

    assert response.status_code == 200

    result = response.get_json()

    assert result["success"] is True

    assert result["status"] == "Backend is running"
