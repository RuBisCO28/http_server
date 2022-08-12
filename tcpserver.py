import socket

class TCPServer:
  def serve(self):
    print("=== Launch Server ===")

    try:
      # generate socket
      server_socket = socket.socket()
      server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

      # assign socket to localhost:8080
      server_socket.bind(("localhost", 8080))
      server_socket.listen(10)

      print("=== Waiting connection ===")
      (client_socket, address) = server_socket.accept()
      print(f"=== Connection established remote_address: {address} ===")

      # Get request data from client
      request = client_socket.recv(4096)

      # Export request data
      with open("server_recv.txt", "wb") as f:
          f.write(request)

      # Input response data
      with open("server_send.txt", "rb") as f:
          response = f.read()

      # Send response to client
      client_socket.send(response)

      # Disconnect
      client_socket.close()

    finally:
        print("=== Stop server ===")

if __name__ == '__main__':
  server = TCPServer()
  server.serve()
