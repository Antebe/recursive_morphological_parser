import morphemes as Morphemes
import morph_confidence

class MealyMachine:
    def __init__(self, word, M: Morphemes.Morphemes):
        self.recursion_depth = int(1/3 * len(word)) + 1
        self.word = word
        self.M = M
        self.transitions = self.fast_parse()
        self.initial_state = word[0] + '0'
        self.terminal_state = 'T'
        self.allowed_paths = {'&': {'p', 'r'},
                              'p': {'p', 'r'},
                              'r': {'p', 'r', 'T', 's', 'i', 'e'},
                              'i': {'p', 'r'},
                              's': {'s', 'e', 'x', 'T', 'i', 'p', 'r'},
                              'e': {'x', 'T'},
                              'x': {'T'},
                              'T': {'T'}}

    def num_letter_2_word(self, num_lettered_word: list):
        return ''.join([i[0] for i in num_lettered_word])

    def morphemes_by_sequence(self, seqs):
        result = set()
        if '+' + seqs in self.M.morphemes:
            result.add('p')
        if '$' + seqs in self.M.morphemes:
            result.add('r')
        if '-' + seqs in self.M.morphemes:
            result.add('i')
        if '^' + seqs in self.M.morphemes:
            result.add('s')
        if '*' + seqs in self.M.morphemes:
            result.add('e')
        if '@' + seqs in self.M.morphemes:
            result.add('x')
        return result
    
    def add_symbol_to_mopheme(self, morpheme:str, type:str):
        type2symbol = {"p":"+", "r":"$","s":"^","e":"*","i":"-","x":"@"}
        return type2symbol[type] + morpheme

    def word2matrix(self, word):
        letters_to_check = [word[i] + str(i) for i in range(len(word))]
        letter_matrix = {}
        for i in range(len(letters_to_check)):
            letter_matrix[letters_to_check[i]] = list()

        indicies_to_check = [0]
        while len(indicies_to_check) != 0:
            new_indices_to_check = []  # Create a new list to store indices to check
            for index in indicies_to_check:
                for i in range(index + 1, len(letters_to_check) + 1):  # Start from index + 1
                    combs = self.morphemes_by_sequence(word[index:i])
                    if combs:
                        combs = [j + str(i - 1) for j in combs]
                        letter_matrix[letters_to_check[index]] += [(letters_to_check[i - 1], combs)]
                        new_indices_to_check.append(i)  # Add the new index to check
            indicies_to_check = new_indices_to_check  # Update the indices to check

        sequence = {letters_to_check[i]: letters_to_check[i + 1] for i in range(len(letters_to_check) - 1)}
        sequence[letters_to_check[-1]] = 'T'
        #print(letter_matrix, "\n", sequence, "\n", letters_to_check)
        return letter_matrix, sequence, letters_to_check


    def fast_parse(self):
        word = self.word
        matrix = self.word2matrix(word)
        transitions = {}
        for letter in matrix[2]:
            if matrix[0][letter] == []:
                transitions[letter] = {}

            for trans in matrix[0][letter]:
                #print(trans)
                temp = dict()
                for morph in trans[1]:
                    temp[morph] = {'output': self.num_letter_2_word(matrix[2][int(
                        letter[1:]):int(trans[0][1:])+1]), 'next_state': matrix[1][trans[0]]}
                if letter in transitions:
                    transitions[letter].update(temp)
                else:
                    transitions[letter] = temp
        transitions['T'] = {'/n': {'output': '/n', 'next_state': 'T'}}
        #print(transitions)
        return transitions

    def get_possible_inputs(self, from_state, to_state):
        possible_inputs = []
        for symbol, transitions in self.transitions[from_state].items():
            if transitions['next_state'] == to_state:
                possible_inputs.append(symbol)
        return possible_inputs

    def backtrace_paths(self, current_state, terminal_state, current_output='', path=[], permitted_transitions='&'):
        max_depth = self.recursion_depth
        if max_depth is not None and len(path) >= max_depth:
            return []  # Return an empty list if the maximum depth is reached.

        if current_state == terminal_state and 'T' in self.allowed_paths.get(permitted_transitions):
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

        #in case parsing failed
        if not all_paths:
            return {"r": [['$' + self.word]]}
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