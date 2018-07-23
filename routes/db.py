import sqlite3

def connect_db():
    # print("in connect_db")
    return sqlite3.connect('F:\Projects\GHI\global-health-impact-web-\ghi.db')