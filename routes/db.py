import sqlite3

def connect_db():
    # print("in connect_db")
    return sqlite3.connect('F:\Projects\GHI\GHI_main\global-health-impact-web-\ghi.db')