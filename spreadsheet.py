import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

print("Authenticating credentials...")
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)

print("Opening sheet and getting values...")
sheet = client.open("Copy of ORS Global Burden of Disease 2013 (2010/2013)").sheet1
values = sheet.get_all_records()

print("Printing...")
pp = pprint.PrettyPrinter()
pp.pprint(values)
