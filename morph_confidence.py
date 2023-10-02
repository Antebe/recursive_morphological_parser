def calculate_confidence(morph):
    """Calculates the confidence of a given morph.

    Args:
        morph: A string representing a morph.

    Returns:
        A float representing the confidence of the morph.
    """
    char_count = {}

    for char in morph:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    
    confidence = 0

    q_rec = -1
    q_nonrec = -4
    q_root = -q_nonrec * (len(morph) - 1)

    for k in char_count.keys():
        if k == 'r':
            confidence = confidence + q_root*char_count['r']
        elif k in {'s', 'p'}:
            confidence = confidence + q_rec*char_count[k]
        else:
            confidence = confidence + q_nonrec*char_count[k]

    return confidence * len(morph)


def most_possible(lst):
    """Returns the most possible morphs in a given list.

    Args:
        lst: A list of strings representing morphs.

    Returns:
        A list of tuples, where each tuple contains a morph and its probability.
    """

    confidences = [calculate_confidence(x) - 1 for x in lst]
    sm = sum(confidences)
    res = []
    for x, c in zip(lst, confidences):
        res.append((c / sm * 100, x))

    res.sort()
    char = [c[1] for c in res]
    num = [c[0] for c in res][::-1]

    return char #list(zip(char, num))


# Example usage:

# print(most_possible(['ppprrsss',
#  'pprrss',
#  'prrss',
#  'pprrs',
#  'ppprrss',
#  'ppprsss',
#  'ppprrs',
#  'pprsss',
#  'pprss',
#  'pprs',
#  'pprrsss',
#  'ppprss',
#  'prrsss',
#  'prrs',
#  'ppprs']))

def sort_dict(dct):
    my_dict = dct
    # Sort the keys in ascending order
    sorted_keys = most_possible(my_dict.keys())
    # Create a new dictionary with sorted keys
    sorted_dict = {key: my_dict[key] for key in sorted_keys}
    return sorted_dict