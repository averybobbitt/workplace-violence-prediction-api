import datetime
import random
from datetime import time

import numpy


# Generates a single instance of gender data based on the gender distribution
# of staff within hospitals. Gives a 25/75, M/F split.
# Returns a string of either M or F
def generate_gender_data() -> str:
    num = random.random()
    if num >= .75:
        gender = 'M'
    else:
        gender = 'F'
    return gender


# Generates random percentage of beds occupied.
# Default mean and standard deviation comes from CDC dataset
# Returns ndarray or scalar based on number of samples
def generate_inpatient_bed_occupancy_data() -> float:
    mean = 0.721760392289664
    std_dev = 0.08738743450179379
    generator = numpy.random.default_rng()
    inpatient_bed_occupancy = generator.normal(loc=mean, scale=std_dev)
    return inpatient_bed_occupancy


# Generates random number of nurses.
# Mean and standard deviation calculated from ER data from Virtua Marlton
# Returns ndarray or scalar based on number of samples
def generate_number_of_nurses() -> float:
    mean = 5.153
    std_dev = .5652
    generator = numpy.random.default_rng()
    nurses = generator.normal(loc=mean, scale=std_dev)
    return nurses


# Generate daily number of patients.
# Mean and standard deviation calculated from ER data from Virtua Marlton
# Returns ndarray or scalar based on number of samples
def generate_number_of_patients() -> float:
    mean = 66.9516
    std_dev = 6.953
    generator = numpy.random.default_rng()
    patients = generator.normal(loc=mean, scale=std_dev)
    return patients


# Generate random hour and minute
# Returns a time object
def generate_time_of_day() -> time:
    hour = random.randrange(24)
    minute = random.randrange(60)
    time_of_day = datetime.time(hour, minute)
    return time_of_day


# Generates a single entry of sample data
def generate_sample() -> dict:
    # get randomly* generated values
    bed_occupancy = generate_inpatient_bed_occupancy_data()
    nurses = generate_number_of_nurses()
    patients = generate_number_of_patients()
    time_of_day = generate_time_of_day()

    # check for wpv risk
    randNum1 = random.uniform(.75, 1.5)
    randNum2 = random.uniform(.75, 1.5)
    randNum3 = random.uniform(.75, 1.5)
    wpv = (nurses <= (5.153 - randNum1 * .5652) and
           bed_occupancy >= (0.72176 + randNum2 * 0.08739) and
           patients >= (66.9516 + randNum3 * 6.953))

    # construct sample dict
    sample = {
        # pad generated values with f-string formatting
        "avgnurses": f'{nurses:.10f}',
        "avgpatients": f'{patients:.10f}',
        "percentbedsfull": f'{bed_occupancy:.10f}',
        "timeofday": time_of_day.isoformat(),
        "wpvrisk": wpv
    }

    return sample


# Generates sample data then dumps it into a JSON
def generate_bulk_samples(samples=10000) -> list[dict]:
    return [generate_sample() for _ in range(samples)]
