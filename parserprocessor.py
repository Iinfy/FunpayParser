import parser
import database as db
from multiprocessing import Process
import time
from datetime import datetime

def startParsing(id,isGroupingOn,mode):
    if mode == 1:
        parseAndShowUserOffers(id,isGroupingOn)
        print("Parsed successful")
    elif mode == 2:
        parseThread = Process(target=parseOffersAndShowChanges, args=(id,))
        parseThread.start()
        while True:
            toStop = input("Enter 'e' to stop parsing ")
            if toStop == "e":
                parseThread.terminate()
                break
    elif mode == 3:
        show_reviews(id)
        print("Parsed successful")
    elif mode == 4:
        parse_thread = Process(target=parse_reviews_and_show_changes, args=(id,))
        parse_thread.start()
        while True:
            toStop = input("Enter 'e' to stop parsing ")
            if toStop == "e":
                parse_thread.terminate()
                break


def parseAndShowUserOffers(id,isGroupingOn):
    if isGroupingOn:
        list = parser.offerParser(id,True)
        for offerClass in list:
            print(offerClass.listName)
            for lot in offerClass.offers:
                db.addLot(lot)
                print(f"{lot.desc} {f"\n{lot.amount}шт" if lot.amount != 0 else ""} {lot.price}".strip())
    else:
        list = parser.offerParser(id,False)
        for lot in list:
            db.addLot(lot)
            print(f"{lot.desc} {f"\n{lot.amount}шт" if lot.amount != 0 else ""} {lot.price}".strip())
            
def parseOffersAndShowChanges(id):
    while True:
        currentTime = datetime.now().time().strftime("%H:%M:%S")
        time.sleep(15)
        db.uncheckLots(id)
        list = parser.offerParser(id,False)
        for lot in list:
            oldLot = db.getLotByHash(db.hashLotDesc(lot))
            if oldLot:
                old_amount = int(oldLot.amount)
                new_amount = int((lot.amount).replace(" ", "").strip())
                if new_amount < old_amount:
                    print(f"\n[{currentTime}] Совершена покупка \n{lot.desc}\n{old_amount} -> {new_amount}({old_amount - new_amount})\nСумма покупки: {(old_amount - new_amount)*oldLot.price}р")
                    purchase = db.Purchase(id, lot.desc, old_amount - new_amount, lot.price, datetime.now())
                    db.add_purchase(purchase)
                elif new_amount > old_amount:
                    print(f"\n[{currentTime}] Лот пополнен\n{lot.desc}\n{old_amount} -> {new_amount}")
            elif not oldLot:
                print(f"\n[{currentTime}] Обнаружен новый лот\n{lot.desc}\nКол-во: {lot.amount}\nЦена: {str(lot.price).strip()}")
            db.addLot(lot)
        for lot in db.getUncheckedLots(id):
            print(f"\n[{currentTime}] Лот был выкуплен или удален\n{lot.desc}\nЦена: {lot.price}р")
            db.deleteLotByHash(db.hashLotDesc(lot))

def show_reviews(id):
    reviews_list = parser.review_parser(id)
    for review in reviews_list:
        print(f"{review.data} - {review.text}")

def parse_reviews_and_show_changes(userid):
    while True:
        currentTime = datetime.now().time().strftime("%H:%M:%S")
        reviews_list = parser.review_parser(userid)
        db.uncheck_reviews_by_userid(userid)
        for review in reviews_list:
            old_review = db.get_review_by_hash(db.hash_review(review))
            if not old_review:
                print(f"\n[{currentTime}] Обнаружен новый отзыв\n{review.data} - {review.text}")
            db.add_review(review)
