import requests
from datetime import datetime
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

class Review:
    def __init__(self,userid,data,text, date):
        self.userid = userid
        self.data = data
        self.text = text
        self.date = date
        
        

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

def review_parser(id):
    reviews_list = []
    answer = requests.get(f"https://funpay.com/users/{id}/")
    html = BS(answer.content,'html.parser')
    for review in html.select(".offer > .dyn-table > .dyn-table-body > .review-container"):
        review_data = review.select_one(".review-item-detail").text.strip()
        review_text = review.select_one(".review-item-text").text.strip()
        reviews_list.append(Review(id,review_data,review_text, datetime.now()))
    return reviews_list

