from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class HttpResponse:
    version: str
    status_code: int
    date: Optional[datetime]
    server: Optional[str]
    last_modified: Optional[datetime]
    content_type: str
    content_length: Optional[int]
    body: Optional[str]

    @staticmethod
    def __get_header_value(key: str, response: list[str]) -> str | None:
        return next((val[len(key):] for val in response[1:] if val.startswith(key)), None)

    @classmethod
    def from_bytes(cls, response_bytes: bytes):
        date_header = 'Date: '
        date_formart = '%a, %d %b %Y %H:%M:%S GMT'
        server_header = 'Server: '
        last_modified_header = 'Last-Modified: '
        content_type_header = 'Content-Type: '
        content_length_header = 'Content-Length: '
        response_decoded = response_bytes.decode()
        response = response_decoded.split('\r\n')
        version, status_code, _ = response[0].split(' ')
        date_val = HttpResponse.__get_header_value(date_header, response)
        if date_val:
            date = datetime.strptime(date_val, date_formart)
        else:
            date = None
        server = HttpResponse.__get_header_value(server_header, response)
        last_modified_val = HttpResponse.__get_header_value(last_modified_header, response)
        if last_modified_val:
            last_modified = datetime.strptime(last_modified_val, date_formart)
        else:
            last_modified = None
        content_type = HttpResponse.__get_header_value(content_type_header, response)
        content_length = HttpResponse.__get_header_value(content_length_header, response)
        body = response_decoded.split("\r\n\r\n", maxsplit=1)[1]
        return cls(version, int(status_code), date, server, last_modified, content_type, content_length, body)
