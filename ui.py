import parserprocessor as pp
from logger import log

@log.catch(level="CRITICAL")
def start():
    log.info("UI started successful")
    while True:
        mode = int(input("Choose mode(OfferParser) - Enter mode number: "))
        userid = input("Enter user id: ")
        parsing_frequency = float(input("Enter parsing frequency: "))
        log.info(f"Settings received, Mode: {mode}, User ID: {userid}, Parsing frequency: {parsing_frequency}")
        if mode == 1:
            isGroupingOn = input("Group offers?(Yes/No): ").strip()
            if isGroupingOn == "Yes":
                pp.startParsing(userid,True,mode,parsing_frequency)
        else:
            pp.startParsing(userid,False,mode,parsing_frequency)
                
        
        