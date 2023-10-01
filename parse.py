import os
import json
import time
import argparse
import morph_confidence
import read_morphemes 
import morphemes as Morphemes
import mealy as MealyMachine
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

M = Morphemes.Morphemes(prefixes = all_morphemes['prefixes'], roots=all_morphemes['roots'], interfixes=all_morphemes['interfixes'], suffixes=all_morphemes['suffixes'], postfixes=all_morphemes['postfixes'],
endings=all_morphemes['endings'] )

print("########test#############")
####test#########
n = 1

if algo == "filter":
    f = filter.Filter(sel_word, M, filter.possible_sequences)
    #print(f.automata2graph())
    #s = list(f.inspect().keys())[0] #the most probable sequence
    print(f.inspect())
    start = time.time()
    for i in range(n):
        f = filter.Filter(sel_word, M, filter.possible_sequences)
        f.inspect()
    print(f'Speed of filter: {(time.time() - start)/n} per word')

if algo == "backtrace":
    mealy = MealyMachine.MealyMachine(sel_word, M)
    d = mealy.all_paths()
    print(list(d.keys())[0], d[list(d.keys())[0]])
    #stress testing
    start = time.time() 
    for i in range(n):
        mealy = MealyMachine.MealyMachine(sel_word, M)
        mealy.all_paths()
    print(f"Speed of backtracing: {(time.time() - start)/n} per word")