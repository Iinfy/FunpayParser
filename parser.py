import requests
from datetime import datetime
from bs4 import BeautifulSoup as BS
from logger import log
import urllib.parse as urp


class Lot:
    def __init__(self,desc,amount,price,userid,lot_id):
        self.desc = desc
        self.amount = amount
        self.price = price
        self.userid = userid
        self.lot_id = lot_id

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

@log.catch(level="ERROR")
def offerParser(id,isGroupingOn):
    OffersList = []
    answer = requests.get(f"https://funpay.com/users/{id}/")
    log.debug(f"Parsing user lots, Grouping: {isGroupingOn}, User ID: {id}, Status code: {answer.status_code}")
    if answer.status_code == 200:
        if not isGroupingOn:
            html = BS(answer.content,'html.parser')
            for offer in html.select(".mb20 > .offer"):
                container = offer.select(".offer-tc-container")[0]
                for item in container.select("a"):
                    desc = item.select_one(".tc-desc > .tc-desc-text").text
                    amount_elem = item.select_one(".tc-amount")
                    amount = amount_elem.text if amount_elem else "0"
                    price = item.select(".tc-price")[0].text
                    lot_url = parse_lot_id_from_url(item.get("href"))
                    lot = Lot(desc,amount,price,id,lot_url)
                    OffersList.append(lot)
        else:
            html = BS(answer.content,'html.parser')
            for offer in html.select(".mb20 > .offer"):
                listName = offer.select_one(".offer-list-title-container").text
                offerclass = OffersGroup(listName)
                container = offer.select(".offer-tc-container")[0]
                for item in container.select("a"):
                    lot_link = item.get("href")
                    desc = item.select_one(".tc-desc > .tc-desc-text").text
                    amount_elem = item.select_one(".tc-amount")
                    amount = amount_elem.text if amount_elem else "0"
                    price = item.select(".tc-price")[0].text
                    lot_url = parse_lot_id_from_url(item.get("href"))
                    lot = Lot(desc, amount, price, id, lot_url)
                    offerclass.offers.append(lot)
                OffersList.append(offerclass)
        return OffersList
    else:
        log.error(f"Parsing error, Status code: {answer.status_code}")
        return False

@log.catch(level="ERROR")
def review_parser(id):
    reviews_list = []
    answer = requests.get(f"https://funpay.com/users/{id}/")
    log.debug(f"Parsing user reviews, User ID: {id}, Status code: {answer.status_code}")
    html = BS(answer.content,'html.parser')
    for review in html.select(".offer > .dyn-table > .dyn-table-body > .review-container"):
        review_data = review.select_one(".review-item-detail").text.strip()
        review_text = review.select_one(".review-item-text").text.strip()
        reviews_list.append(Review(id,review_data,review_text, datetime.now()))
    return reviews_list

def parse_lot_id_from_url(url):
    parsed_url = urp.urlparse(url)
    try:
        lot_id = urp.parse_qs(parsed_url.query)['id'][0]
        return lot_id
    except:
        log.error("URL has no lot id")
        return False