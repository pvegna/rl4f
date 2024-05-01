import random

train_sample_size = 606 * 4 # size of cryptic train set * 4

with open('train_sup_large.jsonl', 'r') as in_file:
    data = in_file.readlines()

with open('train_sup.jsonl', 'w') as out_file:
    data = random.sample(data, train_sample_size)
    for line in data: 
        out_file.write(line)

test_sample_size = 76 * 4 # size of cryptic test set * 4

with open('test_sup_large.jsonl', 'r') as in_file:
    data = in_file.readlines()

with open('test_sup.jsonl', 'w') as out_file:
    data = random.sample(data, test_sample_size)
    for line in data: 
        out_file.write(line)

dev_sample_size = 75 * 4 # size of cryptic test set * 4

with open('dev_sup_large.jsonl', 'r') as in_file:
    data = in_file.readlines()

with open('dev_sup.jsonl', 'w') as out_file:
    data = random.sample(data, dev_sample_size)
    for line in data: 
        out_file.write(line)
