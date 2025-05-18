from network.HttpClient import HttpClient
from client.SocketHttpClient import SocketHttpClient

if __name__ == '__main__':
    client: HttpClient = SocketHttpClient('https://jsonplaceholder.typicode.com/posts')
    reponse = client.get()
    print(reponse.status_code)
    print(reponse.body)
    client.close()