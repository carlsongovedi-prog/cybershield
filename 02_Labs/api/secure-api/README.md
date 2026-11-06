# CyberShield Secure API Lab

## 1. Overview

This project is a local Flask API developed as part of CyberShield's secure software development and API security training.

The API accepts numeric input, validates requests, enforces input limits, and returns JSON responses.

## 2. Objectives

- Build a basic REST API using Flask.
- Implement input validation.
- Reject invalid data types.
- Enforce positive and negative numeric boundaries.
- Reject non-finite numeric values.
- Perform automated security testing.

## 3. Technology Stack

- Python 3
- Flask
- Python unittest
- JSON
- curl

## 4. API Endpoints

### GET /health

Checks whether the API is operational.

Example:

`curl http://127.0.0.1:5001/health`

Expected response:

`{"service":"training-api","status":"ok"}`

### POST /double

Accepts a JSON object containing a numeric value and returns twice that value.

Example request:

`{"value":25}`

Expected response:

`{"result":50}`

## 5. Security Controls

The API implements:

1. JSON object validation.
2. Numeric type validation.
3. Boolean rejection.
4. Non-finite number rejection (NaN and infinity).
5. Absolute numeric range enforcement.
6. Consistent JSON error responses.

Allowed range: -1,000,000 to 1,000,000.

## 6. Automated Security Tests

The test suite is located in `test_app.py`.

Run tests:

`python3 -m unittest -v`

### Test results

**10 tests passed.**

Test coverage:

- Health endpoint.
- Valid numeric input.
- Text rejection.
- Boolean rejection.
- Positive boundary acceptance.
- Negative boundary acceptance.
- Positive range violation.
- Negative range violation.
- NaN rejection.
- Infinity rejection.

## 7. Running the Lab

Activate the virtual environment, install Flask if necessary, and start the API:

`python3 app.py`

The API listens locally on:

`http://127.0.0.1:5001`

## 8. Security Limitations

This is an educational local API, not a production-ready service.

It does not currently implement:

- Authentication or authorization.
- Rate limiting.
- HTTPS/TLS.
- Production deployment controls.
- Centralized logging and monitoring.

Only run security tests against systems you own or have explicit permission to assess.

## 9. Project Status

Version: 1.0

Status: Initial implementation and automated validation completed.

Organization: CyberShield Security Solutions
