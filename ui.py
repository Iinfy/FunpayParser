import parserprocessor as pp
from logger import log

@log.catch(level="CRITICAL")
def start():
    log.info("UI started successful")
    while True:
        mode = int(input("Choose mode(OfferParser) - Enter mode number: "))
        id = input("Enter user id: ")
        parsing_frequency = int(input("Enter parsing frequency: "))
        if mode == 1:
            isGroupingOn = input("Group offers?(Yes/No): ").strip()
            if isGroupingOn == "Yes":
                pp.startParsing(id,True,mode,parsing_frequency)
        else:
            pp.startParsing(id,False,mode,parsing_frequency)
                
        
        