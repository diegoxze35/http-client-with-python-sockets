from typing import Optional

from network.HttpClient import HttpClient
from socket import socket, gethostbyname, create_connection

from network.HttpResponse import HttpResponse


class SocketHttpClient(HttpClient):
    """
    Implementation of HttpClient using a socket object
    all http messages are treated as strings and bytes
    """
    __BUFFER_SIZE = 1024 #Default buffer size to read from socket

    def __init__(self, base_url):
        super().__init__(base_url)
        # Default configuration
        self.__request = {
            'start-line': '',
            'headers': {
                HttpClient.HOST: f'{self.hostname}:{self.port}',
                HttpClient.USER_AGENT: 'python-client',
                HttpClient.ACCEPT: '*/*',
                HttpClient.CONNECTION: 'close'
            }
        }
        self.__connected = True
        ip = gethostbyname(self.hostname)
        self.__socket: socket = create_connection((ip, self.port), timeout=5)

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _connect(self):
        if not self.__connected:
            ip = gethostbyname(self.hostname)
            self.__socket = create_connection((ip, self.port), timeout=5)
            self.__connected = True

    def _on_host_change(self):
        self.__request['headers'][HttpClient.HOST] = f'{self.hostname}:{self.port}'

    def add_header(self, header: str, value):
        self.__request['headers'][header] = value

    def remove_header(self, header: str):
        if header in self.__request['headers'].keys():
            del self.__request['headers'][header]

    def get(self) -> HttpResponse:
        self.__request['start-line'] = f'GET {self.path}{self.query} HTTP/1.1'
        self.remove_header(HttpClient.CONTENT_TYPE)
        self.remove_header(HttpClient.CONTENT_LENGTH)
        request_bytes = SocketHttpClient.__parse_request(self.__request)
        self.__socket.sendall(request_bytes)
        response = b''
        while True:
            response_bytes = self.__socket.recv(SocketHttpClient.__BUFFER_SIZE)
            if not response_bytes:
                break
            response += response_bytes
        return HttpResponse.from_bytes(response)

    def post(self, body: str) -> HttpResponse:
        self.__request['start-line'] = f'POST {self.path}{self.query} HTTP/1.1'
        self.__request['body'] = body
        # self.__request['headers'][HttpClient.CONTENT_LENGTH] = len(body)
        request_bytes = SocketHttpClient.__parse_request(self.__request)
        print(request_bytes)
        self.__socket.sendall(request_bytes)
        response = b''
        while True:
            response_bytes = self.__socket.recv(SocketHttpClient.__BUFFER_SIZE)
            if not response_bytes:
                break
            response += response_bytes
        return HttpResponse.from_bytes(response)

    def put(self, body: str) -> HttpResponse:
        self.__request['start-line'] = f'PUT {self.path}{self.query} HTTP/1.1'
        self.__request['body'] = body
        # self.__request['headers'][HttpClient.CONTENT_LENGTH] = len(body)
        request_bytes = SocketHttpClient.__parse_request(self.__request)
        self.__socket.sendall(request_bytes)
        response = b''
        while True:
            response_bytes = self.__socket.recv(SocketHttpClient.__BUFFER_SIZE)
            if not response_bytes:
                break
            response += response_bytes
        return HttpResponse.from_bytes(response)

    def delete(self, body: Optional[str] = None) -> HttpResponse:
        self.__request['start-line'] = f'DELETE {self.path}{self.query} HTTP/1.1'
        if body:
            self.__request['body'] = body
        elif 'body' in self.__request.keys():
            del self.__request['body']
        request_bytes = SocketHttpClient.__parse_request(self.__request)
        print(request_bytes)
        self.__socket.sendall(request_bytes)
        response = b''
        while True:
            response_bytes = self.__socket.recv(SocketHttpClient.__BUFFER_SIZE)
            if not response_bytes:
                break
            response += response_bytes
        return HttpResponse.from_bytes(response)

    def close(self) -> None:
        self.__connected = False
        self.__socket.close()

    @staticmethod
    def __parse_request(data: dict[str, str], with_key=False) -> bytes:
        """
        This method parses a string http request to bytes http request
        because the sockets only work with a bytes-like object
        :param data: The whole request as string
        Example:
        "DELETE /posts/1 HTTP/1.1\r\nHost: jsonplaceholder.typicode.com:80\r\nUser-Agent: python-client\r\nAccept: */*\r\nConnection: close\r\n\r\n"
        :param with_key: boolean variable to incluide a request key in the convertions (HTTP headers needs to be sent with their key)
        :return: A bytes http request
        """
        acc = b''
        for key, value in data.items():
            if not isinstance(value, dict):
                acc += f'{f'{key}: ' if with_key else ''}{value}\r\n'.encode()
            else:
                acc += SocketHttpClient.__parse_request(value, with_key=key == 'headers')
                acc += b'\r\n'
        return acc
