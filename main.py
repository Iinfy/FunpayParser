import ui
import database as db
from logger import log

log.info("FunPay Parser Application started")
db.connect()
db.createParserTable()

if __name__ == "__main__":
    print("\n\n\n\n\nWelcome to FunPay Parser")
    ui.start()



