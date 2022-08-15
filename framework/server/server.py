import socket

from framework.server.worker import Worker

class Server:
  def serve(self):
    print("=== Server: Launch Server ===")

    try:
      server_socket = self.create_server_socket()

      while True:
        print("=== Server: Waiting connection ===")
        (client_socket, address) = server_socket.accept()
        print(f"=== Server: Connection established remote_address: {address} ===")

        thread = Worker(client_socket, address)
        thread.start()

    finally:
        print("=== Server: Stop server ===")

  def create_server_socket(self) -> socket:
    # generate socket
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # assign socket to localhost:8080
    server_socket.bind(("localhost", 8080))
    server_socket.listen(10)
    return server_socket
