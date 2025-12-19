#!/usr/bin/env python3
"""
Application-level performance test for the file transfer application.

This script measures end-to-end transfer time for a 5 MB test file
under four scenarios:

A. Baseline   (no VPN,  no SSL)  -> 127.0.0.1:9997
B. VPN only   (VPN,    no SSL)   -> 10.8.0.1:9997
C. SSL only   (no VPN,  SSL)     -> 127.0.0.1:9999
D. VPN + SSL  (VPN,     SSL)     -> 10.8.0.1:9999

The script assumes that the corresponding file-transfer servers are
already running in another terminal.

Results are written to a JSON file for later analysis.
"""

import argparse
import json
import os
import subprocess
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FILE_TRANSFER_DIR = PROJECT_ROOT / "file-transfer"
TEST_FILE = FILE_TRANSFER_DIR / "test_app.bin"


def ensure_test_file(size_mb: int = 5) -> None:
    """Ensure the 5 MB test file exists in the file-transfer directory."""
    if TEST_FILE.exists():
        return

    print(f"[+] Creating {size_mb} MB test file at {TEST_FILE} ...")
    FILE_TRANSFER_DIR.mkdir(parents=True, exist_ok=True)

    # Use dd to generate random data, similar to the lab instructions.
    cmd = [
        "dd",
        "if=/dev/urandom",
        f"of={TEST_FILE}",
        "bs=1M",
        f"count={size_mb}",
    ]
    # Suppress dd's stderr to keep output clean
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("[+] Test file created.")


def run_scenario(name: str, cmd: list[str]) -> dict:
    """Run a single scenario and return a result dict."""
    print(f"\n=== Running scenario {name} ===")
    print("[+] Command:", " ".join(cmd))

    start = time.perf_counter()
    completed = subprocess.run(cmd)
    elapsed = time.perf_counter() - start

    success = completed.returncode == 0

    print(f"[+] Scenario {name} finished with return code {completed.returncode}")
    print(f"[+] Elapsed time: {elapsed:.3f} s")
    print(f"[+] Success: {success}")

    return {
        "name": name,
        "command": cmd,
        "elapsed_seconds": elapsed,
        "return_code": completed.returncode,
        "success": success,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Application-level performance tests for the file-transfer app."
    )
    parser.add_argument(
        "--output",
        default="results/app_performance.json",
        help="Path to output JSON file (default: results/app_performance.json)",
    )
    args = parser.parse_args()

    ensure_test_file(size_mb=5)

    scenarios = [
        {
            "name": "A_baseline_no_vpn_no_ssl",
            "cmd": [
                "python3",
                str(FILE_TRANSFER_DIR / "client" / "file_client.py"),
                "--host",
                "127.0.0.1",
                "--port",
                "9997",
                "--file",
                str(TEST_FILE),
            ],
        },
        {
            "name": "B_vpn_only",
            "cmd": [
                "python3",
                str(FILE_TRANSFER_DIR / "client" / "file_client.py"),
                "--host",
                "10.8.0.1",
                "--port",
                "9997",
                "--file",
                str(TEST_FILE),
            ],
        },
        {
            "name": "C_ssl_only",
            "cmd": [
                "python3",
                str(FILE_TRANSFER_DIR / "client" / "file_client_ssl.py"),
                "--host",
                "127.0.0.1",
                "--port",
                "9999",
                "--file",
                str(TEST_FILE),
            ],
        },
        {
            "name": "D_vpn_plus_ssl",
            "cmd": [
                "python3",
                str(FILE_TRANSFER_DIR / "client" / "file_client_ssl.py"),
                "--host",
                "10.8.0.1",
                "--port",
                "9999",
                "--file",
                str(TEST_FILE),
            ],
        },
    ]

    results: list[dict] = []

    print("=== Application Performance Test ===")
    print(f"[+] Using test file: {TEST_FILE}")

    for scenario in scenarios:
        result = run_scenario(scenario["name"], scenario["cmd"])
        results.append(result)

    # Build output structure
    output_data = {
        "test_file": str(TEST_FILE),
        "file_size_bytes": TEST_FILE.stat().st_size,
        "scenarios": results,
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"\n[+] Application performance results saved to {output_path}")


if __name__ == "__main__":
    main()

