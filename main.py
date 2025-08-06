import ui
import database as db
from logger import log

db.connect()
db.createParserTable()
log.info("FunPay Parser Application started")
    
if __name__ == "__main__":
    ui.start()



