import re
from re import Match
from typing import Callable, Optional

from framework.http.request import HTTPRequest
from framework.http.response import HTTPResponse

class URLPattern:
  pattern: str
  view: Callable[[HTTPRequest], HTTPResponse]

  def __init__(self, pattern: str, view: Callable[[HTTPRequest], HTTPResponse]):
    self.pattern = pattern
    self.view = view

  def match(self, path: str) -> Optional[Match]:
    pattern = re.sub(r"<(.+?)>", r"(?P<\1>[^/]+)", self.pattern)
    return re.match(pattern, path)
