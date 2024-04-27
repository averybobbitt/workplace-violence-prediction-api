import datetime
import random
from datetime import time

import numpy
from imblearn.over_sampling import SMOTE


def generate_gender_data() -> str:
    """
    Generates a single instance of gender data based on the gender distribution
    of staff within hospitals. Gives a 25/75, M/F split.

    Returns:
        str: A string representing gender, either "M" or "F".
    """
    num = random.random()
    if num >= 0.75:
        gender = "M"
    else:
        gender = "F"
    return gender


def generate_inpatient_bed_occupancy_data() -> float:
    """
    Generates random percentage of beds occupied.
    Default mean and standard deviation comes from CDC dataset.

    Returns:
        float: Random percentage of beds occupied.
    """
    mean = 0.721760392289664
    std_dev = 0.08738743450179379
    generator = numpy.random.default_rng()
    inpatient_bed_occupancy = generator.normal(loc=mean, scale=std_dev)
    return inpatient_bed_occupancy


def generate_number_of_nurses() -> float:
    """
    Generates a random number of nurses.
    Mean and standard deviation calculated from ER data from Virtua Marlton.

    Returns:
        float: Random number of nurses.
    """
    mean = 5.153
    std_dev = 0.5652
    generator = numpy.random.default_rng()
    nurses = generator.normal(loc=mean, scale=std_dev)
    return nurses


def generate_number_of_patients() -> float:
    """
    Generates daily number of patients.
    Mean and standard deviation calculated from ER data from Virtua Marlton.

    Returns:
        float: Daily number of patients.
    """
    mean = 66.9516
    std_dev = 6.953
    generator = numpy.random.default_rng()
    patients = generator.normal(loc=mean, scale=std_dev)
    return patients


def generate_time_of_day() -> time:
    """
    Generates a random hour and minute.

    Returns:
        time: A time object representing the generated time.
    """
    hour = random.randrange(24)
    minute = random.randrange(60)
    time_of_day = datetime.time(hour, minute)
    return time_of_day


def generate_sample() -> dict:
    """
    Generates a single entry of sample data.

    Returns:
        dict: A dictionary containing generated sample data.
    """
    bed_occupancy = generate_inpatient_bed_occupancy_data()
    nurses = generate_number_of_nurses()
    patients = generate_number_of_patients()
    time_of_day = generate_time_of_day()

    randNum1 = random.uniform(0.75, 1.5)
    randNum2 = random.uniform(0.75, 1.5)
    randNum3 = random.uniform(0.75, 1.5)
    wpv = (nurses <= (5.153 - randNum1 * 0.5652)
           and bed_occupancy >= (0.72176 + randNum2 * 0.08739)
           and patients >= (66.9516 + randNum3 * 6.953))

    sample = {
        "avgNurses": f"{nurses:.10f}",
        "avgPatients": f"{patients:.10f}",
        "percentBedsFull": f"{bed_occupancy:.10f}",
        "timeOfDay": time_of_day.isoformat(),
        "wpvRisk": wpv
    }
    return sample


def generate_bulk_samples(samples=10000) -> list[dict]:
    """
    Generates sample data and dumps it into a JSON format.

    Args:
        samples (int): Number of samples to generate. Default is 10,000.

    Returns:
        list[dict]: A list of dictionaries containing generated sample data.
    """
    return [generate_sample() for _ in range(samples)]


def generate_training_data(samples=10000, smotePercentage=.25) -> list[dict]:
    """
    Generates training data for machine learning models.

    Args:
        samples (int): Number of samples to generate. Default is 10,000.
        smotePercentage (float): Percentage of SMOTE oversampling to apply. Default is 0.25.

    Returns:
        list[dict]: A list of dictionaries containing generated training data.
    """
    data = []
    dataClass = []

    for i in range(samples):
        bed_occupancy = generate_inpatient_bed_occupancy_data()
        nurses = generate_number_of_nurses()
        patients = generate_number_of_patients()

        randNum1 = random.uniform(0.75, 1.5)
        randNum2 = random.uniform(0.75, 1.5)
        randNum3 = random.uniform(0.75, 1.5)
        wpv = (nurses <= (5.153 - randNum1 * 0.5652)
               and bed_occupancy >= (0.72176 + randNum2 * 0.08739)
               and patients >= (66.9516 + randNum3 * 6.953))

        data.append([nurses, patients, bed_occupancy])
        dataClass.append(wpv)

    data_smote, class_smote = SMOTE(sampling_strategy=smotePercentage).fit_resample(data, dataClass)
    dictList = []
    for i in range(len(data_smote)):
        sample = {
            "avgNurses": f"{data_smote[i][0]:.10f}",
            "avgPatients": f"{data_smote[i][1]:.10f}",
            "percentBedsFull": f"{data_smote[i][2]:.10f}",
            "timeOfDay": generate_time_of_day().isoformat(),
            "wpvRisk": class_smote[i]
        }
        dictList.append(sample)

    return dictList


def generate_wpv_sample():
    """
    Generates a sample with Workplace Violence (WPV) risk.

    Returns:
        dict: A dictionary containing generated sample data with WPV risk.
    """
    time_of_day = generate_time_of_day()
    randNum1 = random.uniform(0.75, 1.5)
    randNum2 = random.uniform(0.75, 1.5)
    randNum3 = random.uniform(0.75, 1.5)
    nurses = (5.153 - randNum1 * 0.5652)
    bed_occupancy = (0.72176 + randNum2 * 0.08739)
    patients = (66.9516 + randNum3 * 6.953)
    wpv = 1
    sample = {
        "avgNurses": f"{nurses:.10f}",
        "avgPatients": f"{patients:.10f}",
        "percentBedsFull": f"{bed_occupancy:.10f}",
        "timeOfDay": time_of_day.isoformat(),
        "wpvRisk": wpv
    }
    return sample
