def partition_metric(pred, ref, clue):
    '''print(pred)
    print(ref)
    print(clue)'''
    true_positives = 0
    false_negatives = 0
    false_positives = 0
    insertions = 0
    num_ref = 0
    num_pred = 0
    for p, r in zip(pred, ref):
        for rw in r.split(' '):
            num_ref += 1
            if rw in p:
                true_positives += 1
            else:
                false_negatives += 1
        for pw in p.split(' '):
            num_pred += 1
            if pw not in r:
              false_positives += 1
              if pw not in clue:
                  insertions += 1

    complete = num_ref == num_pred and insertions == 0
    sequential = True
    for p in pred:
        sequential = sequential and (p in clue)
    exact_partition = 1 if sequential and insertions == 0 and false_negatives == 0 else 0

    '''print("tp: " + str(true_positives))
    print("fn: " + str(false_negatives))
    print("fo: " + str(false_positives))
    print("ins: " + str(insertions))
    print("cmplt: " + str(complete))
    print("seq: " + str(sequential))
    print("exact: " + str(exact_partition))'''
    
    reward = true_positives - false_negatives - false_positives - insertions + complete + sequential + exact_partition
    return reward, exact_partition

with open("sup_test_edits.json", 'r') as edit_file:
    edited = edit_file.read()

import json, re, string
edited = json.loads(edited)["edits"]

with open("data/Data/Definition/test_ppo_sampled.jsonl", 'r') as ref_file:
    refs = ref_file.readlines()

rewards = 0
exacts = 0
exact_rewards = 0
bad_rewards = 0
for edit, ref in zip(edited, refs):
    ref = json.loads(ref)
    search_str = "Definition:(.*)Cipher:(.*)"
    pred_parts = re.match(search_str, edit).group(1, 2)
    ref_parts = re.match(search_str, ref["summary"]).group(1, 2)
  
    pred_parts = [p.strip().lower().translate(str.maketrans('', '', string.punctuation)) for p in pred_parts]
    ref_parts = [r.strip().lower().translate(str.maketrans('', '', string.punctuation)) for r in ref_parts]
    
    search_str = "(.*)\|\|\|"
    clue = re.search(search_str, ref["text"]).group(1)
    clue = clue.strip().lower().translate(str.maketrans('', '', string.punctuation))
    reward, exact = partition_metric(pred_parts, ref_parts, clue)
    rewards+=reward
    exacts+=exact
    exact_rewards += reward if exact else 0
    bad_rewards += 0 if exact else reward
print("avg reward: " + str(rewards / len(edited)))
print("exact : " + str(exacts / len(edited)))
print("avg reward of exact: " + str(exact_rewards/exacts))
print("avg reward of non-exact: " + str(bad_rewards/(len(edited) - exacts)))