#!/usr/bin/env python3

"""
Performance Results Analysis and Visualization

COSC 450 Final Project - Longyu Tang
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


class ResultsAnalyzer:
    def __init__(self, results_dir='./results'):
        self.results_dir = Path(results_dir)
        self.data = {}
        self.load_all_results()

    def load_all_results(self):
        """Load all JSON result files"""
        for json_file in self.results_dir.glob('*.json'):
            with open(json_file) as f:
                scenario = json_file.stem
                self.data[scenario] = json.load(f)

    def plot_latency_comparison(self):
        """Create latency comparison bar chart"""
        scenarios = []
        avg_latencies = []

        for scenario, data in self.data.items():
            if 'network' in scenario and 'latency' in data.get('tests', {}):
                scenarios.append(
                    scenario.replace('_network', '').replace('_', ' ').title()
                )
                avg_latencies.append(data['tests']['latency']['avg'])

        if not scenarios:
            print("[!] No latency results found, skipping latency plot.")
            return

        plt.figure(figsize=(10, 6))
        bars = plt.bar(scenarios, avg_latencies)

        plt.xlabel('Configuration', fontsize=12)
        plt.ylabel('Average Latency (ms)', fontsize=12)
        plt.title('VPN Impact on Network Latency', fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f'{height:.2f}ms',
                ha='center',
                va='bottom',
                fontsize=10,
            )

        plt.tight_layout()
        plt.savefig(self.results_dir / 'latency_comparison.png', dpi=300)
        plt.close()
        print("[+] Saved: latency_comparison.png")

    def plot_throughput_comparison(self):
        """Create throughput comparison bar chart"""
        scenarios = []
        throughputs = []

        for scenario, data in self.data.items():
            if 'network' in scenario and 'throughput' in data.get('tests', {}):
                scenarios.append(
                    scenario.replace('_network', '').replace('_', ' ').title()
                )
                throughputs.append(data['tests']['throughput']['value'])

        if not scenarios:
            print("[!] No throughput results found, skipping throughput plot.")
            return

        plt.figure(figsize=(10, 6))
        bars = plt.bar(scenarios, throughputs)

        plt.xlabel('Configuration', fontsize=12)
        plt.ylabel('Throughput (Mbps)', fontsize=12)
        plt.title('VPN Impact on Network Throughput', fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3)

        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f'{height:.1f}',
                ha='center',
                va='bottom',
                fontsize=10,
            )

        plt.tight_layout()
        plt.savefig(self.results_dir / 'throughput_comparison.png', dpi=300)
        plt.close()
        print("[+] Saved: throughput_comparison.png")

    def plot_file_transfer_performance(self):
        """Create file transfer performance chart"""
        plt.figure(figsize=(12, 6))
        has_data = False

        for scenario, data in self.data.items():
            if 'app' in scenario and 'file_transfer' in data.get('tests', {}):
                transfers = data['tests']['file_transfer']
                sizes = [t['file_size_mb'] for t in transfers]
                times = [t['transfer_time_sec'] for t in transfers]
                label = scenario.replace('_app', '').replace('_', ' ').title()
                plt.plot(
                    sizes,
                    times,
                    marker='o',
                    linewidth=2,
                    markersize=8,
                    label=label,
                )
                has_data = True

        if not has_data:
            print("[!] No app/file_transfer data found, skipping file transfer plot.")
            plt.close()
            return

        plt.xlabel('File Size (MB)', fontsize=12)
        plt.ylabel('Transfer Time (seconds)', fontsize=12)
        plt.title(
            'File Transfer Performance Across Configurations',
            fontsize=14,
            fontweight='bold',
        )
        plt.legend(fontsize=10)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.results_dir / 'file_transfer_performance.png', dpi=300)
        plt.close()
        print("[+] Saved: file_transfer_performance.png")

    def plot_overhead_analysis(self):
        """Calculate and plot VPN overhead"""
        baseline_throughput = None
        vpn_throughput = None

        for scenario, data in self.data.items():
            tests = data.get('tests', {})
            if 'baseline' in scenario and 'throughput' in tests:
                baseline_throughput = tests['throughput']['value']
            elif 'vpn_full' in scenario and 'throughput' in tests:
                vpn_throughput = tests['throughput']['value']

        if not (baseline_throughput and vpn_throughput):
            print("[!] Missing baseline/vpn_full throughput, skipping overhead plot.")
            return

        overhead = ((baseline_throughput - vpn_throughput) / baseline_throughput) * 100

        fig, ax = plt.subplots(figsize=(8, 6))
        categories = ['Baseline', 'VPN Overhead', 'VPN Throughput']
        values = [
            baseline_throughput,
            baseline_throughput - vpn_throughput,
            vpn_throughput,
        ]

        bars = ax.bar(categories, values)
        ax.set_ylabel('Throughput (Mbps)', fontsize=12)
        ax.set_title(
            f'VPN Overhead Analysis\n({overhead:.1f}% reduction)',
            fontsize=14,
            fontweight='bold',
        )
        ax.grid(axis='y', alpha=0.3)

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f'{height:.1f}',
                ha='center',
                va='bottom',
                fontsize=10,
            )

        plt.tight_layout()
        plt.savefig(self.results_dir / 'vpn_overhead.png', dpi=300)
        plt.close()
        print("[+] Saved: vpn_overhead.png")

    def generate_summary_report(self):
        """Generate text summary of results"""
        report_file = self.results_dir / 'performance_summary.txt'

        with open(report_file, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("COSC 450 Final Project - Performance Test Summary\n")
            f.write("=" * 70 + "\n\n")

            for scenario, data in sorted(self.data.items()):
                f.write(f"\n{scenario.upper()}\n")
                f.write("-" * 70 + "\n")

                tests = data.get('tests', {})

                if 'latency' in tests:
                    lat = tests['latency']
                    f.write("Latency:\n")
                    f.write(f"  Average: {lat['avg']:.2f} ms\n")
                    f.write(f"  Min: {lat['min']:.2f} ms\n")
                    f.write(f"  Max: {lat['max']:.2f} ms\n")
                    f.write(f"  Std Dev: {lat['stdev']:.2f} ms\n\n")

                if 'throughput' in tests:
                    tp = tests['throughput']
                    f.write(
                        f"Throughput: {tp['value']:.2f} {tp['unit']}\n\n"
                    )

                if 'packet_loss' in tests:
                    pl = tests['packet_loss']
                    f.write(f"Packet Loss: {pl['value']:.2f}%\n\n")

                if 'file_transfer' in tests:
                    f.write("File Transfer Results:\n")
                    for transfer in tests['file_transfer']:
                        f.write(f"  {transfer['file_size_mb']}MB: ")
                        f.write(f"{transfer['transfer_time_sec']:.2f}s ")
                        f.write(
                            f"({transfer['throughput_mbps']:.2f} Mbps)\n"
                        )

            f.write("\n" + "=" * 70 + "\n")

        print(f"[+] Summary report saved: {report_file}")

    def generate_all_visualizations(self):
        """Generate all charts and reports"""
        print("\n=== Generating Performance Visualizations ===\n")
        self.plot_latency_comparison()
        self.plot_throughput_comparison()
        self.plot_file_transfer_performance()
        self.plot_overhead_analysis()
        self.generate_summary_report()
        print("\n[+] All visualizations complete!")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Analyze Performance Results')
    parser.add_argument('--dir', default='./results', help='Results directory')

    args = parser.parse_args()

    analyzer = ResultsAnalyzer(args.dir)
    analyzer.generate_all_visualizations()

