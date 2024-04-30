import json

with open('def_feedback.json', 'r') as in_file:
    data = in_file.readlines()

with open('def_train_ppo.json', 'w') as ppo_file, open('def_train_sup.json', 'w') as sup_file:
    for line in data:
        ex = json.loads(line)
        text = ex['clue'] + ' ||| Definition: ' + ex['definition_pred'] + '. Cipher: ' + ex['cipher_pred'] + '.'
        sum_ppo = 'Definition: ' + ex['definition_target'] + '. Cipher: ' + ex['cipher_target'] + '.'
        sum_sup = ex['feedback']
        ppo_ex = {'text': text, 'summary': sum_ppo}
        sup_ex = {'text': text, 'summary': sum_sup}
        ppo_file.write(json.dumps(ppo_ex) + '\n')
        sup_file.write(json.dumps(sup_ex) + '\n')