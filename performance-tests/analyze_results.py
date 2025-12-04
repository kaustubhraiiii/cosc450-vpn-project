#!/usr/bin/env python3
"""
Performance Results Analysis and Visualization

COSC 450 Final Project - Longyu Tang
"""

import json
import matplotlib.pyplot as plt
from pathlib import Path


class ResultsAnalyzer:
    def __init__(self, results_dir="./results"):
        self.results_dir = Path(results_dir)
        self.data = {}
        self.load_all_results()

    def load_all_results(self):
        """Load all JSON result files"""
        for json_file in self.results_dir.glob("*.json"):
            with open(json_file) as f:
                scenario = json_file.stem
                self.data[scenario] = json.load(f)

    def plot_latency_comparison(self):
        scenarios = []
        avg_latencies = []

        for scenario, data in self.data.items():
            tests = data.get("tests", {})
            if "latency" in tests:
                label = scenario.replace("_network", "").replace("_", " ").title()
                scenarios.append(label)
                avg_latencies.append(tests["latency"]["avg"])

        if not scenarios:
            print("[!] No latency data found")
            return

        plt.figure(figsize=(8, 5))
        bars = plt.bar(scenarios, avg_latencies)
        plt.xlabel("Configuration")
        plt.ylabel("Average Latency (ms)")
        plt.title("Network Latency Comparison")
        plt.grid(axis="y", alpha=0.3)

        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.2f}",
                ha="center",
                va="bottom",
            )

        out = self.results_dir / "latency_comparison.png"
        plt.tight_layout()
        plt.savefig(out, dpi=300)
        plt.close()
        print(f"[+] Saved: {out.name}")

    def plot_throughput_comparison(self):
        scenarios = []
        throughputs = []

        for scenario, data in self.data.items():
            tests = data.get("tests", {})
            if "throughput" in tests:
                label = scenario.replace("_network", "").replace("_", " ").title()
                scenarios.append(label)
                throughputs.append(tests["throughput"]["value"])

        if not scenarios:
            print("[!] No throughput data found")
            return

        plt.figure(figsize=(8, 5))
        bars = plt.bar(scenarios, throughputs)
        plt.xlabel("Configuration")
        plt.ylabel("Throughput (Mbps)")
        plt.title("Network Throughput Comparison")
        plt.grid(axis="y", alpha=0.3)

        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.1f}",
                ha="center",
                va="bottom",
            )

        out = self.results_dir / "throughput_comparison.png"
        plt.tight_layout()
        plt.savefig(out, dpi=300)
        plt.close()
        print(f"[+] Saved: {out.name}")

    def generate_summary(self):
        report = self.results_dir / "performance_summary.txt"
        with open(report, "w") as f:
            f.write("COSC 450 Performance Test Summary\n")
            f.write("=" * 50 + "\n\n")
            for scenario, data in self.data.items():
                f.write(f"{scenario.upper()}\n")
                f.write("-" * 50 + "\n")
                tests = data.get("tests", {})
                if "latency" in tests:
                    f.write(f"Latency avg: {tests['latency']['avg']:.2f} ms\n")
                if "throughput" in tests:
                    f.write(
                        f"Throughput: {tests['throughput']['value']:.2f} {tests['throughput']['unit']}\n"
                    )
                if "packet_loss" in tests:
                    f.write(f"Packet loss: {tests['packet_loss']['value']}%\n")
                f.write("\n")

        print(f"[+] Saved: {report.name}")

    def run_all(self):
        self.plot_latency_comparison()
        self.plot_throughput_comparison()
        self.generate_summary()
        print("[+] Analysis complete")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="./results")
    args = parser.parse_args()

    analyzer = ResultsAnalyzer(args.dir)
    analyzer.run_all()


