from cnf import remove_empties, remove_units, convert_grammar, remove_unreachable
from syntax import parse_grammar, to_pretty


INPUT_PATH = 'input'
OUTPUT_PATH = 'output'


def print_g(g):
    keys = g.keys()
    for key in keys:
        for value in g[key]:
            print(key, ": ", value)


if __name__ == '__main__':
    with open(INPUT_PATH, 'r+') as input_file:
        input_content = input_file.read()
        input_file.close()

    if input_content is None:
        pass

    g = parse_grammar(input_content)
    e = remove_empties(g)
    u = remove_units(e)
    l = remove_unreachable(u)
    c = convert_grammar(l)
    p = to_pretty(c)

    with open(OUTPUT_PATH, 'w+') as output_file:
        output_file.write(p)
        output_file.close()

    print(p)
