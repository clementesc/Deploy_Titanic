import requests

# teste 1
response = requests.get("http://127.0.0.1:8000/hello-world")
#print(response)

if response.status_code == 200:
    response_data = response.json()
    print(f"response: {response_data['message']}")
else:
    print(f"Erro na requisição\nStatus code: {response.status_code}")