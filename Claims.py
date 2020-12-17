import bs4
import requests

FedEx_url = 'https://www.fedex.com/apps/onlineclaims/?locale=en_US'

res = requests.get(FedEx_url)
bs = bs4.BeautifulSoup(res.text, "html.parser")


print(bs)