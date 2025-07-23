import requests
from bs4 import BeautifulSoup as BS


class Lot:
    def __init__(self,desc,amount,price,userid):
        self.id = userid
        self.desc = desc
        self.amount = amount
        self.price = price
        
class OffersGroup:
    def __init__(self,ListName):
        self.listName = ListName
        self.offers = []
        
        

def offerParser(id,isGroupingOn):
    OffersList = []
    answer = requests.get(f"https://funpay.com/users/{id}/")
    if not isGroupingOn:
        html = BS(answer.content,'html.parser')
        for offer in html.select(".mb20 > .offer"):
            container = offer.select(".offer-tc-container")[0]
            for item in container.select("a"):
                desc = item.select_one(".tc-desc > .tc-desc-text").text
                amount_elem = item.select_one(".tc-amount")
                amount = amount_elem.text if amount_elem else "0"
                price = item.select(".tc-price")[0].text
                lot = Lot(desc,amount,price,id)
                OffersList.append(lot)
    else:
        html = BS(answer.content,'html.parser')
        for offer in html.select(".mb20 > .offer"):
            listName = offer.select_one(".offer-list-title-container").text
            offerclass = OffersGroup(listName)
            container = offer.select(".offer-tc-container")[0]
            for item in container.select("a"):
                desc = item.select_one(".tc-desc > .tc-desc-text").text
                amount_elem = item.select_one(".tc-amount")
                amount = amount_elem.text if amount_elem else "0"
                price = item.select(".tc-price")[0].text
                lot = Lot(desc,amount,price,id)
                offerclass.offers.append(lot)
            OffersList.append(offerclass)
            
    return OffersList

