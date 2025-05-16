import requests

print(requests.get('http://127.0.0.1:8080/api/jobs/1').json())  # all ok
print(requests.get('http://127.0.0.1:8080/api/jobs').json())  # all ok
print(requests.get('http://127.0.0.1:8080/api/jobs/10').json())  # no key
print(requests.get('http://127.0.0.1:8080/api/jobs/q'))  # no key
