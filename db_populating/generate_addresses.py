import datetime
import random


countries = {
    'USA': ['California', 'Boston', 'Los Angeles'],
    'UK': ['London', 'Oxford'],
    'France': ['Paris', 'Lyon', 'Marseille'],
    'Germany': ['Berlin', 'Cologne'],
    'Kanada': ['Toronto'],
    'Sweden': ['Stockholm'],
    'Finland': ['Helsinki'],
    'Denmark': ['Copenhagen'],
    'Netherlands': ['Amsterdam'],
}

streets = []

with open('raw_streets.txt', 'r') as f:
    for i in f:
        streets.append(" ".join(i.split()[1:]))

streets.sort()

# filename = 'address_' + str(datetime.datetime.today()).replace(' ', '_').replace(':', '_') + '.txt'
filename = 'addresses.txt'
with open(filename, 'w') as out:
    for country in countries:
        for city in countries[country]:
            for j in range(random.randint(2, 5)):
                cur = f'("{country}", "{city}", "{streets.pop()}", {random.randint(1, 150)})\n'
                out.write(cur)

