import re

import parser
import database as db
from multiprocessing import Process
import time
from datetime import datetime
from logger import log

def startParsing(id,mode,parsing_frequency):
    log.info(f"Set parsing mode to {mode}")
    if mode == 1:
        log.info(f"Parsing started with mode {mode}")
        parse_and_show_user_offers(id)
        print("Parsed successful")
    elif mode == 2:
        log.info(f"Parsing started with mode {mode}")
        parse_thread = Process(target=parseOffersAndShowChanges, args=(id,parsing_frequency,))
        parse_thread.start()
        while True:
            toStop = input("Enter 'e' to stop parsing ")
            if toStop == "e":
                log.info("Stoping parsing due to exit command")
                parse_thread.terminate()
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
        show_user_reviews(id)
    else:
        log.warning("Incorrect parsing mode")



def parse_and_show_user_offers(id):
    list = parser.offerParser(id)
    for lot in list:
        db.add_lot(lot)
        print(f"{lot.desc} {f"\n{lot.amount}шт" if lot.amount != 0 else ""} {lot.price}".strip())
    log.info(f"Lots parsing completed successful, User ID: {id}, Mode: LotsParser(1)")
            
def parseOffersAndShowChanges(id, parsing_frequency):
    while True:
        changes = 0
        current_time = datetime.now().time().strftime("%H:%M:%S")
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lot_list = parser.offerParser(id)
        if list:
            db.uncheckLots(id)
            for lot in lot_list:
                old_lot = db.get_lot_by_id(lot.lot_id)
                if old_lot:
                    old_amount = int(old_lot.amount)
                    new_amount = int((lot.amount).replace(" ", "").strip())
                    price = re.sub(r"[^\d.,]", "", lot.price)
                    if new_amount < old_amount:
                        message = f"Purchase \n{lot.desc}\n{old_amount} -> {new_amount}({old_amount - new_amount})\nAmount: {(old_amount - new_amount)*old_lot.price}Rub"
                        print(f"\n[{current_time}]{message}")
                        action = db.Action(current_datetime,lot.userid,lot.lot_id,"purchase", message)
                        db.add_action(action)
                        changes = changes + 1
                    elif new_amount > old_amount:
                        message = f"Lot restocked\n{lot.desc}\n{old_amount} -> {new_amount}"
                        print(f"\n[{current_time}]{message}")
                        action = db.Action(current_datetime, lot.userid, lot.lot_id, "restock", message)
                        db.add_action(action)
                        changes = changes + 1
                    elif float(old_lot.price) != float(price):
                        message = f"Price changed\n{lot.desc}\n{old_lot.price}Rub -> {price}Rub"
                        print(f"\n[{current_time}]{message}")
                        action = db.Action(current_datetime, lot.userid, lot.lot_id, "price", message)
                        db.add_action(action)
                        changes = changes + 1
                elif not old_lot:
                    message = f"New lot found\n{lot.desc}\nAmount: {lot.amount}\nPrice: {str(lot.price).strip()}Rub"
                    print(f"\n[{current_time}]{message}")
                    action = db.Action(current_datetime, lot.userid, lot.lot_id, "new_lot", message)
                    db.add_action(action)
                    changes = changes + 1
                db.add_lot(lot)
            for lot in db.getUncheckedLots(id):
                message = f"The lot was purchased or removed\n{lot.desc}\nPrice: {lot.price}Rub"
                print(f"\n[{current_time}]{message}")
                action = db.Action(current_datetime, lot.userid, lot.lot_id, "lot_deleted", message)
                db.add_action(action)
                changes = changes + 1
                db.delete_lot_by_id(lot.lot_id)
            if changes > 0:
                log.info(f"Changes found, Parsing frequency: {parsing_frequency}s, Mode: Comparator(2), Lot count: {len(lot_list)}, Changes: {changes}")
        else:
            log.warning(f"Empty lot list, Parsing frequency: {parsing_frequency}s, Mode: Comparator(2)")
        time.sleep(parsing_frequency)

def show_reviews(userid):
    reviews_list = parser.review_parser(userid)
    for review in reviews_list:
        print(f"{review.data} - {review.text}")
    log.info(f"Review parsing completed successful, User ID: {userid}, Mode: ReviewParser(3)")

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

def show_user_reviews(userid):
    reviews = db.get_user_reviews(userid)
    if reviews:
        for review in reviews:
            print(f"\n[{review.date}] Отзыв\n{review.data} - {review.text}")
        print(f"\nВсе отзывы пользователя {userid} отображены")
    log.info(f"Requested user reviews, User ID: {userid}")