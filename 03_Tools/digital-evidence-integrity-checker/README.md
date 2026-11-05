# CyberShield Digital Evidence Integrity Checker

## 1. Project Overview

A Python command-line tool that verifies the integrity of digital evidence using the SHA-256 cryptographic hash algorithm.

The tool calculates a file's SHA-256 hash, compares it against a trusted reference checksum, and generates a timestamped verification report.

## 2. Objectives

- Calculate SHA-256 file hashes.
- Compare evidence files against trusted reference checksums.
- Detect unexpected file modifications.
- Generate timestamped verification reports.
- Preserve separate PASS and FAIL reports.
- Return meaningful process exit codes.
- Validate inputs and checksum formats.

## 3. Technologies

- Python 3
- hashlib
- pathlib
- datetime
- subprocess
- unittest
- SHA-256

## 4. Project Structure

```text
digital-evidence-integrity-checker/
├── integrity_check.py
├── test_integrity_check.py
├── README.md
├── invoice.txt
├── invoice.sha256
└── evidence/
    ├── invoice_original.txt
    ├── invoice_original.sha256
    ├── invoice_test.txt
    └── verification_report_*.txt
```

## 5. Usage

Run:

```bash
python3 integrity_check.py FILE CHECKSUM_FILE
```

Example:

```bash
python3 integrity_check.py \
evidence/invoice_original.txt \
evidence/invoice_original.sha256
```

The tool generates a timestamped report in the `evidence/` directory.

## 6. Exit Codes

- `0`: Integrity verification passed.
- `1`: Integrity verification failed.
- `2`: Invalid input, missing file, or usage error.

## 7. Automated Testing

Run:

```bash
python3 -m unittest -v test_integrity_check.py
```

Current test coverage:

- Original evidence passes verification.
- Modified evidence fails verification.
- Missing evidence is rejected.
- Missing command-line arguments are rejected.
- Invalid checksums are rejected.
- Separate PASS and FAIL reports are preserved.

**Latest test result: 6 tests passed.**

## 8. Security Considerations

- Preserve original evidence.
- Work on separate copies where possible.
- Protect reference checksums.
- Record collection and verification details.
- Maintain chain-of-custody documentation.
- Use trusted methods to store and protect verification reports.

A matching hash confirms that the file matches the supplied checksum. It does not establish the authenticity of the evidence or prove that it was not modified before the checksum was created.

## 9. Limitations

This is an educational prototype, not a certified forensic acquisition or evidence-management system.

The integrity of the verification depends on the trustworthiness of the reference checksum and the environment in which verification is performed.

## 10. Project Status

Version 1.0 — Initial educational implementation.

Automated test suite: 6 passing tests.
