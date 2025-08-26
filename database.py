import sqlite3
import hashlib
import re
from parser import Lot, Review
from datetime import datetime
from logger import log

connection :sqlite3.Connection = None
cursor : sqlite3.Cursor = None


class Purchase:
    def __init__(self, userid, desc, amount, price, date):
        self.userid = userid
        self.desc = desc
        self.amount = amount
        self.price = price
        self.date = date

class Action:
    def __init__(self,date,user_id,lot_id,action_type,message):
        self.id = 0
        self.date = date
        self.user_id = user_id
        self.lot_id = lot_id
        self.action_type = action_type
        self.message = message
        
@log.catch(level="ERROR")
def connect():
    global connection
    global cursor
    connection = sqlite3.connect("parser.db")
    cursor = connection.cursor()
    log.info("Database connection opened")

@log.catch(level="ERROR")
def createParserTable():
    global cursor
    global connection
    cursor.execute("CREATE TABLE IF NOT EXISTS parseddata (lot_id BIGINT UNIQUE,"
                   "userid BIGINT,"
                   "desc TEXT,"
                   "amount BIGINT,"
                   "price double,"
                   "checked INT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS parsedreviews (hash TEXT UNIQUE, userid BIGINT, data TEXT, text TEXT, checked INT, date DATETIME)")
    cursor.execute("CREATE TABLE IF NOT EXISTS action_log "
                   "(id INTEGER PRIMARY KEY,"
                   "date DATETIME,"
                   "user_id BIGINT,"
                   "lot_id BIGINT,"
                   "action_type TEXT,"
                   "message TEXT)")
    log.info("Database tables found")
    connection.commit()

@log.catch(level="ERROR")
def add_lot(lot):
    global cursor
    global connection
    price = re.sub(r"[^\d.,]", "", lot.price)
    amount = lot.amount.replace(" ","")
    cursor.execute(f"INSERT INTO parseddata(lot_id,userid,desc,amount,price,checked) VALUES ('{lot.lot_id}', {lot.userid} ,'{lot.desc}',{amount},{price}, 1) ON CONFLICT(lot_id) DO UPDATE SET desc = excluded.desc, amount = excluded.amount, price = excluded.price, checked = 1")
    connection.commit()

def get_lot_by_id(lot_id):
    global cursor
    global connection
    lot = cursor.execute(f"SELECT * FROM parseddata WHERE lot_id = {lot_id}")
    raw_lot = cursor.fetchone()
    if raw_lot:
        lot = Lot(raw_lot[2],raw_lot[3],raw_lot[4],raw_lot[1],raw_lot[0])
        return lot
    else:
        return False

def delete_lot_by_id(lot_id):
    global cursor
    global connection
    cursor.execute(f"DELETE FROM parseddata WHERE lot_id = {lot_id}")
    connection.commit()
    
def uncheckLots(userid):
    global cursor
    global connection
    cursor.execute(f"UPDATE parseddata SET checked = 0 WHERE userid = {userid}")
    connection.commit()
    
def getUncheckedLots(userid):
    global cursor
    global connection
    cursor.execute(f"SELECT * FROM parseddata WHERE userid = {userid} AND checked = 0")
    unchecked_lots_list = []
    raw_lots = cursor.fetchall()
    for offer in raw_lots:
        unchecked_lots_list.append(Lot(offer[2],offer[3],offer[4],offer[1],offer[0]))
    return unchecked_lots_list

@log.catch(level="ERROR")
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

def delete_all_tables():
    global connection
    global cursor
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        cursor.execute(f'DROP TABLE IF EXISTS "{table_name}";')
        log.info(f"Table dropped: {table_name}")
    connection.commit()

def delete_all_lots():
    global connection
    global cursor
    cursor.execute("DELETE FROM parseddata")
    connection.commit()

def delete_all_reviews():
    global connection
    global cursor
    cursor.execute("DELETE FROM parsedreviews")
    connection.commit()

def add_action(action : Action):
    global cursor
    global connection
    cursor.execute("INSERT INTO action_log (date,user_id,lot_id,action_type,message) VALUES (?,?,?,?,?)", (action.date,action.user_id,action.lot_id,action.action_type,action.message))
    connection.commit()

def hash_review(review):
    hash_data = f"{review.data}_{review.text}"
    return  hashlib.sha256(hash_data.encode("utf-8")).hexdigest()