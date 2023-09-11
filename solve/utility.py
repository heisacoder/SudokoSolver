
def cross(A, B):
    """
    cross product of elements in A and in B. E.g. A = 'AB', B = '12', cross(A, B) = ['A1','A2', 'B1', 'B2']
    """
    return [a + b for a in A for b in B]


def min_dictionary(dictionary):
    """
    finds the key with minimum value in the dictionary.
    :param dictionary:
    :return:
    """
    return min(dictionary, key=dictionary.get)
