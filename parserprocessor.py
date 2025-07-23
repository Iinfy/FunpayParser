import parser
import database as db
from multiprocessing import Process
import time
from datetime import datetime

def startParsing(id,isGroupingOn,mode):
    if mode == 1:
        parseThread = Process(target=parseAndShowUserOffers, args=(id,isGroupingOn))
        parseThread.start()
        while True:
            toStop = input("Enter 'e' to stop parsing ")
            if toStop == "e":
                parseThread.terminate()
                break
    if mode == 2:
        parseThread = Process(target=parseAndShowChanges, args=(id,))
        parseThread.start()
        while True:
            toStop = input("Enter 'e' to stop parsing ")
            if toStop == "e":
                parseThread.terminate()
                break
        
        
def parseLotsIntoDataBase(id):
    list = parser.offerParser(id,False)
    for lot in list:
        db.addLot(lot)

def parseAndShowUserOffers(id,isGroupingOn):
    while True:
        time.sleep(1)
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
            
def parseAndShowChanges(id):
    while True:
        currentTime = datetime.now().time().strftime("%H:%M:%S")
        time.sleep(15)
        db.uncheckLots(id)
        list = parser.offerParser(id,False)
        for lot in list:
            try:
                oldLot = db.getLotByHash(db.hashLotDesc(lot))
            except:
                db.addLot(lot)
            if oldLot:
                old_amount = int(oldLot.amount)
                new_amount = int((lot.amount).replace(" ", "").strip())
                if new_amount < old_amount:
                    print(f"\n[{currentTime}] Совершена покупка \n{lot.desc}\n{old_amount} -> {new_amount}({old_amount - new_amount})\nСумма покупки: {(old_amount - new_amount)*oldLot.price}р")
                elif new_amount > old_amount:
                    print(f"\n[{currentTime}] Лот пополнен\n{lot.desc}\n{old_amount} -> {new_amount}")
            elif not oldLot:
                print(f"\n[{currentTime}] Обнаружен новый лот\n{lot.desc}\nКол-во: {lot.amount}\nЦена: {str(lot.price).strip()}")
            db.addLot(lot)
        for lot in db.getUncheckedLots(id):
            print(f"\n[{currentTime}] Лот был выкуплен или удален\n{lot.desc}\nЦена: {lot.price}р")
            db.deleteLotByHash(db.hashLotDesc(lot))
