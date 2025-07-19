import requests
from bs4 import BeautifulSoup as BS


class Lot:
    def __init__(self,desc,amount,price):
        self.desc = desc
        self.amount = amount
        self.price = price
        
class OfferClass:
    def __init__(self,ListName):
        self.listName = ListName
        self.offers = []
        
        

def offerParser(id):
    OffersList = []
    answer = requests.get(f"https://funpay.com/users/{id}/")
    html = BS(answer.content,'html.parser')


    for offer in html.select(".mb20 > .offer"):
        listName = offer.select_one(".offer-list-title-container").text
        offerclass = OfferClass(listName)
        container = offer.select(".offer-tc-container")[0]
        for item in container.select("a"):
            desc = item.select_one(".tc-desc > .tc-desc-text").text
            amount_elem = item.select_one(".tc-amount")
            amount = amount_elem.text if amount_elem else 0
            price = item.select(".tc-price")[0].text
            lot = Lot(desc,amount,price)
            offerclass.offers.append(lot)
            print(f"{lot.desc} {f"{lot.amount}шт" if lot.amount != 0 else ""} {lot.price}")
        OffersList.append(offerclass)
            
    return OffersList