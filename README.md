# Example usage
```python
from network.HttpClient import HttpClient
from client.SocketHttpClient import SocketHttpClient

if __name__ == '__main__':
    client: HttpClient = SocketHttpClient('https://jsonplaceholder.typicode.com/posts')
    with client as g:
        reponse = client.get()
        print(reponse.status_code)
        print(reponse.body)
    with client as p:
        new = '{' \
                '\"title\": \"ESCOM\",' \
                '\"body\": \"POST TEST\",' \
                '\"userId\": 1' \
              '}'
        print(new)
        #Be aware to add necessary headers for each request
        p.add_header(HttpClient.CONTENT_TYPE, 'application/json; charset=utf-8')
        p.add_header(HttpClient.CONTENT_LENGTH, len(new))
        response = p.post(new)
        print(response.status_code)
        print(response.body)
    with client as pu:
        updated = '{' \
                f'\"id\": 1,' \
                '\"title\": \"ESCOM\",' \
                '\"body\": \"POST TEST\",' \
                '\"userId\": 1' \
              '}'
        p.add_header(HttpClient.CONTENT_LENGTH, len(updated)) #Update header
        reponse = pu.put(updated)
        print(response.status_code)
        print(response.body)
    client.base_url = 'https://jsonplaceholder.typicode.com/posts/1'
    with client as d:
        d.remove_header(HttpClient.CONTENT_TYPE) #Be aware to remove unnecessary headers for each request
        d.remove_header(HttpClient.CONTENT_LENGTH)
        response = d.delete()
        print(response.status_code)
        print(response.body)

```
