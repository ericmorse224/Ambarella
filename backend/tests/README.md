# 🧪 AI Meeting Summarizer – Test Suite

This folder contains all unit and integration tests for the backend, including Flask routes, service logic, and utilities.

---

## 📁 Structure Overview

```
tests/
├── test_routes/              # Flask endpoint tests
├── test_services/            # Business logic tests (mocked)
├── test_utils/               # Stateless utility function tests
├── test_services.zip         # 🔐 Real API key-dependent tests (e.g. Google Cloud)
├── mocks.py                  # Reusable mock return values
├── conftest.py               # Shared fixtures
├── README.md                 # 📘 You're here
```

---

## ✅ Mocked Test Suite (Default)

To run the full mocked test suite:

```bash
cd backend
pytest
```

This runs all tests **without any real API calls or secrets**.

---

## 🔐 Real API Testing (Advanced)

For developers who want to validate real third-party integrations like Google Cloud:

### Step 1: Extract the secure tests

```bash
unzip tests/test_services.zip -d tests/test_services_real/
```

### Step 2: Set your environment variables:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/path/to/google-key.json
```

Or use a `.env` loader if preferred.

### Step 3: Run just those tests:

```bash
pytest tests/test_services_real/
```

> ⚠️ Be sure to **exclude these from CI** or any public repo if they contain sensitive tests.

---

## 📌 Notes
- All tests in `test_services/` and `test_utils/` are self-contained and safe for CI
- Tests in `test_services_real/` require credentials and should be opt-in only