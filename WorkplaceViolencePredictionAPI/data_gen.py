import random

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

if __name__ == '__main__':
    print("Test data generation")
    maleCount = 0
    for i in range(10000):
        gender = generate_gender_data()
        if gender == 'M':
            maleCount += 1
    print("Total male: " + str(maleCount))
    print("Total female: " + str(10000 - maleCount))