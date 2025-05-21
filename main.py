from network.HttpClient import HttpClient
from client.SocketHttpClient import SocketHttpClient

if __name__ == '__main__':
    client: HttpClient = SocketHttpClient('http://localhost:80/')
    with client as g:
        reponse = client.get()
        print(reponse.status_code)
        print(reponse.body)
    client.base_url = 'https://localhost:443/'
    with client as gs:
        reponse = client.get()
        print(reponse.status_code)
        print(reponse.body)
