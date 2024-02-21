import random
import numpy as np
from numpy.random import Generator
import datetime

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
def generate_inpatient_bed_occupancy_data(mean=0.721760392289664, stdDev=0.08738743450179379, samples=1):
    inpatient_bed_occupancy = Generator.normal(mean, stdDev, samples)
    return inpatient_bed_occupancy

def generate_number_of_nurses(mean=5.153, stdDev=.5652, samples=1):
    nurses = Generator.normal(mean, stdDev, samples)
    return nurses

def generate_number_of_patients(mean=66.9516, stdDev=6.953, samples=1):
    patients = Generator.normal(mean, stdDev, samples)
    return patients

def generate_time_of_day():
    hour = random.randrange(24)
    minute = random.randrange(60)
    time_of_day = datetime.time(hour, minute)
    return time_of_day


if __name__ == '__main__':
    print("Test data generation")
    maleCount = 0
    for i in range(10000):
        gender = generate_gender_data()
        if gender == 'M':
            maleCount += 1
    print("Total male: " + str(maleCount))
    print("Total female: " + str(10000 - maleCount))