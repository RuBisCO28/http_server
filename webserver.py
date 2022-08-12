import socket
from datetime import datetime
import os

class WebServer:
  BASE_DIR = os.path.dirname(os.path.abspath(__file__))
  STATIC_ROOT = os.path.join(BASE_DIR, "static")

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

      request_line, remain = request.split(b"\r\n",maxsplit=1)
      request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)

      # parse request_line
      method, path, http_version = request_line.decode().split(" ")

      # get static file path
      relative_path = path.lstrip("/")
      static_file_path = os.path.join(self.STATIC_ROOT, relative_path)

      print(static_file_path)
      # generate response body
      with open(static_file_path, "rb") as f:
        response_body = f.read()

      # generate response line
      response_line = "HTTP/1.1 200 OK\r\n"

      # generate response header
      response_header = ""
      response_header += f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
      response_header += "Host: ToyServer/0.1\r\n"
      response_header += f"Content-Length: {len(response_body)}\r\n"
      response_header += "Connection: Close\r\n"
      response_header += "Content-Type: text/html\r\n"

      response = (response_line + response_header + "\r\n").encode() + response_body

      # Send response to client
      client_socket.send(response)

      # Disconnect
      client_socket.close()

    finally:
        print("=== Stop server ===")

if __name__ == '__main__':
  server = WebServer()
  server.serve()
