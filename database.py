import sqlite3
import hashlib
import re
from parser import Lot, Review
from datetime import datetime

connection :sqlite3.Connection = None
cursor : sqlite3.Cursor = None


class Purchase:
    def __init__(self, userid, desc, amount, price, date):
        self.userid = userid
        self.desc = desc
        self.amount = amount
        self.price = price
        self.date = date
        

def connect():
    global connection
    global cursor
    connection = sqlite3.connect("parser.db")
    cursor = connection.cursor()
    
def createParserTable():
    global cursor
    global connection
    cursor.execute("CREATE TABLE IF NOT EXISTS parseddata (hash TEXT UNIQUE, userid BIGINT, desc TEXT, amount BIGINT, price double, checked INT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS parsedreviews (hash TEXT UNIQUE, userid BIGINT, data TEXT, text TEXT, checked INT, date DATETIME)")
    cursor.execute("CREATE TABLE IF NOT EXISTS purchases (userid BIGINT, desc TEXT, amount BIGINT, price double, date DATETIME)")
    connection.commit()
    
def addLot(lot):
    global cursor
    global connection
    price = re.sub(r"[^\d.,]", "", lot.price)
    amount = lot.amount.replace(" ","")
    cursor.execute(f"INSERT INTO parseddata(hash,userid,desc,amount,price,checked) VALUES ('{hashLotDesc(lot)}', {lot.id} ,'{lot.desc}',{amount},{price}, 1) ON CONFLICT(hash) DO UPDATE SET desc = excluded.desc, amount = excluded.amount, price = excluded.price, checked = 1")
    connection.commit()
    
def getLotByHash(hash):
    global cursor
    global connection
    result = cursor.execute(f"SELECT * FROM parseddata WHERE hash = '{hash}'")
    rawLot = cursor.fetchone()
    if rawLot:
        lot = Lot(rawLot[2],rawLot[3],rawLot[4],rawLot[1])
        return lot
    else:
        return False
    
def uncheckLots(userid):
    global cursor
    global connection
    cursor.execute(f"UPDATE parseddata SET checked = 0 WHERE userid = {userid}")
    connection.commit()
    
def getUncheckedLots(id):
    global cursor
    global connection
    cursor.execute(f"SELECT * FROM parseddata WHERE userid = {id} AND checked = 0")
    uncheckedList = []
    uncheckedOffers = cursor.fetchall()
    for offer in uncheckedOffers:
        uncheckedList.append(Lot(offer[2],offer[3],offer[4],offer[1]))
    return uncheckedList

def deleteLotByHash(hash):
    global cursor
    global connection
    cursor.execute(f"DELETE FROM parseddata WHERE hash = '{hash}'")
    connection.commit()

def add_review(review):
    global connection
    global cursor
    userid = review.userid
    data = review.data
    text = review.text
    cursor.execute(f"INSERT INTO parsedreviews(hash,userid,data,text,checked, date) VALUES ('{hash_review(review)}',{userid},'{data}','{text}', 1, '{review.date}') ON CONFLICT(hash) DO UPDATE SET data = excluded.data, text = excluded.text, checked = 1")
    connection.commit()

def get_review_by_hash(hash):
    global cursor
    global connection
    result = cursor.execute(f"SELECT * FROM parsedreviews WHERE hash = '{hash}'")
    rawLot = cursor.fetchone()
    if rawLot:
        review = Review(rawLot[1],rawLot[2],rawLot[3],datetime.now())
        return review
    else:
        return False

def uncheck_reviews_by_userid(userid):
    global cursor
    global connection
    cursor.execute(f"UPDATE parsedreviews SET checked = 0 WHERE userid = {userid}")
    connection.commit()

def get_unchecked_reviews_by_userid(userid):
    global cursor
    global connection
    cursor.execute(f"SELECT * FROM parsedreviews WHERE userid = {userid} AND checked = 0")
    unchecked_reviews = []
    reviews_list = cursor.fetchall()
    for review in reviews_list:
        unchecked_reviews.append(Review(review[1],review[2],review[3],datetime.now()))
    return unchecked_reviews

def delete_review_by_hash(hash):
    global cursor
    global connection
    cursor.execute(f"DELETE FROM parsedreviews WHERE hash = '{hash}'")
    connection.commit()

def get_user_reviews(userid):
    global cursor
    global connection
    cursor.execute("SELECT * FROM parsedreviews WHERE userid = ?",(userid,))
    raw_data = cursor.fetchall()
    reviews = []
    for review in raw_data:
        reviews.append(Review(userid,review[2],review[3],review[5]))
    return reviews


def add_purchase(purchase):
    global cursor
    global connection
    price = re.sub(r"[^\d.,]", "", purchase.price)
    print(f"{purchase.userid}, '{purchase.desc}', {purchase.amount}, {price}, {purchase.date})")
    cursor.execute(f"INSERT INTO purchases (userid, desc, amount, price, date) VALUES ({purchase.userid}, '{purchase.desc}', {purchase.amount}, {price}, '{purchase.date}')")
    connection.commit()

def get_user_purchases(userid):
    global cursor
    global connection
    cursor.execute("SELECT * FROM purchases WHERE userid = ?",(userid,))
    raw_data = cursor.fetchall()
    purchases = []
    for purchase in raw_data:
        purchases.append(Purchase(userid,purchase[1],purchase[2],purchase[3],purchase[4]))
    return purchases


def hashLotDesc(lot):
    hash_data = f"{lot.desc}_{lot.id}"
    return hashlib.sha256(hash_data.encode("utf-8")).hexdigest()

def hash_review(review):
    hash_data = f"{review.data}_{review.text}"
    return  hashlib.sha256(hash_data.encode("utf-8")).hexdigest()


    
    
    