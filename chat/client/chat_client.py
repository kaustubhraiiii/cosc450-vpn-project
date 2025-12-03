#!/usr/bin/env python3
"""
Chat Client
COSC 450 Final Project - Kaustubh Rai
"""

import socket
import threading
import sys


class ChatClient:
    """Chat client with threaded message receiving"""
    
    def __init__(self, server_host, server_port, username):
        self.server_host = server_host
        self.server_port = server_port
        self.username = username
        self.socket = None
        self.running = False
    
    def connect(self):
        """Connect to chat server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            
            # Send username
            self.socket.send(self.username.encode('utf-8'))
            
            print(f"[+] Connected to chat server at {self.server_host}:{self.server_port}")
            print("=" * 70)
            return True
        except Exception as e:
            print(f"[!] Connection failed: {e}")
            return False
    
    def receive_messages(self):
        """Receive and display messages from server"""
        while self.running:
            try:
                message = self.socket.recv(4096).decode('utf-8')
                if message:
                    # Clear current line, print message, reprint prompt
                    print(f"\r{message}", end='')
                    print(f"You: ", end='', flush=True)
                else:
                    break
            except:
                break
        
        print("\n[!] Disconnected from server")
        self.running = False
    
    def send_messages(self):
        """Send messages to server"""
        print("You: ", end='', flush=True)
        
        while self.running:
            try:
                message = input()
                
                if message.lower() == '/quit':
                    print("[!] Exiting chat...")
                    self.running = False
                    break
                
                if message.strip():
                    self.socket.send(message.encode('utf-8'))
                    print("You: ", end='', flush=True)
                    
            except KeyboardInterrupt:
                print("\n[!] Interrupted")
                self.running = False
                break
            except:
                break
    
    def start(self):
        """Start the chat client"""
        if not self.connect():
            return
        
        self.running = True
        
        print("\nChat Commands:")
        print("  /quit - Exit the chat")
        print("=" * 70 + "\n")
        
        # Start receive thread
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        
        # Handle sending in main thread
        try:
            self.send_messages()
        except KeyboardInterrupt:
            print("\n[!] Exiting...")
        finally:
            self.running = False
            if self.socket:
                self.socket.close()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Chat Client for COSC 450 Project'
    )
    parser.add_argument('--host', required=True,
                       help='Server hostname or IP address')
    parser.add_argument('--port', type=int, default=8888,
                       help='Server port (default: 8888)')
    parser.add_argument('--username', required=True,
                       help='Your username')
    
    args = parser.parse_args()
    
    client = ChatClient(args.host, args.port, args.username)
    client.start()
