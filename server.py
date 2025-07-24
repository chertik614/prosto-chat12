import os
import socket
import threading
from config import PORT

clients = []

def broadcast(msg, sender):
    for c in clients:
        if c != sender:
            try:
                c.send(msg)
            except:
                clients.remove(c)

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg, client)
        except:
            clients.remove(client)
            client.close()
            break

def chat_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', PORT))
    server.listen()
    print(f"[SERVER] Chat started on port {PORT}")
    while True:
        client, addr = server.accept()
        print(f"[NEW] {addr}")
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

if __name__ == "__main__":
    chat_server()