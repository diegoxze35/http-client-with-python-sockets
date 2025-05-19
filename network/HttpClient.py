from abc import ABC, abstractmethod
from typing import Optional

from network.HttpResponse import HttpResponse

class HttpClient(ABC):
    """
    This class acts as a very simple HTTP client
    with methods GET, POST, PUT and DELETE.
    Also, it allows to add headers and close the
    connection.
    """
    HOST: str = 'Host'
    USER_AGENT: str = 'User-Agent'
    ACCEPT: str = 'Accept'
    CONTENT_TYPE: str = 'Content-Type'
    CONTENT_LENGTH: str = 'Content-Length'
    AUTHORIZATION: str = 'Authorization'
    CONNECTION: str = 'Connection'

    def __init__(self, base_url):
        """
        Contructor that receives an url to make a request.
        :param base_url: URL where the client will connect.
        """
        self.__base_url: str = ''
        self.__protocol: str = ''
        self.__hostname: str = ''
        self.__port: str = ''
        self.__path: str = ''
        self.__query: str = ''
        assert self.__is_valid_url(url=base_url), f'{base_url} is not a valid url'

    @abstractmethod
    def __enter__(self):
        """
        Method to use 'with' statement
        :return: it could return this client.
        """
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Default behavior is call close()
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return: None
        """
        pass

    def __is_valid_url(self, url: str) -> bool | None:
        """
        Check for valid url to make a request.
        :param url: URL where the client will connect.
        :return: True if the url is valid, otherwise it throws an exception.
        """
        try:
            self.__protocol, self.__base_url = url.split('://')
        except ValueError:
            raise Exception('Invalid URL')
        if self.__protocol != 'http' and self.__protocol != 'https':
            raise Exception(f'{self.__protocol} is not supported')
        # Get the hostname and port, example www.google.com:80
        hostname_port = self.__base_url.split('/')[0]
        try:
            self.__hostname, self.__port = hostname_port.split(':')
        except ValueError:
            self.__hostname = hostname_port
            self.__port = 80
        try:
            #print(self.__base_url.split('/'))
            for p in self.__base_url.split('/')[1:]:
                self.__path += f'/{p}'
            """
            self.__path = self.__base_url.split('/')[1]
            self.__path = '/' + self.__path
            """
        except IndexError:
            self.__path = '/'
        # remove any query string from our path
        if '?q=' in self.__path:
            self.__path = self.__path.split('?q=')[0]
        try:
            self.__query = self.__base_url.split('?q=')[1]
        except IndexError:
            self.__query = ''
        return True

    @property
    def base_url(self) -> str:
        return self.__base_url

    @base_url.setter
    def base_url(self, base_url: str):
        self.__base_url = ''
        self.__protocol = ''
        self.__hostname = ''
        self.__port = ''
        self.__path = ''
        self.__query = ''
        assert self.__is_valid_url(base_url), f'{base_url} is not a valid url'
        self.__base_url = base_url
        self._on_host_change()

    @property
    def protocol(self) -> str:
        return self.__protocol

    @property
    def hostname(self) -> str:
        return self.__hostname

    @property
    def port(self) -> str:
        return self.__port

    @property
    def path(self) -> str:
        return self.__path

    @property
    def query(self) -> str:
        return self.__query

    @abstractmethod
    def _connect(self) -> None:
        pass

    @abstractmethod
    def _on_host_change(self) -> None:
        """
        This method will be executed when the base url is changed.
        :return: None
        """
        pass

    @abstractmethod
    def add_header(self, header: str, value) -> None:
        pass

    @abstractmethod
    def remove_header(self, header: str) -> None:
        pass

    @abstractmethod
    def get(self) -> HttpResponse:
        pass

    @abstractmethod
    def post(self, body: str) -> HttpResponse:
        pass

    @abstractmethod
    def put(self, body: str) -> HttpResponse:
        pass

    @abstractmethod
    def delete(self, body: Optional[str] = None) -> HttpResponse:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
