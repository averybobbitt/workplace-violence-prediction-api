"""
Connects to a database.
"""

import mysql.connector

mydb = mysql.connector.connect(
  host="73.248.135.215",
  port="3306",
  user="anthony",
  password="ungant67"
)


def main():
    print(mydb)
