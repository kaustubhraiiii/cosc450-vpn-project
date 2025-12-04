#!/usr/bin/env python3
"""
Network Performance Testing

COSC 450 Final Project - Longyu Tang
"""

import subprocess
import json
import statistics
from datetime import datetime


class NetworkPerformanceTester:
    def __init__(self, target_host):
        self.target_host = target_host
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "target": target_host,
            "tests": {}
        }

    def test_latency(self, count=50):
        """Test latency using ping"""
        print(f"[+] Testing latency to {self.target_host}...")

        cmd = ["ping", "-c", str(count), self.target_host]
        result = subprocess.run(cmd, capture_output=True, text=True)

        latencies = []
        for line in result.stdout.splitlines():
            if "time=" in line:
                try:
                    time_str = line.split("time=")[1].split()[0]
                    latencies.append(float(time_str))
                except:
                    continue

        if latencies:
            self.results["tests"]["latency"] = {
                "min": min(latencies),
                "max": max(latencies),
                "avg": statistics.mean(latencies),
                "stdev": statistics.stdev(latencies) if len(latencies) > 1 else 0,
                "unit": "ms",
                "samples": len(latencies)
            }

            print(f"    Avg latency: {statistics.mean(latencies):.2f} ms")

    def test_throughput(self, duration=10):
        """Test throughput using iperf3"""
        print(f"[+] Testing throughput to {self.target_host}...")

        cmd = ["iperf3", "-c", self.target_host, "-t", str(duration), "-J"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        try:
            data = json.loads(result.stdout)
            bps = data["end"]["sum_sent"]["bits_per_second"]
            mbps = bps / 1_000_000

            self.results["tests"]["throughput"] = {
                "value": mbps,
                "unit": "Mbps",
                "duration": duration
            }

            print(f"    Throughput: {mbps:.2f} Mbps")
        except:
            print("    [!] iperf3 parsing failed")

    def test_packet_loss(self, count=100):
        """Test packet loss using ping"""
        print(f"[+] Testing packet loss to {self.target_host}...")

        cmd = ["ping", "-c", str(count), self.target_host]
        result = subprocess.run(cmd, capture_output=True, text=True)

        for line in result.stdout.splitlines():
            if "packet loss" in line:
                loss = line.split(",")[2].split("%")[0].strip()
                self.results["tests"]["packet_loss"] = {
                    "value": float(loss),
                    "unit": "%"
                }
                print(f"    Packet loss: {loss}%")

    def save_results(self, filename):
        with open(filename, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"[+] Results saved to {filename}")

    def run_all(self):
        print("\n=== Network Performance Test ===\n")
        self.test_latency()
        self.test_throughput()
        self.test_packet_loss()
        print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Network performance test")
    parser.add_argument("--host", required=True, help="Target host")
    parser.add_argument("--output", default="results.json", help="Output file")
    args = parser.parse_args()

    tester = NetworkPerformanceTester(args.host)
    tester.run_all()
    tester.save_results(args.output)

