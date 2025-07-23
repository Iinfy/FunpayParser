import ui
import database as db

db.connect()
db.createParserTable()
    
if __name__ == "__main__":
    ui.start()



