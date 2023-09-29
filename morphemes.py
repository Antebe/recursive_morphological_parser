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