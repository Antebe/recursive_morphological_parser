import os
import json
from collections import deque
import time
from nltk import CFG
from nltk.parse.generate import generate
import argparse
import morph_confidence
import read_morphemes 

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--word', type=str, required=True)
parser.add_argument('-f', '--folder', type=str, required=True)
parser.add_argument('-a', '--algo', type=str, required=True)
args = parser.parse_args()
sel_word = args.word
folder_lang = args.folder
algo = args.algo
d = 9 #depth of recursion

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
lang_dir = os.path.join(THIS_DIR, folder_lang)
all_morphemes = read_morphemes.read_morphemes(folder_lang)


class Morphemes:
    def __init__(self, prefixes, roots, interfixes, suffixes, endings=[], postfixes=[]):
        self.morphemes_dict = self.load_morphemes(
            prefixes, roots, interfixes, suffixes, endings, postfixes)
        self.morphemes = self.morphemes_dict['prefixes'] | self.morphemes_dict['roots'] | self.morphemes_dict[
            'interfixes'] | self.morphemes_dict['suffixes'] | self.morphemes_dict['endings'] | self.morphemes_dict['postfixes']

    def load_morphemes(self, prefixes, roots, interfixes, suffixes, endings, postfixes):
        morphemes_dict = {
            'prefixes': set(['+' + i for i in prefixes]),
            'roots': set(['$' + i for i in roots]),
            'interfixes': set(['-' + i for i in interfixes]),
            'suffixes': set(['^' + i for i in suffixes]),
            'endings': set(['*' + i for i in endings]),
            'postfixes': set(['@' + i for i in postfixes])
        }
        return morphemes_dict


grammar = CFG.fromstring('''
  W -> Base End | Base
  Base -> Stem | Stem XBase
  XBase -> "i" Base | Base
  Stem ->  Prefix Root Suffix | Prefix Root | Root | Root Suffix
  Suffix -> "s" | "s" Suffix
  Prefix -> "p" | "p" Prefix
  End -> "e" | "ex" | "x"
  Root -> "r"  ''')
grammar.productions()

possible_sequences = []
i = 0
for production in generate(grammar, depth=d):
    possible_sequences.append(''.join(production))
    i += 1
possible_sequences = list(set(possible_sequences))
print("# of sequences: ", len(possible_sequences))

class MealyMachine:
    def __init__(self, word, M: Morphemes):
        self.word = word
        self.transitions = self.fast_parse()
        self.initial_state = word[0] + '0'
        self.terminal_state = 'T'
        self.allowed_paths = {'&': {'p', 'r'},
                              'p': {'p', 'r'},
                              'r': {'p', 'r', 'T', 's', 'i', 'e'},
                              'i': {'p', 'r'},
                              's': {'s', 'e', 'x', 'T', 'i', 'p'},
                              'e': {'x', 'T'},
                              'x': {'T'},
                              'T': {'T'}}

    def num_letter_2_word(self, num_lettered_word: list):
        return ''.join([i[0] for i in num_lettered_word])

    def morphemes_by_sequence(self, seqs):
        result = set()
        if '+' + seqs in M.morphemes:
            result.add('p')
        if '$' + seqs in M.morphemes:
            result.add('r')
        if '-' + seqs in M.morphemes:
            result.add('i')
        if '^' + seqs in M.morphemes:
            result.add('s')
        if '*' + seqs in M.morphemes:
            result.add('e')
        if '@' + seqs in M.morphemes:
            result.add('x')
        return result
    
    def add_symbol_to_mopheme(self, morpheme:str, type:str):
        type2symbol = {"p":"+", "r":"$","s":"^","e":"*","i":"-","x":"@"}
        return type2symbol[type] + morpheme

    def word2matrix(self, word):
        letters_to_check = [word[i]+str(i) for i in range(len(word))]
        letter_matrix = {}
        for i in range(len(letters_to_check)):
            letter_matrix[letters_to_check[i]] = list()

        indicies_to_check = [0]
        while len(indicies_to_check) != 0:
            for index in indicies_to_check:
                indicies_to_check = []
                for i in range(len(letters_to_check)+1):
                    if index > len(word):
                        break
                    combs = self.morphemes_by_sequence(word[index:i])
                    if combs != set():
                        combs = ([j + str(i-1) for j in list(combs)])
                        #print(letter_matrix)
                        letter_matrix[letters_to_check[index]] = letter_matrix[letters_to_check[index]]+(
                            [(letters_to_check[i-1], combs)])
                        if i >= 0:
                            indicies_to_check.append(i)
        sequence = {letters_to_check[i]: letters_to_check[i+1]
                    for i in range(len(letters_to_check) - 1)}
        sequence[letters_to_check[-1]] = 'T'
        return letter_matrix, sequence, letters_to_check

    def fast_parse(self):
        word = self.word
        matrix = self.word2matrix(word)
        transitions = {}
        for letter in matrix[2]:
            if matrix[0][letter] == []:
                transitions[letter] = {}

            for trans in matrix[0][letter]:
                temp = dict()
                for morph in trans[1]:
                    temp[morph] = {'output': self.num_letter_2_word(matrix[2][int(
                        letter[1:]):int(trans[0][1:])+1]), 'next_state': matrix[1][trans[0]]}
                if letter in transitions:
                    transitions[letter].update(temp)
                else:
                    transitions[letter] = temp
        transitions['T'] = {'/n': {'output': '/n', 'next_state': 'T'}}
        return transitions

    def get_possible_inputs(self, from_state, to_state):
        possible_inputs = []
        for symbol, transitions in self.transitions[from_state].items():
            if transitions['next_state'] == to_state:
                possible_inputs.append(symbol)
        return possible_inputs

    def backtrace_paths(self, current_state, terminal_state, current_output='', path=[], permitted_transitions='&'):
        if current_state == terminal_state:
            return [(path + [(current_state, current_output)])]

        paths = []
        for symbol, transitions in self.transitions[current_state].items():

            next_state = transitions['next_state']
            output = transitions['output']

            possible_inputs = self.get_possible_inputs(
                current_state, next_state)
            for input_symbol in possible_inputs:

                x = self.allowed_paths.get(permitted_transitions)
                if input_symbol[0] in x:
                    new_path = path + [(current_state, input_symbol, output)]
                    new_output = current_output + output
                    paths.extend(self.backtrace_paths(next_state, terminal_state,
                                 new_output, new_path, permitted_transitions=input_symbol[0]))

        return paths

    def remove_duplicates(self, list_of_lists):
        list_of_tuples = [tuple(inner_list) for inner_list in list_of_lists]
        unique_set = set(list_of_tuples)
        unique_list_of_lists = [list(unique_tuple)
                                for unique_tuple in unique_set]
        return unique_list_of_lists

    def all_paths(self):
        all_paths = self.backtrace_paths(
            self.initial_state, self.terminal_state)
        all_paths = self.remove_duplicates(all_paths)
        #print(all_paths)
        decompositions = {}
        for d in all_paths:
            seq = str()
            word_decomposed = list()
            for morpheme in d:
                if morpheme[0] == 'T':
                    continue
                seq += morpheme[1][0]
                word_decomposed.append(self.add_symbol_to_mopheme(morpheme[2], morpheme[1][0]))
            if seq in decompositions:
                decompositions[seq].append(word_decomposed)
            else:
                decompositions[seq] = [word_decomposed]
        return morph_confidence.sort_dict(decompositions)


