import random
import numpy as np
import datetime
import json

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
def generate_inpatient_bed_occupancy_data(mean=0.72176, stdDev=0.08739, samples=2):
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
def generate_sample_data(samples=2):
    bedOccupancy = generate_inpatient_bed_occupancy_data(samples=samples)
    nurses = generate_number_of_nurses(samples=samples)
    patients = generate_number_of_patients(samples=samples)
    time_of_day_array = []
    current_time_array = []
    WPV_array = []
    for i in range(samples):
        time_of_day_array.append(generate_time_of_day())
        current_time_array.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        wpv = 0
        randNum1 = random.uniform(.75, 1.5)
        randNum2 = random.uniform(.75, 1.5)
        randNum3 = random.uniform(.75, 1.5)
        if nurses[i] <= (5.153 - randNum1 * .5652) and bedOccupancy[i] >= (0.72176 + randNum2 * 0.08739) and patients[i] >= (66.9516 + randNum3 * 6.953):
            wpv = 1
        WPV_array.append(wpv)

    data = []
    for i in range(samples):
        row = [current_time_array[i], nurses[i], patients[i], bedOccupancy[i], time_of_day_array[i], WPV_array[i]]
        data.append(row)

    dataJSON = []
    for i in range(len(data)):
        row = data[i]
        dict = {
            "createdTime" : row[0],
            "avgNurses" : row[1],
            "avgPatients" : row[2],
            "percentBedsFull" : row[3],
            "timeOfDay" : row[4],
            "workplaceViolence" : row[5]
        }
        dataJSON.append(dict)

    jsonData = json.dumps(dataJSON, default=str)
    return jsonData



if __name__ == '__main__':
    data = generate_sample_data(samples=100000)
    WPVNum = 0
    for i in range(len(data)):
        if data[i][5] == 1:
            WPVNum += 1

    print(WPVNum)