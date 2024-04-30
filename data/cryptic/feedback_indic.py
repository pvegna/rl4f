import re
import json
import random

with open('cryptic_train.json', 'r') as in_file:
    train = in_file.readlines()

# possibilities: 
# 0->correct
# 1->indicator phrases incorrect
# 2->correct indicator, wrong wordplay type.
# 3->no indics identified
# 4->wordplay without indic
# 5->indic without wordplay
# 6->additional indicators to identify

with open('indic_train.json', 'w') as def_file:
    for n,line in enumerate(train):
        print(n)
        ex = json.loads(line)
        cipher = ex['steps'][1]
        cipher = cipher[:cipher.rindex(' =')].split()
        i_cipher = ex['steps'][1+len(ex['indicators'])]
        i_cipher = i_cipher[:i_cipher.rindex(' =')].split()
        indics = ex['indicators']
        types = ['anagram', 'reversal', 'container', 'deletion', 'combination', 
                 'alternation', 'homophone', 'hidden', 'acronym']
        # punctuation might be an issue w this method
        indic_locs = [i_cipher.index('(' + indic[0].split()[0]) for indic in indics]
        indic_lens = [len(indic.split()) for indic in indics]
        
        

        options = [0, 1]
        if len(indics) >= 1:
            options.extend([2, 3, 4, 5])
        if len(indics) >= 2:
            options.append(6)

        selection = []
        feedback = ''

        outcome = random.choice(options)
        match outcome:
            case 0:
                selection = cipher
                feedback = 'The indicators are correctly identified.'
            case 1:
                og_locs = [cipher.index('(' + indic[0].split()[0]) for indic in indics]
                indic_mask = [1] * len(cipher)
                for i in range(len(indic_locs)):
                    indic_mask[og_locs[i]:og_locs[i]+indic_lens[i]] = 0
                num_right = random.randint(1, len(indics) - 1)
                num_wrong = len(indics) - num_right
                
            case 2:
                num_wrong = random.randint(1, len(indics))
                wrong_indics = random.sample(indics, num_wrong)
                wrong_wps = [types.index([indic[1]]) for indic in indics]
                shifts = [random.randint(1, 8)]
                selection = i_cipher.copy()
                feedback = ''
                for i in range(len(wrong_indics)):
                    indic_num = wrong_indics[i]
                    loc = indic_locs[indic_num]
                    length = indic_lens[indic_num]
                    new_wp = types[(wrong_wps[i] + shifts[i]) % 9]
                    selection[loc + length + 1] = new_wp
                    feedback += f'"{new_wp}" is not the correct wordplay type for the indicator phrase "{indics[indic_num][0]}". '
            case 3:
                selection = cipher.copy()
                feedback = 'There should be indicators identified, and there are none.'
            case 4:
                wp = random.choice(types)
                selection = i_cipher.copy()
                loc = random.randint(0, len(indic_locs)-1)
                selection[indic_locs[loc] + indic_lens[loc] + 1] = wp + ')'
                feedback = 'Each wordplay selection must correspond to an indicator phrase from the cipher.'
            case 5:
                selection = i_cipher.copy()
                loc = random.randint(0, len(indic_locs)-1)
                selection[indic_locs[loc] + indic_lens[loc] + 1] = ')'
                feedback = 'Each indicator phrase identified must have a corresponding wordplay type.'
            case 6:
                selection = i_cipher.copy()
                locs = random.sample(list(range(0, len(indics))), random.randint(1, len(indic_lens) - 2))
                for loc in locs:
                    i_cipher[indic_locs[loc]] = i_cipher[loc][1:] # get rid of (
                    i_cipher[indic_locs[loc] + indic_lens[loc]] = '$' # get rid of =
                    i_cipher[indic_locs[loc] + indic_lens[loc] + 1] = '$' # get rid of wp
                c = selection.count('')
                for i in range(c):
                    selection.remove('')
                feedback = 'There are additional indicators to be identified.'



                    


                
         
        