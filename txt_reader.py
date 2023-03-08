import os

data_dir = 'Admin/Downloads'
txt_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]

for file in txt_files:
    data = {}
    with open(os.path.join(data_dir, file), 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(': ')
            data[line[0]] = line[1]
        print(file)
        print(data)
        print("__________________________________")
