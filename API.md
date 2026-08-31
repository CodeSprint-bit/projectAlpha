# Document Verification Backend API

## 1. Backend Setup

### Requirements

* Python 3
* Virtual environment
* Tesseract OCR
* Required Python packages

### Start the backend

From the project root:

```bash
source .venv/bin/activate  # Linux
.\venv\Scripts\activate    # Windows
python app.py
```

The backend will run at:

```text
http://127.0.0.1:5000
```

---

# 2. API Endpoints

| Method | Endpoint      | Purpose                          |
| ------ | ------------- | -------------------------------- |
| GET    | `/api/health` | Check whether backend is running |
| POST   | `/api/verify` | Verify an uploaded document      |

---

# 3. Health Check

### Request

```text
GET /api/health
```

Example:

```text
http://127.0.0.1:5000/api/health
```

### Response

```json
{
    "success": true,
    "status": "Backend is running"
}
```

---

# 4. Document Verification

### Request

```text
POST /api/verify
```

The request must use:

```text
multipart/form-data
```

This is required because the request contains both text fields and an uploaded document.

---

## Required Fields

| Field          | Type   | Required | Description                         |
| -------------- | ------ | -------- | ----------------------------------- |
| `documentType` | string | Yes      | `pan`, `aadhaar`, or `visa`         |
| `name`         | string | Yes      | Name entered by the user            |
| `document`     | string | Yes      | Document number entered by the user |
| `documentFile` | file   | Yes      | JPG, JPEG, or PNG document          |

---

# 5. Example Request

For a PAN document:

```text
documentType = pan
name = Rahul Kumar
document = ABCDE1234F
documentFile = pan.jpg
```

For Aadhaar:

```text
documentType = aadhaar
name = Rahul Kumar
document = 123456789012
documentFile = aadhaar.jpg
```

For VISA:

```text
documentType = visa
name = Rahul Kumar
document = YOUR_VISA_NUMBER
documentFile = visa.jpg
```

---

# 6. Example Frontend Request

JavaScript can send the document to the backend like this:

```javascript
const formData = new FormData();

formData.append("documentType", "pan");
formData.append("name", "Rahul Kumar");
formData.append("document", "ABCDE1234F");
formData.append("documentFile", fileInput.files[0]);

const response = await fetch(
    "http://127.0.0.1:5000/api/verify",
    {
        method: "POST",
        body: formData
    }
);

const result = await response.json();

console.log(result);
```

**Do not manually set `Content-Type`.**

The browser automatically creates the correct `multipart/form-data` boundary when using `FormData`.

---

# 7. Successful Response

Example:

```json
{
    "success": true,

    "document": {
        "type": "pan",
        "entered_number": "ABCDE1234F",
        "detected_number": "ABCDE1234F",
        "number_match": true,
        "format_valid": true
    },

    "identity": {
        "name_similarity": 96
    },

    "risk": {
        "score": 0,
        "level": "Low Risk"
    }
}
```

---

# 8. Understanding the Response

## `success`

```json
"success": true
```

Means the backend successfully processed the request.

---

## `document`

Contains document-related verification results.

### `type`

```json
"type": "pan"
```

The document type selected by the user.

Possible values:

```text
pan
aadhaar
visa
```

### `entered_number`

The document number entered by the user.

### `detected_number`

The document number detected from the uploaded document using OCR.

### `number_match`

```json
"number_match": true
```

Means the entered number matches the number detected from the document.

### `format_valid`

Indicates whether the detected document number follows the expected format.

---

# 9. Identity Verification

```json
"identity": {
    "name_similarity": 96
}
```

`name_similarity` represents the similarity between the entered name and the name found in the OCR text.

Higher similarity generally means the names are more similar.

---

# 10. Risk Result

```json
"risk": {
    "score": 0,
    "level": "Low Risk"
}
```

### Risk score

The backend calculates a numerical risk score based on verification failures.

### Risk levels

```text
Low Risk
Medium Risk
High Risk
```

The frontend should use `risk.level` to decide what result to display to the user.

Example:

```javascript
if (result.risk.level === "High Risk") {
    // Show warning
}
```

---

# 11. Common Errors

## Invalid document type

Request:

```text
documentType = passport
```

Response:

```json
{
    "success": false,
    "error": "Invalid document type"
}
```

HTTP status:

```text
400
```

---

## Missing name

Response:

```json
{
    "success": false,
    "error": "Name is required"
}
```

HTTP status:

```text
400
```

---

## Missing document number

Response:

```json
{
    "success": false,
    "error": "Document number is required"
}
```

HTTP status:

```text
400
```

---

## No uploaded file

Response:

```json
{
    "success": false,
    "error": "No file uploaded"
}
```

HTTP status:

```text
400
```

---

## Invalid file type

Currently supported:

```text
.jpg
.jpeg
.png
```

PDF is currently not supported by the OCR pipeline.

---

## File too large

Maximum upload size:

```text
5 MB
```

If the uploaded file exceeds this limit, the backend returns HTTP:

```text
413
```

---

# 12. Supported Documents

Currently supported:

* PAN
* Aadhaar
* VISA

Supported image formats:

* JPG
* JPEG
* PNG

Maximum file size:

```text
5 MB
```

---

# 13. Backend Processing Flow

The backend processes a document approximately like this:

```text
Frontend
    |
    | POST /api/verify
    |
    v
Flask API
    |
    v
Input Validation
    |
    v
File Validation
    |
    v
OCR
    |
    v
Document Number Extraction
    |
    v
Document Number Comparison
    |
    v
Name Similarity
    |
    v
Risk Calculation
    |
    v
JSON Response
    |
    v
Frontend
```

---

# 14. Important Note for Frontend Developers

The frontend should call:

```text
POST /api/verify
```

and use the JSON response.

For example:

```javascript
result.document.number_match
```

gets the document-number match result.

```javascript
result.identity.name_similarity
```

gets the name similarity.

```javascript
result.risk.score
```

gets the risk score.

```javascript
result.risk.level
```

gets the risk level.

---

# 15. Local Development

Backend:

```text
http://127.0.0.1:5000
```

API:

```text
http://127.0.0.1:5000/api/verify
```

Health check:

```text
http://127.0.0.1:5000/api/health
```

When the frontend and backend are running on different machines, the frontend should use the backend machine's network address instead of `127.0.0.1`.
