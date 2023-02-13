

with open('names.txt', 'w') as out, open('raw_names.txt', 'r') as f:
    for line in f:
        first_name, last_name = line.split()
        out.write(f'"{first_name}", "{last_name}"\n')
