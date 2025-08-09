import parserprocessor as pp
from logger import log
import recovery as rc
import settings
import config as cfg

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
                userid = input("Enter user id: ")
                mode = cfg.parser_settings["parsing_mode"]
                parsing_frequency = cfg.parser_settings["parsing_frequency"]
                if parsing_frequency < 5:
                    print("Parsing frequency lower than 5 seconds may occur problems")
                    continue_with_current_speed = input("Continue? (Y/n): ")
                else:
                    continue_with_current_speed = "n"
                if continue_with_current_speed.lower() == "y" or parsing_frequency >= 5:
                    log.info(
                        f"Settings received, Mode: {mode}, User ID: {userid}, Parsing frequency: {parsing_frequency}")
                    if parsing_frequency < 5:
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
                print(f"Current settings\n\n"
                      f"1.Parsing mode: {cfg.parser_settings["parsing_mode"]}\n"
                      f"2.Parsing frequency: {cfg.parser_settings["parsing_frequency"]}\n")
                option = input("Select parameter for edit or press ENTER for exit settings: ")
                if option == "":
                    continue
                elif int(option) == 1:
                    print("\nParsing modes\n"
                          "1.Single lot parser\n"
                          "2.Lot parser and comparator\n"
                          "3.Single review parser\n"
                          "4.Review parser and comparator\n")
                    new_value = input("\nSelect parsing mode: ")
                    cfg.parser_settings["parsing_mode"] = int(new_value)
                    settings.export_settings()
                elif int(option) == 2:
                    new_value = input("\nEnter parsing frequency in seconds: ")
                    cfg.parser_settings["parsing_frequency"] = float(new_value)
                    settings.export_settings()
            elif int(menu_mode) == 3:
                rc.recover()
            elif int(menu_mode) == 4:
                break
        except Exception as ex:
            print("\nIncorrect value\n")
            log.warning(ex)

        