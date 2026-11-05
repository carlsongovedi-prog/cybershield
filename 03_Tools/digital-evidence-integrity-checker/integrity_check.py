import hashlib
import sys
from pathlib import Path
from datetime import datetime, timezone


def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def main():

    if len(sys.argv) != 3:
        print("Usage: python3 integrity_check.py FILE CHECKSUM_FILE")
        return 2

    file_path = Path(sys.argv[1])
    checksum_path = Path(sys.argv[2])

    if not file_path.is_file():
        print("Error: Evidence file not found.")
        return 2

    if not checksum_path.is_file():
        print("Error: Checksum file not found.")
        return 2

    checksum_parts = checksum_path.read_text().split()

    if not checksum_parts:
        print("Error: Checksum file is empty.")
        return 2

    expected_hash = checksum_parts[0].lower()

    if len(expected_hash) != 64 or any(
        char not in "0123456789abcdef" for char in expected_hash
    ):
        print("Error: Invalid SHA-256 checksum.")
        return 2

    actual_hash = calculate_sha256(file_path)

    verified_at = datetime.now(timezone.utc).isoformat()

    if actual_hash == expected_hash:
        result = "PASS"
        exit_code = 0
    else:
        result = "FAIL"
        exit_code = 1

    report = (
        f"Verified at (UTC): {verified_at}\n"
        f"Evidence: {file_path}\n"
        f"Expected: {expected_hash}\n"
        f"Calculated: {actual_hash}\n"
        f"INTEGRITY CHECK: {result}\n"
    )

    report_directory = Path("evidence")
    report_directory.mkdir(exist_ok=True)

    report_timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")

    report_path = report_directory / f"verification_report_{report_timestamp}.txt"

    report_path.write_text(report)

    print(report)
    print("Report saved to:", report_path)

    return exit_code


if __name__ == "__main__":  
    sys.exit(main())
