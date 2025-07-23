import sqlite3
import hashlib
import re
from parser import Lot

connection = None
cursor = None

class LotChanges():
    def __init__(self,desc,amount,price):
        self.desc = desc
        self.amount = amount
        self.price = price
        

def connect():
    global connection
    global cursor
    connection = sqlite3.connect("parser.db")
    cursor = connection.cursor()
    
def createParserTable():
    global cursor
    global connection
    cursor.execute("CREATE TABLE IF NOT EXISTS parseddata (hash TEXT UNIQUE, userid BIGINT, desc TEXT, amount BIGINT, price double, checked INT)")
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
    
    
def uncheckLots(id):
    global cursor
    global connection
    cursor.execute(f"UPDATE parseddata SET checked = 0 WHERE userid = {id}")
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


def hashLotDesc(lot):
    hashdata = f"{lot.desc}_{lot.id}"
    return hashlib.sha256(hashdata.encode("utf-8")).hexdigest()


    
    
    