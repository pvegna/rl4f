import re
import json
import random

with open('cryptic_train.json', 'r') as in_file:
    train = in_file.readlines()

# possibilities: 
# 0->correct
# 1->incorrect selection
# 2->part of selection reoccurs in clue
# 3->empty definition
# 4->meaningful words missing
# 5->words added not present in orginal clue
# 6->words replaced
# 7->non-sequential selection
# 8->definition indicator words included

with open('def_train.json', 'w') as def_file:
    for n,line in enumerate(train):
        print(n)
        ex = json.loads(line)
        defin_txt = ex['definition']
        defin = defin_txt.split()
        words = ex['clue'].split()
        cipher = ex['steps'][1]
        cipher = cipher[:cipher.index(' =')].split()

        # remove length
        if re.match(r'\([0-9,\- ]+\)', words[-1]):
            words = words[:-1]
        
        options = list(range(0, 7))
        if len(cipher) > 2: 
            options.append(7)
        if len(words) > len(cipher) + len(defin):
            options.append(8)
        outcome = random.choice(options)
        selection = []
        excess = []
        feedback = ''

        match outcome:
            case 0:
                selection = defin
                excess = cipher
                feedback = 'The definition is correctly identified.'
            case 1: 
                pivot = random.randint(0, len(cipher)-1)
                if ex['clue'].index(defin_txt) == 0:
                    selection = cipher[-pivot:]
                    excess = defin + cipher[:-pivot]
                else:
                    selection = cipher[:pivot]
                    excess = cipher[pivot:] + defin
                feedback = "The definition is incorrectly identified."
            case 2:
                defin_loc = ex['clue'].index(defin_txt)
                pivot = random.randint(1, 3)
                overlap = []
                if defin_loc == 0:
                    if pivot < len(defin) and random.randint(0, 1):
                        # repeat from definition
                        overlap = defin[-pivot:] 
                        selection = defin
                        excess = overlap + cipher
                    else:
                        # repeat from cipher
                        overlap = cipher[:pivot]
                        selection = defin + overlap
                        excess = cipher
                else:
                    if pivot < len(defin) and random.randint(0, 1):
                        # repeat from definition
                        overlap = defin[:pivot+1]
                        selection = defin
                        excess = cipher + overlap
                    else: 
                        # repeat from cipher
                        overlap = cipher[-pivot:]
                        selection = overlap + defin
                        excess = cipher 
                feedback = f'Each word in the clue can only belong to either the cipher or definition, not both. The phrase "{" ".join(overlap)}" appears in both.'
            case 3:
                selection = ''
                excess = words
                feedback = 'The definition must not be empty.'
            case 4:
                num_missing = random.randint(1, 2)
                selection = defin.copy()
                excess = cipher.copy()
                missing = []
                if random.randint(0, 1) and len(defin) > 1:
                    # take from definition
                    for _ in range(num_missing):
                        if len(selection) > 1:
                            popped = random.choice(selection)
                            selection.remove(popped)
                            missing.append(popped)
                else:
                    # take from cipher
                    for _ in range(num_missing):
                        if len(excess) > 1:
                            popped = random.choice(excess)
                            excess.remove(popped)
                            missing.append(popped)
                if len(missing) == 1:
                    feedback = f'An important word, "{missing[0]}", that should have been included in either the cipher or definition is missing.'
                else:
                    feedback = f'Important words, {missing}, that should have been included in either the cipher or definition are missing.'
            case 5:
                new_word = "$$$"
                selection = defin.copy()
                excess = cipher.copy()
                if random.randint(0, 1):
                    # insert in definition
                    pivot = random.randint(0, len(selection))
                    selection.insert(pivot, new_word)
                else: 
                    # insert in cipher
                    pivot = random.randint(0, len(excess))
                    excess.insert(pivot, new_word)
                feedback = f'The word "{new_word}" was erroneously inserted.'
            case 6:
                new_word = "$$$"
                selection = defin.copy()
                excess = cipher.copy()
                deletion = ''
                if random.randint(0, 1):
                    # replace in definition
                    if len(selection) <= 1:
                        pivot = 0
                    else:
                        pivot = random.randint(0, len(selection) - 1)
                    deletion = selection[pivot]
                    selection[pivot] = new_word
                else: 
                    # insert in cipher
                    pivot = random.randint(0, len(excess) - 1)
                    deletion = excess[pivot]
                    excess[pivot] = new_word
                feedback = f'The word "{deletion}" was erroneously replaced with "{new_word}".'
            case 7:
                defin_loc = ex['clue'].index(defin_txt)
                pivot = random.randint(1, min(3, len(cipher)-2))
                end = random.randint(pivot+1, min(len(cipher)-1, pivot+3))
                if defin_loc == 0: 
                    selection = defin + cipher[pivot:end]
                    excess = cipher[:pivot] + cipher[end:]
                else:
                    selection = cipher[-end:-pivot] + defin
                    excess = cipher[:-end] + cipher[-pivot:]  
                feedback = 'The cipher and definition must both be made up of sequential words.'
            case 8: 
                diff = len(words) - (len(cipher) + len(defin))
                which = ''
                if ex['clue'].index(defin_txt) == 0:
                    indic = words[len(defin):len(defin) + diff]
                    if random.randint(0, 1):
                        # add to defin
                        selection = defin + indic
                        excess = cipher
                        which = 'definition'
                    else:
                        # add to cipher
                        selection = defin
                        excess = indic + cipher
                        which = 'cipher'
                else:
                    indic = words[len(cipher):len(cipher) + diff]
                    if random.randint(0, 1):
                        # add to defin
                        selection = indic + defin
                        excess = cipher
                        which = 'defintion'
                    else:
                        # add to cipher
                        selection = defin
                        excess = cipher + indic
                        which = 'cipher'
                feedback = f'Definition indicator words were erroneously included in the {which}.'
            case _:
                selection = []
                excess = []
                feedback = ''

        output = {'clue': ex['clue'], 
                          'definition_target': defin_txt,
                          'definition_pred': ' '.join(selection),
                          'cipher_target': ' '.join(cipher),
                          'cipher_pred': ' '.join(excess), 
                          'feedback': feedback,
                          'variation': outcome}
        output = json.dumps(output)
        def_file.write(output + '\n')

                

        



