import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("E:\KGB PROJECTS\KGB_Golem\Floria\code\Credentials.json", scope)


gclient = gspread.authorize(credentials)
CONFIG_SOURCE = gclient.open("Monopoly_config")
mono_config = CONFIG_SOURCE.get_worksheet(2)


board = []

with open("monopoly_props.json") as source:
    data = json.load(source)
    
properties_list = data["Properties"]

for prop in properties_list.values():
    board.append(prop)

row_ref = 1
col_ref = 1


def port_to_sheets(row_ref, col_ref, mono_config, board):
    for item in board:
        print(item)
        sleep(15)
        row_ref = item["Position"]
        mono_config.update_cell(row_ref, col_ref, "Position")
        col_ref += 1
        mono_config.update_cell(row_ref, col_ref, item["Position"])
        col_ref += 1
        mono_config.update_cell(row_ref, col_ref, "Group")
        col_ref += 1
        mono_config.update_cell(row_ref, col_ref, item["Group"])
        col_ref += 1
        mono_config.update_cell(row_ref, col_ref, "Name")
        col_ref += 1
        mono_config.update_cell(row_ref, col_ref, item["Name"])
        col_ref += 1
        mono_config.update_cell(row_ref, col_ref, "Price")
        col_ref += 1
        mono_config.update_cell(row_ref, col_ref, item["Price"])
        col_ref += 1
        mono_config.update_cell(row_ref, col_ref, "Rent")
        col_ref += 1
        mono_config.update_cell(row_ref, col_ref, item["Rent"])
        col_ref += 1
        if item["Group"] == "Railroad":
            mono_config.update_cell(row_ref, col_ref, "2 owned")
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, item["2 owned"])
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, "3 owned")
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, item["3 owned"])
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, "4 owned")
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, item["4 owned"])
            col_ref = 1
        elif item["Group"] == "Utilities":
            mono_config.update_cell(row_ref, col_ref, "Both owned")
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, item["Both owned"])
            col_ref = 1
        else:
            mono_config.update_cell(row_ref, col_ref, "1 House")
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, item["1 House"])
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, "2 Houses")
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, item["2 Houses"])
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, "3 Houses")
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, item["3 Houses"])
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, "4 Houses")
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, item["4 Houses"])
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, "Hotel")
            col_ref += 1
            mono_config.update_cell(row_ref, col_ref, item["Hotel"])
            col_ref = 1


def main():
    port_to_sheets(row_ref, col_ref, mono_config, board)
    return True

main()

 
# for position in board:
#     print("Name: ", position["Name"])
#     print("Position: ", position["Position"])
#     print("Group: ", position["Group"])
#     print("Price: ", position["Price"])
#     print("Rent: ", position["Rent"])
#     if position["Group"] == "Railroad":
#         print("2 owned: ", position["2 owned"])
#         print("3 owned: ", position["3 owned"])
#         print("4 owned: ", position["4 owned"])
#     elif position["Group"] == "Utilities":
#         print("Both owned: ", position["Both owned"])
#     else:
#         print("1 House: ", position["1 House"])
#         print("2 Houses: ", position["2 Houses"])
#         print("3 Houses: ", position["3 Houses"])
#         print("4 Houses: ", position["4 Houses"])
#         print("Hotel: ", position["Hotel"])
