import sys 

def g_0(n):
    return ('?',) * n

def s_0(n):
    return ('T',) * n

hypothesis_general = g_0(5)
hypothesis_specific = s_0(5)
# print(hypothesis_general)
# print(hypothesis_specific)

def more_general(h1, h2):
    if h1.count('?') > h2.count('?'):
        return h1
    return h2

def min_generalizations(h, x):
    new_hypothesis = []
    for index, feature in enumerate(h):
        if feature == '?' or x[index] != feature:
            new_hypothesis.append('?')
        else:
            new_hypothesis.append(feature)

    return tuple(new_hypothesis)

def min_specializations(h, domains, x):
    list_result = []

    for index, feature in enumerate(h):
        if feature == '?':
            for value in domains[index]:
                if value != x[index]:
                    h_copy = list(h)
                    h_copy[index] = value
                    list_result.append(tuple(h_copy))

    return list_result

netspeak3-log-browser

def candidate_elimination(examples):
    list_domains = create_list_domains(examples)

    S = init_S(examples)
    G = [g_0(len(examples[0]) - 1)]

    for example in examples:
        if example[-1]:
            for index, hypothesis in enumerate(G):
                if not is_consistent(hypothesis, example):
                    del G[index]

            print(S, G)
            
            for index, hypothesis in enumerate(S):
                if not is_consistent(hypothesis, example):
                    del S[index]
                    S.append(min_generalizations(hypothesis, example))
                    S = remove_less_specific(S)
        else:
            for index, hypothesis in enumerate(S):
                if not is_consistent(hypothesis, example):
                    del S[index]

            print(S, G)
            
            for index, hypothesis in enumerate(G):
                if is_consistent(hypothesis, example):
                    print('G', G)
                    del G[index]
                    G.append(min_specializations(hypothesis, list_domains, example))
                    print('G', G)
                    G = remove_less_general(G)
            

def remove_less_specific(S):
    print('S before', S)
    spec_count = sys.maxsize
    for hypothesis in S:
        curr_count = hypothesis.count('?') 
        if spec_count > curr_count:
            spec_count = curr_count
    for index, hypothesis in enumerate(S):
        if hypothesis.count('?') > spec_count:
            del S[index]
    print('S after', S)
    return S

def remove_less_general(G):
    print('G before', G)
    general_count = 0
    for hypothesis in G:
        curr_count = hypothesis.count('?') 
        if general_count < curr_count:
            general_count = curr_count
    for index, hypothesis in enumerate(G):
        if hypothesis.count('?') < general_count:
            del G[index]
    print('G after', G)
    return G


def is_consistent(h, x):
    for index, feature in enumerate(h):
        if feature != '?' and x[index] != feature:
            return False
    return True

def create_list_domains(examples):
    list_result = [set() for e in examples[0][:-1]]


    for example in examples:
        for index, feature in enumerate(example[:-1]):
            list_result[index].add(feature)

    return [list(s) for s in list_result]

def init_S(examples):
    for example in examples:
        if example[-1]:
            return [example[:-1]]


# print(more_general(hypothesis_general, hypothesis_specific))
# print(min_generalizations(('Monday', 'no', 'yes'), ('Monday', 'no', 'yes')))

list_domains = [
    ['Sunday', 'Monday', 'Wednesday'],
    ['yes', 'no'],
    ['1', '3', '5.7']
]

# print(min_specializations(('?', '?', '?'), list_domains, ('Monday', 'no', 'yes')))

candidate_elimination([
    ('Monday', 'no', 'no', False),
    ('Wednesday', 'yes', 'yes', True),
    ('Sunday', 'no', 'yes', True),
])