#!/usr/bin/env python3
"""
Multi-Client Chat Server
COSC 450 Final Project - Kaustubh Rai
"""

import socket
import threading
import json
from datetime import datetime


class ChatServer:
    """Multi-threaded chat server with client management"""
    
    def __init__(self, host='0.0.0.0', port=8888):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}  # {socket: username}
        self.clients_lock = threading.Lock()
    
    def start(self):
        """Start the chat server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        
        print("=" * 70)
        print("Multi-Client Chat Server Started")
        print("=" * 70)
        print(f"Host: {self.host}")
        print(f"Port: {self.port}")
        print("=" * 70)
        print("Waiting for connections...\n")
        
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                
                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n\n[!] Shutting down server...")
        finally:
            self.shutdown()
    
    def handle_client(self, client_socket, client_address):
        """Handle a client connection"""
        username = None
        
        try:
            # Receive username
            username = client_socket.recv(1024).decode('utf-8').strip()
            
            if not username:
                client_socket.close()
                return
            
            # Add client to active clients
            with self.clients_lock:
                self.clients[client_socket] = username
            
            print(f"[+] User '{username}' joined from {client_address[0]}:{client_address[1]}")
            
            # Broadcast join message
            join_msg = f"*** {username} has joined the chat ***"
            self.broadcast(join_msg, client_socket)
            
            # Send welcome message
            welcome_msg = f"Welcome to the chat, {username}!\n"
            welcome_msg += f"Users online: {len(self.clients)}\n"
            client_socket.send(welcome_msg.encode('utf-8'))
            
            # Handle messages from this client
            while True:
                message = client_socket.recv(4096).decode('utf-8')
                
                if not message:
                    break
                
                # Format and broadcast message
                timestamp = datetime.now().strftime("%H:%M:%S")
                formatted_msg = f"[{timestamp}] {username}: {message}"
                print(formatted_msg)
                
                self.broadcast(formatted_msg, client_socket)
            
        except Exception as e:
            print(f"[!] Error handling client {client_address}: {e}")
        
        finally:
            # Remove client and broadcast leave message
            with self.clients_lock:
                if client_socket in self.clients:
                    username = self.clients[client_socket]
                    del self.clients[client_socket]
            
            if username:
                leave_msg = f"*** {username} has left the chat ***"
                print(leave_msg)
                self.broadcast(leave_msg, client_socket)
            
            client_socket.close()
    
    def broadcast(self, message, sender_socket=None):
        """Broadcast message to all connected clients except sender"""
        message_bytes = (message + '\n').encode('utf-8')
        
        with self.clients_lock:
            for client_socket in list(self.clients.keys()):
                if client_socket != sender_socket:
                    try:
                        client_socket.send(message_bytes)
                    except:
                        # Remove dead client
                        if client_socket in self.clients:
                            username = self.clients[client_socket]
                            del self.clients[client_socket]
                            print(f"[-] Removed dead connection: {username}")
    
    def shutdown(self):
        """Shutdown server and close all connections"""
        with self.clients_lock:
            for client_socket in self.clients.keys():
                try:
                    client_socket.close()
                except:
                    pass
        
        if self.server_socket:
            self.server_socket.close()
        
        print("[+] Server shutdown complete")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Multi-Client Chat Server for COSC 450 Project'
    )
    parser.add_argument('--host', default='0.0.0.0',
                       help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8888,
                       help='Port to bind to (default: 8888)')
    
    args = parser.parse_args()
    
    server = ChatServer(args.host, args.port)
    server.start()
