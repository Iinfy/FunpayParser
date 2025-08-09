import ui
import database as db
from logger import log
import settings

log.info("\n\nFunPay Parser Application started")
db.connect()
db.createParserTable()

if __name__ == "__main__":
    print("\n\n\n\n\nWelcome to FunPay Parser")
    if settings.check_config_exists():
        settings.import_settings()
    else:
        settings.reset_default_settings()
    ui.start()



