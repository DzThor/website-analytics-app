import requests

r = requests.get("http://socialmention.com/search?q=iphone+apps")

print(r.status_code)
print(r.content)
