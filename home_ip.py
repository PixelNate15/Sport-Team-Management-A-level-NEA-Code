import urllib.request

_URL = 'https://www.nwinchester.co.uk/ip/getIP.php?secret=765KGH45KLf'


def getHomeIP() -> str:
    with urllib.request.urlopen(_URL, timeout=10) as response:
        return response.read().decode().strip()


if __name__ == '__main__':
    print(getHomeIP())
