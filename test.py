from gspread import Client, Spreadsheet, Worksheet, service_account
from config import table_id


data = ['tinkertwitcher','wqweqwe','1236','123709213','2-3','нет']

def client_init_json() -> Client:
    return service_account(filename='sowiicup-a7b6607dcc6b.json')

if __name__ == '__main__':
    client = client_init_json()
    table = client.open_by_key(table_id)
    print(table)
    title = table.worksheets()[0].title
    worksheet = table.worksheet(title)
    worksheet.append_row(data)