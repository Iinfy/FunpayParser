import parserprocessor as pp

def start():
    while True:
        mode = int(input("Choose mode(OfferParser) - Enter mode number: "))
        id = input("Enter user id: ")
        if mode == 1:
            isGroupingOn = input("Group offers?(Yes/No): ").strip()
            if isGroupingOn == "Yes":
                pp.startParsing(id,True,mode)
            else:
                pp.startParsing(id,False,mode)   
        else:
            pp.startParsing(id,False,mode) 
                
        
        