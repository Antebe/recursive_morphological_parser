import os
import json
import time
import argparse
import morph_confidence
import read_morphemes 
import morphemes as Morphemes
import mealy as MealyMachine
import math
#import filter


parser = argparse.ArgumentParser()
parser.add_argument('-w', '--word', type=str, required=True)
parser.add_argument('-f', '--folder', type=str, required=True)
parser.add_argument('-a', '--algo', type=str, required=True)
args = parser.parse_args()
sel_word = args.word
folder_lang = args.folder
algo = args.algo

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
lang_dir = os.path.join(THIS_DIR, folder_lang)
all_morphemes = read_morphemes.read_morphemes(folder_lang)

#load freqs vocab
# Read the JSON file
with open(os.path.join(lang_dir, "frequency.json"), 'r', encoding="UTF8") as json_file:
    freqs = json.load(json_file)

M = Morphemes.Morphemes(prefixes = all_morphemes['prefixes'], roots=all_morphemes['roots'], interfixes=all_morphemes['interfixes'], suffixes=all_morphemes['suffixes'], postfixes=all_morphemes['postfixes'],
endings=all_morphemes['endings'] )

print("########test#############")
####test#########
n = 1

if algo == "filter":
    f = filter.Filter(sel_word, M, filter.possible_sequences)
    #print(f.automata2graph())
    #s = list(f.inspect().keys())[0] #the most probable sequence
    #print(f.inspect())
    start = time.time()
    for i in range(n):
        f = filter.Filter(sel_word, M, filter.possible_sequences)
        f.inspect()
    print(f'Speed of filter: {(time.time() - start)/n} per word')

if algo == "backtrace":
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
    print(list(ans_d.keys())[0])
    #stress testing
    start = time.time() 
    for i in range(n):
        mealy = MealyMachine.MealyMachine(sel_word, M)
        mealy.all_paths()
    print(f"Speed of backtracing: {(time.time() - start)/n} per word")

def parse(w):
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
    return (list(ans_d.keys())[0])
