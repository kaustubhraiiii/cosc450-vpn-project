#!/usr/bin/env python3
"""
SSL/TLS-enabled File Transfer Client
COSC 450 Final Project - Longyu Tang
"""

import socket
import ssl
import os
import sys

# Ensure original client module can be imported
sys.path.insert(0, os.path.dirname(__file__))

from file_client import FileTransferClient


class FileTransferClientSSL(FileTransferClient):
    """
    File transfer client with SSL/TLS encryption.
    """

    def connect(self):
        """Connect to the file transfer server using SSL/TLS."""
        try:
            # Create TCP socket
            raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Create SSL context
            context = ssl.create_default_context()
            # For this project, we do not verify the certificate
            # (in real world, you MUST verify certificates)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            # Wrap socket with SSL
            self.socket = context.wrap_socket(
                raw_socket,
                server_hostname=self.server_host
            )

            # Connect to server
            self.socket.connect((self.server_host, self.server_port))
            print(f"[+] Connected securely to {self.server_host}:{self.server_port}")
            return True
        except Exception as e:
            print(f"[!] SSL connection failed: {e}")
            return False


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="SSL/TLS File Transfer Client"
    )
    parser.add_argument("--host", required=True, help="Server host")
    parser.add_argument("--port", type=int, default=9998, help="Server port")
    parser.add_argument("--file", required=True, help="File to send")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    client = FileTransferClientSSL(args.host, args.port)

    if client.connect():
        client.send_file(args.file)
        client.disconnect()

