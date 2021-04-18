def parse_grammar(text):
    index = 0
    grammar = dict()
    head = None
    tokens = text.split()
    while index < len(tokens):
        if index + 1 < len(tokens) and tokens[index + 1] == '->':
            head = tokens[index]
            index += 2
            grammar[head] = [[]]
        elif tokens[index] == '|':
            grammar[head].append([])
            index += 1
        else:
            l = len(grammar[head]) - 1
            grammar[head][l].append(tokens[index])
            index += 1

    return grammar


def set_space(n):
    s = ''
    while n > 0:
        s += ' '
        n -= 1
    return s


def to_pretty(grammar):
    keys = list(grammar.keys())
    left = 0
    pretty = ''

    for key in keys:
        if len(key) > left:
            left = len(key)

    for key in keys:
        for i in range(0, len(grammar[key])):
            if i == 0:
                pretty += set_space(left - len(key))
                pretty += key
                pretty += ' -> '
            else:
                pretty += set_space(left)
                pretty += '  | '
            pretty += ' '.join(grammar[key][i]) + '\n'

    return pretty


