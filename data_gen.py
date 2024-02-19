import random
import numpy as np
from numpy.random import Generator

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
    randomNum = Generator.normal(mean, stdDev, samples)
    return randomNum

if __name__ == '__main__':
    print("Test data generation")
    maleCount = 0
    for i in range(10000):
        gender = generate_gender_data()
        if gender == 'M':
            maleCount += 1
    print("Total male: " + str(maleCount))
    print("Total female: " + str(10000 - maleCount))