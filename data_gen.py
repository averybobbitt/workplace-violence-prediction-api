import random
from decimal import Decimal

import numpy as np
import datetime
import json
import requests
import mysql.connector


# Generates a single instance of gender data based on the gender distribution
# of staff within hospitals. Gives a 25/75, M/F split.
# Returns a string of either M or F
def generate_gender_data():
    num = random.random()
    gender = ''
    if num >= .75:
        gender = 'M'
    else:
        gender = 'F'
    return gender


# Generates random percentage of beds occupied.
# Default mean and standard deviation comes from CDC dataset
# Returns ndarray or scalar based on number of samples
def generate_inpatient_bed_occupancy_data(mean=0.721760392289664, stdDev=0.08738743450179379, samples=2):
    generator = np.random.default_rng()
    inpatient_bed_occupancy = generator.normal(loc=mean, scale=stdDev, size=samples)
    return inpatient_bed_occupancy


# Generates random number of nurses.
# Mean and standard deviation calculated from ER data from Virtua Marlton
# Returns ndarray or scalar based on number of samples
def generate_number_of_nurses(mean=5.153, stdDev=.5652, samples=2):
    generator = np.random.default_rng()
    nurses = generator.normal(loc=mean, scale=stdDev, size=samples)
    return nurses


# Generate daily number of patients.
# Mean and standard deviation calculated from ER data from Virtua Marlton
# Returns ndarray or scalar based on number of samples
def generate_number_of_patients(mean=66.9516, stdDev=6.953, samples=2):
    generator = np.random.default_rng()
    patients = generator.normal(loc=mean, scale=stdDev, size=samples)
    return patients


# Generate random hour and minute
# Returns a time object
def generate_time_of_day():
    hour = random.randrange(24)
    minute = random.randrange(60)
    time_of_day = datetime.time(hour, minute)
    return time_of_day


# Generates sample data then dumps it into a JSON
def generate_sample_data(samples=1):
    bedOccupancy = generate_inpatient_bed_occupancy_data(samples=samples)
    nurses = generate_number_of_nurses(samples=samples)
    patients = generate_number_of_patients(samples=samples)
    time_of_day_array = []
    current_time_array = []
    for i in range(samples):
        time_of_day_array.append(generate_time_of_day())
        current_time_array.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    data = []
    for i in range(samples):
        row = [current_time_array[i], nurses[i], patients[i], bedOccupancy[i], time_of_day_array[i]]
        data.append(row)

    dataJSON = []
    for i in range(len(data)):
        row = data[i]
        dict = {
            "createdtime": datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S"),
            "avgnurses": Decimal(row[1]).quantize(Decimal('0.0000000001')),
            "avgpatients": Decimal(row[2]).quantize(Decimal('0.0000000001')),
            "percentbedsfull": Decimal(row[3]).quantize(Decimal('0.0000000001')),
            "timeofday": row[4]
        }
        dataJSON.append(dict)

    return dataJSON
    #file = open("sampleData.json", "w")
    #json.dump(dataJSON, file, default=str)
    #file.close()

def filldatabase(json_file_path, database_config):
    generate_sample_data(10000)
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)

    connection = mysql.connector.connect(**database_config)
    cursor = connection.cursor()

    try:
        for json_object in json_data:
            cursor.execute("""
                    INSERT INTO hospital_data
                    (createdTime, avgNurses, avgPatients, percentBedsFull, timeOfDay) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                json_object["createdTime"],
                json_object["avgNurses"],
                json_object["avgPatients"],
                json_object["percentBedsFull"],
                json_object["timeOfDay"]
            ))

            connection.commit()
        print("Finished inserting data")
    except Exception as e:
            print(f"Error: {e}")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    json_file_path = 'sampleData.json'
    database_config = {
        'host': '73.248.135.215',
        'user': 'joe',
        'password': 'dipiet77',
        'database': 'sweng'
    }
    filldatabase(json_file_path, database_config)
