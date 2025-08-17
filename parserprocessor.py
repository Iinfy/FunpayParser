import re

import parser
import database as db
from multiprocessing import Process
import time
from datetime import datetime
from logger import log

def startParsing(id,isGroupingOn,mode,parsing_frequency):
    log.info(f"Set parsing mode to {mode}")
    if mode == 1:
        log.info(f"Parsing started with mode {mode}")
        parseAndShowUserOffers(id,isGroupingOn)
        print("Parsed successful")
    elif mode == 2:
        log.info(f"Parsing started with mode {mode}")
        parseThread = Process(target=parseOffersAndShowChanges, args=(id,parsing_frequency,))
        parseThread.start()
        while True:
            toStop = input("Enter 'e' to stop parsing ")
            if toStop == "e":
                log.info("Stoping parsing due to exit command")
                parseThread.terminate()
                break
    elif mode == 3:
        log.info(f"Parsing started with mode {mode}")
        show_reviews(id)
        print("Parsed successful")
    elif mode == 4:
        log.info(f"Parsing started with mode {mode}")
        parse_thread = Process(target=parse_reviews_and_show_changes, args=(id,parsing_frequency,))
        parse_thread.start()
        while True:
            toStop = input("Enter 'e' to stop parsing ")
            if toStop == "e":
                log.info("Stoping parsing due to exit command")
                parse_thread.terminate()
                break
    elif mode == 5:
        log.info(f"Parsing started with mode {mode}")
        show_user_purchases(id)
    elif mode == 6:
        log.info(f"Parsing started with mode {mode}")
        show_user_reviews(id)
    else:
        log.warning("Incorrect parsing mode")



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
    log.info(f"Lots parsing completed successful, User ID: {id}, Mode: LotsParser(1)")
            
def parseOffersAndShowChanges(id, parsing_frequency):
    while True:
        changes = 0
        currentTime = datetime.now().time().strftime("%H:%M:%S")
        list = parser.offerParser(id,False)
        if list:
            db.uncheckLots(id)
            for lot in list:
                oldLot = db.getLotByHash(db.hashLotDesc(lot))
                if oldLot:
                    old_amount = int(oldLot.amount)
                    new_amount = int((lot.amount).replace(" ", "").strip())
                    price = re.sub(r"[^\d.,]", "", lot.price)
                    if new_amount < old_amount:
                        print(f"\n[{currentTime}] Совершена покупка \n{lot.desc}\n{old_amount} -> {new_amount}({old_amount - new_amount})\nСумма покупки: {(old_amount - new_amount)*oldLot.price}р")
                        purchase = db.Purchase(id, lot.desc, old_amount - new_amount, lot.price, datetime.now())
                        db.add_purchase(purchase)
                        changes = changes + 1
                    elif new_amount > old_amount:
                        print(f"\n[{currentTime}] Лот пополнен\n{lot.desc}\n{old_amount} -> {new_amount}")
                        changes = changes + 1
                    elif float(oldLot.price) != float(price):
                        print(f"\n[{currentTime}] Цена изменена\n{lot.desc}\n{oldLot.price} -> {price}")
                elif not oldLot:
                    print(f"\n[{currentTime}] Обнаружен новый лот\n{lot.desc}\nКол-во: {lot.amount}\nЦена: {str(lot.price).strip()}")
                    changes = changes + 1
                db.addLot(lot)
            for lot in db.getUncheckedLots(id):
                print(f"\n[{currentTime}] Лот был выкуплен или удален\n{lot.desc}\nЦена: {lot.price}р")
                changes = changes + 1
                db.deleteLotByHash(db.hashLotDesc(lot))
            if changes > 0:
                log.info(f"Changes found, Parsing frequency: {parsing_frequency}s, Mode: Comparator(2), Lot count: {len(list)}, Changes: {changes}")
        else:
            log.warning(f"Empty lot list, Parsing frequency: {parsing_frequency}s, Mode: Comparator(2)")
        time.sleep(parsing_frequency)

def show_reviews(id):
    reviews_list = parser.review_parser(id)
    for review in reviews_list:
        print(f"{review.data} - {review.text}")
    log.info(f"Review parsing completed successful, User ID: {id}, Mode: ReviewParser(3)")

def parse_reviews_and_show_changes(userid,parsing_frequency):
    while True:
        changes = 0
        currentTime = datetime.now().time().strftime("%H:%M:%S")
        reviews_list = parser.review_parser(userid)
        db.uncheck_reviews_by_userid(userid)
        for review in reviews_list:
            old_review = db.get_review_by_hash(db.hash_review(review))
            if not old_review:
                print(f"\n[{currentTime}] Обнаружен новый отзыв\n{review.data} - {review.text}")
                changes = changes + 1
            db.add_review(review)
        if changes > 0:
            log.info(f"Parsing user reviews and comparing with old, User ID: {id}, Parsing frequency: {parsing_frequency}s, Changes: {changes}")
        time.sleep(parsing_frequency)

def show_user_purchases(userid):
    purchases = db.get_user_purchases(userid)
    for purchase in purchases:
        print(f"\n[{purchase.date}] Покупка\n{purchase.desc}\n{purchase.amount}шт\nСумма: {purchase.amount * purchase.price}")
    print(f"\nВсе покупки пользователя {userid} отображены")
    log.info(f"Requested user purchases, User ID: {userid}")

def show_user_reviews(userid):
    reviews = db.get_user_reviews(userid)
    if reviews:
        for review in reviews:
            print(f"\n[{review.date}] Отзыв\n{review.data} - {review.text}")
        print(f"\nВсе отзывы пользователя {userid} отображены")
    log.info(f"Requested user reviews, User ID: {userid}")