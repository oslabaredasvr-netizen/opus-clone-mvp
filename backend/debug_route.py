import requests
try:
    print('Enviando POST de teste bruto...')
    res = requests.post("http://localhost:8080/api/v1/art/generate", json={"theme": "teste"}, allow_redirects=False)
    print(res.status_code)
    print(res.text)
except Exception as e:
    print(e)
