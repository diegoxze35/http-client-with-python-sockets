from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class HttpResponse:
    version: str
    status_code: str
    date: Optional[datetime]
    server: Optional[str]
    last_modified: Optional[datetime]
    connection: str
    content_type: str
    content_length: Optional[int]
    content_location: Optional[str]
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
        conection_header = 'Connection: '
        content_type_header = 'Content-Type: '
        content_length_header = 'Content-Length: '
        content_location_header = 'Content-Location: '
        response_decoded = response_bytes.decode()
        response = response_decoded.split('\r\n')
        fisrt_line = response[0].split(' ', maxsplit=1)
        version, status_code = fisrt_line if len(fisrt_line) == 2 else ('HTTP / 1.1', fisrt_line[0])
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
        connection = HttpResponse.__get_header_value(conection_header, response)
        content_type = HttpResponse.__get_header_value(content_type_header, response)
        content_length = HttpResponse.__get_header_value(content_length_header, response)
        content_location = HttpResponse.__get_header_value(content_location_header, response)
        """
        print(body_response)
        body = body_response[1] if len(body_response) > 1 else body_response[0]
        """
        body_response = response_decoded.split("\r\n\r\n", maxsplit=1)
        body = body_response[1] if len(body_response) > 1 else None
        return cls(version=version, status_code=status_code, date=date, server=server, last_modified=last_modified,
                   connection=connection, content_type=content_type, content_length=content_length,
                   content_location=content_location, body=body)
