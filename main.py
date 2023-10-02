import os
import json
import time
import argparse
import morph_confidence
import read_morphemes 
import morphemes as Morphemes
import mealy as MealyMachine
import math

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def preprocess(folder_lang):
    lang_dir = os.path.join(THIS_DIR, folder_lang)
    all_morphemes = read_morphemes.read_morphemes(folder_lang)

    #load freqs vocab
    # Read the JSON file
    with open(os.path.join(lang_dir, "frequency.json"), 'r', encoding="UTF8") as json_file:
        freqs = json.load(json_file)
    return all_morphemes, freqs

def parse(sel_word, preprocessed):

    all_morphemes, freqs = preprocessed[0], preprocessed[1]
    M = Morphemes.Morphemes(prefixes = all_morphemes['prefixes'], roots=all_morphemes['roots'], interfixes=all_morphemes['interfixes'], suffixes=all_morphemes['suffixes'], postfixes=all_morphemes['postfixes'],
    endings=all_morphemes['endings'] )
    ####test#########

    mealy = MealyMachine.MealyMachine(sel_word, M)
    d = mealy.all_paths()
    #print(list(d.keys())[0], d[list(d.keys())[0]]) #sequence + parsing
    answer = d[list(d.keys())[0]]
    ans_d = {}
    for parsing in answer:
        s = 0
        for morph in parsing:
            if morph[1:] in freqs:
                s+=math.log(freqs[morph[1:]]) * len(morph)
            else:
                s+=1
        ans_d[tuple(parsing)] = s
    ans_d = {k: v for k, v in sorted(ans_d.items(), key=lambda item: item[1], reverse=True)}
    return list(ans_d.keys())[0]

def parse_text(text, preprocessed):
    start = time.time()
    res = list()
    text = text.split()
    for w in text:
        res.append(" ".join(parse(w, preprocessed)))
        if w == ".":
            res.append("<END_SENT>")
        else:
            res.append("<END_W>")
    print("Time elapsed: ", time.time() - start)
    return " ".join(res)
    
########
l = "en"
preprocessed = preprocess(l)
print(parse_text("she underestimates people who have unlockable doors . \
                 in my hyperhumble opinion a lot of people fail to recognize the danger of such recklessness  ", preprocessed))

# l = "uk"
# preprocessed = preprocess(l)
# print(parse_text("щоземлетрусу я бачу радіокардіограф", preprocessed))