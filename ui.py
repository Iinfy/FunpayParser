import parserprocessor as pp
from logger import log
import recovery as rc

@log.catch(level="CRITICAL", reraise=False)
def start():
    continue_with_current_speed = None
    log.info("UI started successful")
    while True:
        print("\nParser menu\n"
              "1.Parser\n"
              "2.Settings\n"
              "3.Recovery\n"
              "4.Exit")
        try:
            menu_mode = input("\nSelect menu mode: ")
            if menu_mode.lower() == "exit":
                break
            if int(menu_mode) == 1:
                mode = int(input("Choose mode(OfferParser) - Enter mode number: "))
                userid = input("Enter user id: ")
                parsing_frequency = float(input("Enter parsing frequency: "))
                if parsing_frequency < 5:
                    print("Parsing frequency lower than 5 seconds may occur problems")
                    continue_with_current_speed = input("Continue? (Y/n): ")
                if continue_with_current_speed.lower() == "y":
                    log.info(
                        f"Settings received, Mode: {mode}, User ID: {userid}, Parsing frequency: {parsing_frequency}")
                    log.warning(f"Parsing frequency lower than 5s, this may occur problems")
                    if mode == 1:
                        isGroupingOn = input("Group offers?(Yes/No): ").strip()
                        if isGroupingOn == "Yes":
                            pp.startParsing(userid, True, mode, parsing_frequency)
                    else:
                        pp.startParsing(userid, False, mode, parsing_frequency)
                else:
                    continue
            elif int(menu_mode) == 2:
                continue
            elif int(menu_mode) == 3:
                rc.recover()
            elif int(menu_mode) == 4:
                break
        except:
            print("\nIncorrect value\n")

        