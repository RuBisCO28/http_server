from typing import Callable, Optional

from framework.http.request import HTTPRequest
from framework.http.response import HTTPResponse
from framework.views.static import static
from urls import url_patterns

class URLResolver:
  def resolve(self, request: HTTPRequest) -> Callable[[HTTPRequest], HTTPResponse]:
    for url_pattern in url_patterns:
      match = url_pattern.match(request.path)
      if match:
        request.params.update(match.groupdict())
        return url_pattern.view

    return static
