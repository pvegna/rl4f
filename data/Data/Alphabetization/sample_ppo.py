import random

train_sample_size = 606 # size of cryptic train set

with open('train_ppo_large.jsonl', 'r') as in_file:
    data = in_file.readlines()

with open('train_ppo_sampled.jsonl', 'w') as out_file:
    data = random.sample(data, train_sample_size)
    for line in data: 
        out_file.write(line)

test_sample_size = 76 # size of cryptic test set

with open('test_ppo_large.jsonl', 'r') as in_file:
    data = in_file.readlines()

with open('test_ppo_sampled.jsonl', 'w') as out_file:
    data = random.sample(data, test_sample_size)
    for line in data: 
        out_file.write(line)

dev_sample_size = 75 # size of cryptic test set

with open('dev_ppo_large.jsonl', 'r') as in_file:
    data = in_file.readlines()

with open('dev_ppo_sampled.jsonl', 'w') as out_file:
    data = random.sample(data, dev_sample_size)
    for line in data: 
        out_file.write(line)
