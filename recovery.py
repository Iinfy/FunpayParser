import database as db
from logger import log

@log.catch(level="ERROR", reraise=False)
def recover():
    print("\nRecovery modes\n"
          "1.Reset storages\n"
          "2.Reset settings\n"
          "3.Factory reset\n")
    try:
        mode = int(input("Select recovery mode: "))
        if mode == 1:
            print("\nReset options\n"
                  "1.Reset lots storage\n"
                  "2.Reset reviews storage\n"
                  "3.Reset purchases storage\n")
            reset_option = int(input("Select option: "))
            if reset_option == 1:
                db.delete_all_lots()
            elif reset_option == 2:
                db.delete_all_reviews()
            elif reset_option == 3:
                db.delete_all_purchases()
            else:
                print("\nIncorrect value\n")
        elif mode == 2:
            print("In development")
        elif mode == 3:
            db.delete_all_tables()
    except:
        print("\nIncorrect value\n")


