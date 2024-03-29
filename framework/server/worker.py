from socket import socket
from datetime import datetime
import traceback
from typing import Tuple
from threading import Thread
import re

from framework.http.request import HTTPRequest
from framework.http.response import HTTPResponse
from framework.urls.resolver import URLResolver

class Worker(Thread):
  # extension and MIME Type
  MIME_TYPES = {
    "html": "text/html; charset=UTF-8",
    "css": "text/css",
    "png": "image/png",
    "jpg": "image/jpg",
    "gif": "image/gif",
  }

  # status code
  STATUS_LINES = {
    200: "200 OK",
    302: "302 Found",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
  }

  def __init__(self, client_socket: socket, address: Tuple[str, int]):
    super().__init__()

    self.client_socket = client_socket
    self.client_address = address

  def run(self) -> None:
    try:
      # Get request data from client
      request_bytes = self.client_socket.recv(4096)

      # Export request data
      with open("server_recv.txt", "wb") as f:
        f.write(request_bytes)

      request = self.parse_http_request(request_bytes)

      view = URLResolver().resolve(request)

      # generate response
      response = view(request)

      if isinstance(response.body, str):
        response.body = response.body.encode()

      response_line = self.build_response_line(response)
      response_header = self.build_response_header(response, request)

      response_bytes = (response_line + response_header + "\r\n").encode() + response.body

      # Send response to client
      self.client_socket.send(response_bytes)

    except Exception:
      print("=== Worker: Error occurred during request ===")
      traceback.print_exc()

    finally:
      # Disconnect
      print(f"=== Worker: Disconnect remote_address:{self.client_address} ===")
      self.client_socket.close()

  def parse_http_request(self, request: bytes) -> HTTPRequest:
    request_line, remain = request.split(b"\r\n",maxsplit=1)
    request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)

    # parse request_line
    method, path, http_version = request_line.decode().split(" ")

    headers = {}
    for header_now in request_header.decode().split("\r\n"):
      key, value = re.split(r": *", header_now, maxsplit=1)
      headers[key] = value

    cookies = {}
    if "Cookie" in headers:
      cookie_strings = headers["Cookie"].split("; ")
      for cookie_string in cookie_strings:
        name, value = cookie_string.split("=", maxsplit=1)
        cookies[name] = value

    return HTTPRequest(
      method=method, path=path, http_version=http_version, headers=headers, cookies=cookies, body=request_body
    )

  def build_response_line(self, response: HTTPResponse) -> str:
    status_line = self.STATUS_LINES[response.status_code]
    return f"HTTP/1.1 {status_line}"

  def build_response_header(self, response: HTTPResponse, request: HTTPRequest) -> str:
    if response.content_type is None:
      if "." in request.path:
        ext = request.path.rsplit(".", maxsplit=1)[-1]
        response.content_type = self.MIME_TYPES.get(ext, "application/octet-stream")
      else:
        response.content_type = "text/html; charset=UTF-8"

    # generate response header
    response_header = ""
    response_header += f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
    response_header += "Host: ToyServer/0.1\r\n"
    response_header += f"Content-Length: {len(response.body)}\r\n"
    response_header += "Connection: Close\r\n"
    response_header += f"Content-Type: {response.content_type}\r\n"

    for cookie in response.cookies:
      cookie_header = f"Set-Cookie: {cookie.name}={cookie.value}"
      if cookie.expires is not None:
        cookie_header += f"; Expires={cookie.expires.strftime('%a, %d %b %Y %H:%M:%S GMT')}"
      if cookie.max_age is not None:
        cookie_header += f"; Max-Age={cookie.max_age}"
      if cookie.domain:
        cookie_header += f"; Domain={cookie.domain}"
      if cookie.path:
        cookie_header += f"; Path={cookie.path}"
      if cookie.secure:
        cookie_header += "; Secure"
      if cookie.http_only:
        cookie_header += "; HttpOnly"

      response_header += cookie_header + "\r\n"

    for header_name, header_value in response.headers.items():
      response_header += f"{header_name}: {header_value}\r\n"

    return response_header
