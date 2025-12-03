"""
File Transfer Protocol - Shared Utilities
COSC 450 Final Project
"""

import struct
import hashlib
import json

# Protocol constants
BUFFER_SIZE = 4096
HEADER_SIZE = 1024

# Message types
MSG_FILE_HEADER = 1
MSG_FILE_CHUNK = 2
MSG_FILE_COMPLETE = 3
MSG_AUTH_REQUEST = 4
MSG_AUTH_RESPONSE = 5
MSG_ERROR = 6


class FileTransferProtocol:
    @staticmethod
    def create_header(msg_type, payload_size, metadata=None):
        """Create protocol header"""
        header = {
            'msg_type': msg_type,
            'payload_size': payload_size,
            'metadata': metadata or {}
        }
        header_json = json.dumps(header).encode('utf-8')
        header_padded = header_json.ljust(HEADER_SIZE, b'\x00')
        return header_padded

    @staticmethod
    def parse_header(header_bytes):
        """Parse protocol header"""
        header_json = header_bytes.rstrip(b'\x00')
        return json.loads(header_json.decode('utf-8'))

    @staticmethod
    def calculate_checksum(data):
        """Calculate SHA256 checksum"""
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def send_message(sock, msg_type, data, metadata=None):
        """Send a protocol message"""
        header = FileTransferProtocol.create_header(
            msg_type, len(data), metadata
        )
        sock.sendall(header + data)

    @staticmethod
    def receive_message(sock):
        """Receive a protocol message"""
        # Receive header
        header_bytes = sock.recv(HEADER_SIZE)
        if not header_bytes:
            return None, None, None

        header = FileTransferProtocol.parse_header(header_bytes)

        # Receive payload
        payload = b''
        remaining = header['payload_size']
        while remaining > 0:
            chunk = sock.recv(min(BUFFER_SIZE, remaining))
            if not chunk:
                break
            payload += chunk
            remaining -= len(chunk)

        return header['msg_type'], header.get('metadata'), payload
