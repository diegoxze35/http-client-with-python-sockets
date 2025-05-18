from network.HttpClient import HttpClient
from socket import socket, gethostbyname, create_connection

from network.HttpResponse import HttpResponse


class SocketHttpClient(HttpClient):
    __BUFFER_SIZE = 1024

    def __init__(self, base_url):
        super().__init__(base_url)
        # Default configuration
        self.__request = {
            'start-line': '',
            'headers': {
                HttpClient.HOST: f'{self.hostname}:{self.port}',
                HttpClient.USER_AGENT: 'python-client',
                HttpClient.ACCEPT: '*/*',
                HttpClient.CONNECTION: 'Close'
            }
        }
        self.__socket: socket
        self._connect()
        print(self.path)

    def _connect(self):
        ip = gethostbyname(self.hostname)
        self.__socket = create_connection((ip, self.port), timeout=5)

    def _on_host_change(self):
        self.__request['headers'][HttpClient.HOST] = f'{self.hostname}:{self.port}'

    def add_header(self, header: str, value: str):
        self.__request['headers'][header] = value

    def get(self) -> HttpResponse:
        self.__request['start-line'] = f'GET {self.path}{self.query} HTTP/1.1'
        request_bytes = SocketHttpClient.__parse_request(self.__request)
        assert self.__socket.send(request_bytes) == len(request_bytes), 'An error occurred sending the request!'
        response = b''
        while True:
            response_bytes = self.__socket.recv(SocketHttpClient.__BUFFER_SIZE)
            if not response_bytes:
                break
            response += response_bytes
        return HttpResponse.from_bytes(response)


    def post(self, body: str) -> HttpResponse:
        self.__request['start-line'] = f'POST {self.path}{self.query} HTTP/1.1'

    def put(self) -> HttpResponse:
        self.__request['start-line'] = f'PUT {self.path}{self.query} HTTP/1.1'

    def delete(self) -> HttpResponse:
        self.__request['start-line'] = f'DELETE {self.path}{self.query} HTTP/1.1'

    def close(self) -> None:
        self.__socket.close()

    @staticmethod
    def __parse_request(data: dict[str, str], with_key=False) -> bytes:
        acc = b''
        for key, value in data.items():
            if isinstance(value, str):
                acc += f'{f'{key}: ' if with_key else ''}{value}\r\n'.encode()
            elif isinstance(value, dict):
                acc += SocketHttpClient.__parse_request(value, with_key=key == 'headers')
                acc += b'\r\n'
        return acc

