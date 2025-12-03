#!/usr/bin/env python3
"""
File Transfer Client
COSC 450 Final Project - Longyu Tang
"""

import socket
import os
import sys
from tqdm import tqdm

# Add shared module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shared.protocol import (
    FileTransferProtocol, BUFFER_SIZE,
    MSG_FILE_HEADER, MSG_FILE_CHUNK, MSG_FILE_COMPLETE
)


class FileTransferClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None

    def connect(self):
        """Connect to the file transfer server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            print(f"[+] Connected to {self.server_host}:{self.server_port}")
            return True
        except Exception as e:
            print(f"[!] Connection failed: {e}")
            return False

    def send_file(self, file_path):
        """Send a file to the server"""
        if not os.path.exists(file_path):
            print(f"[!] File not found: {file_path}")
            return False

        try:
            # Get file info
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)

            print(f"[+] Preparing to send: {file_name} ({file_size} bytes)")

            # Read file and calculate checksum
            with open(file_path, 'rb') as f:
                file_data = f.read()

            checksum = FileTransferProtocol.calculate_checksum(file_data)
            print(f"[+] Checksum: {checksum}")

            # Send file header
            metadata = {
                'filename': file_name,
                'filesize': file_size,
                'checksum': checksum
            }
            FileTransferProtocol.send_message(
                self.socket, MSG_FILE_HEADER, b'', metadata
            )

            # Send file in chunks with progress bar
            chunks_sent = 0
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=file_name) as pbar:
                for i in range(0, len(file_data), BUFFER_SIZE):
                    chunk = file_data[i:i + BUFFER_SIZE]
                    FileTransferProtocol.send_message(
                        self.socket, MSG_FILE_CHUNK, chunk
                    )
                    chunks_sent += 1
                    pbar.update(len(chunk))

            print(f"[+] Sent {chunks_sent} chunks")

            # Send completion message
            FileTransferProtocol.send_message(
                self.socket, MSG_FILE_COMPLETE, b'',
                {'checksum': checksum}
            )

            # Receive server response
            msg_type, metadata, payload = FileTransferProtocol.receive_message(self.socket)

            if payload == b'SUCCESS':
                print(f"[+] File transferred successfully!")
                print(f"[+] Saved as: {metadata.get('saved_as')}")
                return True
            else:
                print(f"[!] Transfer failed: {payload.decode()}")
                return False

        except Exception as e:
            print(f"[!] Error sending file: {e}")
            return False

    def disconnect(self):
        """Disconnect from server"""
        if self.socket:
            self.socket.close()
            print("[+] Disconnected")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='File Transfer Client')
    parser.add_argument('--host', required=True, help='Server host')
    parser.add_argument('--port', type=int, default=9999, help='Server port')
    parser.add_argument('--file', required=True, help='File to transfer')

    args = parser.parse_args()

    client = FileTransferClient(args.host, args.port)

    if client.connect():
        client.send_file(args.file)
        client.disconnect()
