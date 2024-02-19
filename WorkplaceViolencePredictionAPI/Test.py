import sqlite3
import json

#Making up dummy data to test the pulling of data from sqlite database, validation, and parsing into JSON file.
#Purely for testing purposes
connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()
test_query = '''CREATE TABLE IF NOT EXISTS hospData
                (PID INTEGER PRIMARY KEY AUTOINCREMENT,
                    TIMESTAMP DOUBLE,
                    INVENTORY INT)'''
cursor.execute(test_query)
test_query = "INSERT INTO hospData (Timestamp, Inventory) VALUES (1028.1738,21)"
cursor.execute(test_query)
connection.commit()
connection.close()
#end of making dummy data


#validation and parsing most recent timestamp entry into JSON
def extract_to_json(db_path, table_name):
    #connect to database
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    #select most recent database entry
    query = f'SELECT Timestamp, Inventory FROM "{table_name}" ORDER BY PID DESC LIMIT 1'
    cursor.execute(query)
    row = cursor.fetchone()

    #data validation
    if row is not None:
        timestamp, inventory = row
        row_dict = {'Timestamp': timestamp, 'Inventory': inventory}
        json_file_path = 'input.json'
        with open(json_file_path, 'w') as json_file:
            json.dump(row_dict, json_file, indent=2)

        print(f'Saved output to {json_file_path}')
    else:
        print('No data')
        #return None

#test
extract_to_json('db.sqlite3', 'hospData')