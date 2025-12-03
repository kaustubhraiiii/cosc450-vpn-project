#!/usr/bin/env python3
"""
File Transfer Server
COSC 450 Final Project - Longyu Tang
"""

import socket
import threading
import os
import sys
from datetime import datetime

# Add shared module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shared.protocol import FileTransferProtocol, MSG_FILE_HEADER, MSG_FILE_CHUNK, MSG_FILE_COMPLETE


class FileTransferServer:
    def __init__(self, host='0.0.0.0', port=9999, storage_dir='./uploads'):
        self.host = host
        self.port = port
        self.storage_dir = storage_dir
        self.server_socket = None
        self.active_transfers = {}

        # Create storage directory
        os.makedirs(self.storage_dir, exist_ok=True)

    def start(self):
        """Start the file transfer server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print(f"[+] File Transfer Server started on {self.host}:{self.port}")
        print(f"[+] Storage directory: {self.storage_dir}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"[+] New connection from {client_address}")

                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("\n[!] Server shutting down...")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket, client_address):
        """Handle a client connection"""
        print(f"[+] Handling client {client_address}")

        try:
            file_data = b''
            file_name = None
            file_size = 0
            chunks_received = 0

            while True:
                msg_type, metadata, payload = FileTransferProtocol.receive_message(client_socket)

                if msg_type is None:
                    break

                if msg_type == MSG_FILE_HEADER:
                    # File transfer starting
                    file_name = metadata.get('filename')
                    file_size = metadata.get('filesize')
                    checksum = metadata.get('checksum')

                    print(f"[+] Receiving file: {file_name} ({file_size} bytes)")
                    print(f"[+] Expected checksum: {checksum}")

                    file_data = b''
                    chunks_received = 0

                elif msg_type == MSG_FILE_CHUNK:
                    # Receiving file chunk
                    file_data += payload
                    chunks_received += 1

                    progress = len(file_data) / file_size * 100
                    print(f"[+] Progress: {progress:.1f}% ({len(file_data)}/{file_size} bytes)")

                elif msg_type == MSG_FILE_COMPLETE:
                    # File transfer complete
                    print(f"[+] Transfer complete. Received {len(file_data)} bytes in {chunks_received} chunks")

                    # Verify checksum
                    received_checksum = FileTransferProtocol.calculate_checksum(file_data)
                    expected_checksum = metadata.get('checksum')

                    if received_checksum == expected_checksum:
                        # Save file
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        safe_filename = f"{timestamp}_{file_name}"
                        file_path = os.path.join(self.storage_dir, safe_filename)

                        with open(file_path, 'wb') as f:
                            f.write(file_data)

                        print(f"[+] File saved successfully: {file_path}")
                        print(f"[+] Checksum verified: {received_checksum}")

                        # Send success response
                        response = b'SUCCESS'
                        FileTransferProtocol.send_message(
                            client_socket, MSG_FILE_COMPLETE, response,
                            {'saved_as': safe_filename}
                        )
                    else:
                        print(f"[!] Checksum mismatch!")
                        print(f"[!] Expected: {expected_checksum}")
                        print(f"[!] Received: {received_checksum}")

                        response = b'ERROR: Checksum mismatch'
                        FileTransferProtocol.send_message(
                            client_socket, MSG_FILE_COMPLETE, response
                        )

                    break

        except Exception as e:
            print(f"[!] Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
            print(f"[-] Connection closed: {client_address}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='File Transfer Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=9999, help='Port to bind to')
    parser.add_argument('--storage', default='./uploads', help='Storage directory')

    args = parser.parse_args()

    server = FileTransferServer(args.host, args.port, args.storage)
    server.start()
