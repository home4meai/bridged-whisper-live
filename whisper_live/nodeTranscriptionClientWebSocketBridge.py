import json
import threading
from websockets.sync.server import serve

class NodeTranscriptionSocket:
    def __init__(self, host='0.0.0.0', port=9080, message_callback=None):
        self.host = host
        self.port = port
        self.message_callback = message_callback
        self.client_sockets = []  # List to store client sockets

        print(f"Server listening on port {self.port}")

    def start(self):
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        with serve(self.handle_client, self.host, self.port) as server:
            server.serve_forever()

    def handle_client(self, websocket):
        self.client_sockets.append(websocket)  # Store the new socket
        try:
            for message in websocket:
                print(f"Received: {message}")
                if self.message_callback is not None:
                    self.message_callback(message) 
        finally:
            self.client_sockets.remove(websocket)  # Remove the socket when done

    def send_json(self, message):
        # Send the JSON message as text to all connected clients
        for client_socket in self.client_sockets:
            client_socket.send(json.dumps(message).encode('ascii'))