#!/usr/bin/env python3
"""
Master test runner for COSC 450 VPN project.

This script runs:
  1. Network performance tests (baseline, VPN-only, VPN+full network)
  2. Application-level performance tests (file-transfer)
  3. Result analysis and plot generation

It assumes:
  - iperf3 server is already running (e.g., `iperf3 -s -D`)
  - OpenVPN is connected when running VPN-related tests
  - File-transfer servers are running for application tests
"""

import subprocess
from pathlib import Path


def run(cmd: list[str]) -> None:
    """Run a command and echo it, raising on error."""
    print("\n[+] Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    here = Path(__file__).resolve().parent
    results_dir = here / "results"
    results_dir.mkdir(exist_ok=True)

    print("=== Master Test Runner ===")

    # 1. Network performance tests
    print("\n=== Step 1: Network performance tests ===")
    run(
        [
            "python3",
            str(here / "network_performance.py"),
            "--host",
            "127.0.0.1",
            "--output",
            str(results_dir / "baseline_network.json"),
        ]
    )

    run(
        [
            "python3",
            str(here / "network_performance.py"),
            "--host",
            "10.8.0.1",
            "--output",
            str(results_dir / "vpn_network.json"),
        ]
    )

    run(
        [
            "python3",
            str(here / "network_performance.py"),
            "--host",
            "github.com",
            "--output",
            str(results_dir / "vpn_full_network.json"),
        ]
    )

    # 2. Application performance tests
    print("\n=== Step 2: Application performance tests ===")
    run(
        [
            "python3",
            str(here / "application_performance.py"),
            "--output",
            str(results_dir / "app_performance.json"),
        ]
    )

    # 3. Analyze results (network plots + summary)
    print("\n=== Step 3: Analyzing results & generating plots ===")
    run(
        [
            "python3",
            str(here / "analyze_results.py"),
            "--dir",
            str(results_dir),
        ]
    )

    print("\n[+] All tests completed successfully.")
    print(f"[+] Results directory: {results_dir}")


if __name__ == "__main__":
    main()

