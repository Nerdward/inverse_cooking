import requests

data = {
    'filename':'1.jpg',
    'content_type':'image/jpeg',
    'file': open('1.jpg','rb')
}
# data = open('1.jpg','rb').read()
r = requests.post('http://127.0.0.1:8000/predict',files=data)

print(r.text)