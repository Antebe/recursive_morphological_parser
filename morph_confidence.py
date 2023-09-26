def calculate_confidence(morph):
    """Calculates the confidence of a given morph.

    Args:
        morph: A string representing a morph.

    Returns:
        A float representing the confidence of the morph.
    """
    base = list("prsie")
    weights = {}
    occurrences = {}
    positions = {}

    for i, char in enumerate(base):
        weights[char] = 1
        occurrences[char] = 0
        positions[char] = i + 1

    if "r" not in morph or morph.count("e") > 1:
        return -1


    confidence = 0.01
    for char in morph:
        occurrences[char] += 1
        confidence += weights[char]

        for key in weights:
            if key == char:
                weights[key] /= (2**occurrences[char])
            else:
                if positions[char] < positions[key]:
                    weights[key] /= 2 + occurrences[char]
                else:
                    weights[key] /= ((2.5)**occurrences[char])

    return confidence


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
