import requests

def valid(url1, url2, url3):
    x = requests.get(url1)
    y = requests.get(url2)
    z = requests.get(url3)
    if x.status_code == 200:
        return url1
    elif y.status_code == 200:
        return url2
    elif z.status_code == 200:
        return url3
    else:
        return 'Error'