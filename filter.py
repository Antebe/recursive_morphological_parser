from nltk import CFG
from nltk.parse.generate import generate
import morphemes as Morphemes
import mealy as MealyMachine
from collections import deque
import morph_confidence

d = 9 #depth of recursion 

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

class Filter:
    def __init__(self, word, M: Morphemes.Morphemes, morph_seqs):
        self.M = M
        self.word = word
        self.mealy = MealyMachine.MealyMachine(word, M)
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