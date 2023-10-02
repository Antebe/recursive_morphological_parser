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
    i = 0
    start = time.time()
    res = list()
    text = text.split()
    for w in text:

        p = " ".join(parse(w, preprocessed))
        res.append(p)
        if w == ".":
            res.append("<END_SENT>")
        else:
            res.append("<END_W>")

        if i%40 == 0:
            print(i, " words out of ", len(text), ". Projected time: ", (time.time() - start)/60, " out of ", i*len(text)/(60 * (time.time() - start) + 1), " mins")
            print(p)
            
        i+=1
    print("Time elapsed: ", time.time() - start)
    return " ".join(res)
    
import re

def remove_punctuation_except_periods(input_string):
    # Remove all punctuation except for periods using a regular expression
    input_string = input_string.replace(".", " .").replace("!", " !").replace("?", " ?")
    cleaned_string = re.sub(r'[^\w\s.!?]', '', input_string)
    return cleaned_string.lower()

# Example usage:
# input_string = "Hello, World! This is a test. How are you?"
# result = remove_punctuation_except_periods(input_string)
# print(result)  # Output will be "Hello World This is a test. How are you."

########
l = "en"
preprocessed = preprocess(l)

file_path = "Bibles\TXT\English.txt"

# Open the file in read mode ('r')
with open(file_path, 'r') as file:
    # Read the entire file content into a variable
    file_contents = file.read()

result = remove_punctuation_except_periods(file_contents)
print(parse_text(result, preprocessed))

# l = "uk"
# preprocessed = preprocess(l)
# print(parse_text("щоземлетрусу я бачу радіокардіограф", preprocessed))