import requests
def test():
    r = requests.get('https://www.google.com.tw/')
    print("status",r.status_code)