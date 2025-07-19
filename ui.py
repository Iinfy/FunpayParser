import parser

def start():
    while True:
        id = input("Enter user id: ")
        list = parser.offerParser(id)
        for offerClass in list:
            print(offerClass.listName)
            for lot in offerClass.offers:
                print(f"{lot.desc} {f"{lot.amount}шт" if lot.amount != 0 else ""} {lot.price}".strip())
        
        