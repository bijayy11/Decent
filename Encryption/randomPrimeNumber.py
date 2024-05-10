import csv
import random

def pick_random_number(nums):
    return random.choice(nums) # returns a random prime number

def read_num_from_csv(file_path):  # reads prime numbers from a csv file
    Primenums = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            num = int(row['Num'])
            Primenums.append(num)
    return Primenums

file_path = './prime_numbers/1m.csv'
Primenums = read_num_from_csv(file_path)
primenumber1=pick_random_number(Primenums)
primenumber2=pick_random_number(Primenums)
print(primenumber1)
print(primenumber2)