class Filter:
    def __init__(self, word, M: Morphemes, morph_seqs):
        self.word = word
        self.mealy = MealyMachine(word, M)
        self.automata = self.mealy.fast_parse()
        self.graph = self.automata2graph()
        self.possible_sequences = morph_seqs

    def automata2graph(self):
        graph = dict()
        for k in self.automata.keys():
            temp = dict()
            for m in self.automata[k]:
                temp[self.automata[k][m]['next_state']] = []
            for m in self.automata[k]:
                temp[self.automata[k][m]['next_state']].append(m)
            graph[k] = (temp)
        return (graph)

    def find_matching_paths(self, chars):
        start = self.word[0] + '0'
        queue = deque([(start, [])])
        paths = []

        while queue:
            node, path = queue.popleft()
            for neighbor in self.graph[node]:
                edges = self.graph[node][neighbor]
                for edge in edges:
                    if ''.join(char for char in edge if char.isalpha()) == chars[len(path)]:
                        new_path = path + [neighbor]
                        if len(new_path) == len(chars):
                            paths.append([start] + new_path)
                        else:
                            queue.append((neighbor, new_path))
        return paths

    def inspect(self):
        res = {}
        for chars in self.possible_sequences:
            chars = chars + 'n'
            if len(chars) <= len(self.word) + 1:
                if self.find_matching_paths(chars):
                    #print(chars, self.find_matching_paths(chars))
                    if chars in res:
                        res[chars].append(self.find_matching_paths(chars))
                    else:
                        res[chars] = self.find_matching_paths(chars)
        return morph_confidence.sort_dict(res)


M = Morphemes(prefixes = all_morphemes['prefixes'], roots=all_morphemes['roots'], interfixes=all_morphemes['interfixes'], suffixes=all_morphemes['suffixes'], postfixes=all_morphemes['postfixes'],
endings=all_morphemes['endings'] )

print("########test#############")
####test#########
n = 5

if algo == "filter":
    f = Filter(sel_word, M, possible_sequences)
    #print(f.automata2graph())
    #s = list(f.inspect().keys())[0] #the most probable sequence
    print(f.inspect())
    start = time.time()
    for i in range(n):
        f = Filter(sel_word, M, possible_sequences)
        f.inspect()
    print(f'Speed of filter: {(time.time() - start)/n} per word')

if algo == "backtrace":
    mealy = MealyMachine(sel_word, M)
    print(mealy.all_paths())
    #stress testing
    start = time.time() 
    # for i in range(n):
    #     mealy = MealyMachine(sel_word, M)
    #     mealy.all_paths()
    # print(f"Speed of backtracing: {(time.time() - start)/n} per word")