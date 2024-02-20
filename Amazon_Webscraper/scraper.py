from bs4 import BeautifulSoup
from requests_html import HTMLSession
import numpy as np
import time

print("Amazon WebScraper\n__________________")
url = 'https://www.amazon.de/s?k=' + input('Search:')
print("Searching at: " + url +"\n")

class Product:
    def __init__(self, price, title):
        self.price = price
        self.title = title

    def getprice(self):
        return self.price

    def gettitle(self):
        shorttitle1 = self.title.split('(')[0]
        shorttitle2 = shorttitle1 + "w"
        try:
            commasplit = self.title.split(',')

            appendString = ""
            for split in commasplit:
                if (split[0] == " "):
                    shorttitle2 = commasplit[0] + split
                    break
            dashsplit = self.title.split('-')

            i = 1
            appendString = ""
            while i < len(dashsplit):
                if (dashsplit[i][0] == " "):
                    shorttitle2 = dashsplit[i - 1] + appendString
                    break
                appendString += dashsplit[i]
                i += 1
        except:
            print("no comma")

        if (len(shorttitle2) < len(shorttitle1)):
            return shorttitle2

        return shorttitle1


def getdata(url):
    s = HTMLSession()
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

#returns link to the next page, currently not used
def getnextpage(soup):
    page = soup.find('span', {'class': 's-pagination-strip'})
    if not page.find('span', {'class': 's-pagination-item s-pagination-next s-pagination-disabled'}):
        url = "https://www.amazon.de" + str(page.find('a', {'class': 's-pagination-next'})['href'])
        return url
    else:
        return


def getinfo(soup):
    try:
        titles = soup.findAll('span', class_=['a-size-medium a-color-base a-text-normal',
                                              'a-size-base-plus a-color-base a-text-normal'])
        prices = soup.findAll('span', {'class': 'a-price-whole'})
        infos = np.concatenate((titles, prices), axis=1)
        print('Prices: ' + str(len(prices)))
        print('Titles: ' + str(len(titles)))
        print(str(getinfo.counter))
        return infos
    except:
        getinfo.counter += 1
        time.sleep(1)
        print("Loading..." + str(getinfo.counter), end='\x1b[1K\r') #Actually Crashing
        print()
        return getinfo(getdata(url))


getinfo.counter = 0

#prints all available pages of a amazon-search
"""
while True:
    soup = getdata(url)
    url = getnextpage(soup)
    if not url:
        break
    print(url)
"""

soup = getdata(url)
infos = getinfo(soup)

productList = [infos]

for info in infos:
    price = float(str(info).split('\'')[3].replace('.', '').replace(',', '.'))
    title = str(info).split('\'')[1]
    print(str(price) + " | " + title)

# print(productList)

sort = input("Do you want to sort the list? (yes/no)")

prices = []
titles = []
products = []
index = 0
for info in infos:
    price = float(str(info).split('\'')[3].replace('.', '').replace(',', '.'))
    title = str(info).split('\'')[1]
    prices.append(price)
    titles.append(title)
    prices.sort()

    product = Product(price, title)

    products.append(product)

    index = index + 1
if (sort == "yes"):
    products.sort(key=lambda x: x.price, reverse=True)
    for product in products:
        print(str(product.getprice()) + " | " + product.gettitle())

else:
    for product in products:
        print(str(product.getprice()) + " | " + product.gettitle())