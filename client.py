import sys
import asyncio
import websockets
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton

class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.websocket = None
        self.username = "Guest"

    def initUI(self):
        self.setWindowTitle("Chat App")
        self.setGeometry(100, 100, 400, 500)

        self.layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.layout.addWidget(self.chat_display)

        self.message_input = QLineEdit()
        self.layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.setLayout(self.layout)

    async def connect_to_server(self):
        try:
            self.websocket = await websockets.connect("ws://216.24.57.4:8765")
            asyncio.create_task(self.receive_messages())
        except Exception as e:
            self.chat_display.append(f"Connection error: {e}")

    async def receive_messages(self):
        try:
            async for message in self.websocket:
                self.chat_display.append(message)
        except Exception as e:
            self.chat_display.append(f"Error receiving message: {e}")

    def send_message(self):
        message = self.message_input.text()
        if message and self.websocket:
            asyncio.create_task(self.websocket.send(json.dumps({"user": self.username, "message": message})))
            self.message_input.clear()

async def start_client():
    app = QApplication(sys.argv)
    client = ChatClient()
    client.show()
    await client.connect_to_server()
    sys.exit(app.exec_())

if __name__ == "__main__":
    asyncio.run(start_client())

# Server-side WebSocket chat server
connected_clients = set()

async def handle_client(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            broadcast_message = f"{data['user']}: {data['message']}"
            await asyncio.wait([client.send(broadcast_message) for client in connected_clients if client != websocket])
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)

async def start_server():
    server = await websockets.serve(handle_client, "0.0.0.0", 8765)
    print("Server started on ws://0.0.0.0:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(start_server())
