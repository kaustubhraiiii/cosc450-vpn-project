#!/usr/bin/env python3
"""
SSL/TLS-enabled File Transfer Server
COSC 450 Final Project - Longyu Tang
"""

import socket
import ssl
import threading
import os
import sys

# Ensure original server module can be imported
sys.path.insert(0, os.path.dirname(__file__))

from file_server import FileTransferServer


class FileTransferServerSSL(FileTransferServer):
    """
    File transfer server with SSL/TLS encryption.
    Wraps the server socket with TLS while reusing
    the original protocol logic.
    """

    def __init__(self, host="0.0.0.0", port=9998,
                 storage_dir="./uploads", certfile=None, keyfile=None):
        super().__init__(host=host, port=port, storage_dir=storage_dir)
        self.certfile = certfile
        self.keyfile = keyfile

    def start(self):
        """Start SSL-enabled file transfer server."""
        # Create TCP socket
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Wrap socket with SSL
        if self.certfile and self.keyfile:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(self.certfile, self.keyfile)
            self.server_socket = context.wrap_socket(
                raw_socket, server_side=True
            )
            print("[+] SSL/TLS enabled for file transfer server")
        else:
            self.server_socket = raw_socket
            print("[!] WARNING: running WITHOUT SSL")

        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print(f"[+] Listening on {self.host}:{self.port}")
        print(f"[+] Upload directory: {self.storage_dir}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"[+] SSL connection from {client_address}")

                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()
        except KeyboardInterrupt:
            print("\n[!] Server shutting down...")
        finally:
            self.server_socket.close()


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="SSL/TLS File Transfer Server"
    )
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=9998)
    parser.add_argument("--storage", default="./uploads")
    parser.add_argument("--certfile", required=True)
    parser.add_argument("--keyfile", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    server = FileTransferServerSSL(
        host=args.host,
        port=args.port,
        storage_dir=args.storage,
        certfile=args.certfile,
        keyfile=args.keyfile
    )
    server.start()

