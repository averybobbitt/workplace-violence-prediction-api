"""
Connects to a database.
"""

import mysql.connector

mydb = mysql.connector.connect(
  host="elvis.rowan.edu",
  user="ungant67",
  password="1Brokentooth!"
)


def main():
    print(mydb)
