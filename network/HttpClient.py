from abc import ABC, abstractmethod

from network.HttpResponse import HttpResponse

class HttpClient(ABC):
    HOST: str = 'Host'
    USER_AGENT: str = 'User-Agent'
    ACCEPT: str = 'Accept'
    CONTENT_TYPE: str = 'Content-Type'
    AUTHORIZATION: str = 'Authorization'
    CONNECTION: str = 'Connection'

    def __init__(self, base_url):
        self.__base_url: str = None
        self.__protocol: str
        self.__hostname: str
        self.__port: str
        self.__path: str = ''
        self.__query: str
        assert self.__is_valid_url(url=base_url), f'{base_url} is not a valid url'

    def __is_valid_url(self, url: str) -> bool | None:
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
        assert self.__is_valid_url(base_url), f'{base_url} is not a valid url'
        self._on_host_change()
        self.__base_url = base_url

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
        pass

    @abstractmethod
    def add_header(self, header: str, value: str) -> None:
        pass

    @abstractmethod
    def get(self) -> HttpResponse:
        pass

    @abstractmethod
    def post(self, body) -> HttpResponse:
        pass

    @abstractmethod
    def put(self) -> HttpResponse:
        pass

    @abstractmethod
    def delete(self) -> HttpResponse:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
