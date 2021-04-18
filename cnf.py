def calculate_w_sets(grammar):
    index_of_w = 1
    temp_list = []
    w = [0]

    keys = list(grammar.keys())
    for key in keys:
        if ['#'] in grammar[key]:
            temp_list.append(key)
        w[0] = temp_list[:]

    while True:
        temp_list = []
        for key in keys:
            value = grammar[key]
            for i in range(0, len(value)):
                for j in range(0, len(value[i])):
                    char = value[i][j]
                    latest = w[index_of_w - 1]

                    if char in latest and \
                            key not in temp_list:
                        temp_list.append(key)

        w.insert(index_of_w, temp_list[:])

        if w[index_of_w] == w[index_of_w - 1]:
            break

        index_of_w += 1

    return index_of_w, w


def find_combinations(set_of, w, s, index_of_w, position):
    for i in range(position, len(s)):
        if s[i] in w[index_of_w]:
            s_1 = s[:]
            s_1.pop(i)

            if s_1 and s_1 not in set_of:
                set_of.append(s_1)

            find_combinations(set_of, w, s_1, index_of_w, position)

    return set_of


def gen_new_grammar(grammar, w, index_of_w):
    new_grammar = dict()

    keys = list(grammar.keys())
    for key in keys:
        value = grammar[key]
        temp_list = []
        for i in range(0, len(value)):
            set_of = find_combinations([], w, value[i], index_of_w, 0)

            if value[i] and [value[i]] not in temp_list:
                temp_list += [value[i]]

            if set_of and set_of not in temp_list:
                temp_list += set_of

        if key in new_grammar:
            new_grammar.pop(key)
        new_grammar[key] = temp_list

    return new_grammar


def remove_empty(grammar):
    keys = list(grammar.keys())
    for key in keys:
        value = grammar[key]
        temp_list = []
        for i in range(0, len(value)):
            if '#' not in value[i]:
                temp_list.append(value[i])

        grammar[key] = temp_list[:]

    for key in keys:
        result = []
        for value in grammar[key]:
            if value not in result:
                result.append(value)
        grammar[key] = result[:]

    return grammar


def remove_empties(grammar):
    index_of_w, w = calculate_w_sets(grammar)
    new_grammar = gen_new_grammar(grammar, w, index_of_w)
    new_grammar = remove_empty(new_grammar)

    return new_grammar


def array_equal(a, b):
    if len(a) != len(b):
        return False

    for i in range(0, len(a)):
        if a[i] != b[i]:
            return False

    return True


def add_new_gen(grammar, key, new_gen):
    for i in range(0, len(grammar[key])):
        if array_equal(new_gen, grammar[key][i]):
            return None

    grammar[key].append(new_gen[:])


def remove_units(grammar):
    keys = list(grammar.keys())
    hasUnit = True

    while hasUnit:
        hasUnit = False
        for key in keys:
            for i in range(0, len(grammar[key])):
                for value in grammar[key][i]:
                    if len(grammar[key][i]) == 1 and value[0] in keys:
                        unit = value[0]
                        grammar[key].pop(i)
                        for j in range(0, len(grammar[unit])):
                            add_new_gen(grammar, key, grammar[unit][j])
                        hasUnit = True

    return grammar


def get_additional_key(index):
    return 'X' + str(index)


def get_additional_index(grammar, index):
    keys = list(grammar.keys())
    while get_additional_key(index) in keys:
        index += 1
    return index


def convert_grammar(grammar):
    keys = list(grammar.keys())
    singles = dict()
    multis = dict()
    additional_index = 0

    for key in keys:
        if len(grammar[key]) == 1:
            if len(grammar[key][0]) == 1:
                term = grammar[key][0][0]
                if term != '#' and term not in keys:
                    singles[term] = key

    for key in keys:
        if len(grammar[key]) == 1:
            multis[' '.join(grammar[key][0])] = key

    for key in keys:
        for j in range(0, len(grammar[key])):
            value = grammar[key][j]
            if len(value) == 2:
                for i in range(0, 2):
                    if value[i] not in keys:
                        if value[i] not in singles:
                            additional_index = get_additional_index(grammar, additional_index)
                            additional_key = get_additional_key(additional_index)
                            keys.append(additional_key)
                            grammar[additional_key] = [value[i][:]]
                            singles[value[i]] = additional_key

                        grammar[key][j][i] = singles[value[i]]

            elif len(value) > 2:
                last = len(value) - 1
                if value[last] not in keys:
                    if value[last] not in singles:
                        additional_index = get_additional_index(grammar, additional_index)
                        additional_key = get_additional_key(additional_index)
                        keys.append(additional_key)
                        grammar[additional_key] = [value[last][:]]
                        singles[value[last]] = additional_key

                    grammar[key][j][last] = singles[value[last]]

                term = ' '.join(value[slice(0, last)])
                if term not in multis:
                    additional_index = get_additional_index(grammar, additional_index)
                    additional_key = get_additional_key(additional_index)
                    keys.append(additional_key)
                    grammar[additional_key] = [value[slice(0, last)][:]]
                    multis[term] = additional_key

                grammar[key][j] = [multis[term], value[last]]

    return grammar


def remove_unreachable(grammar):
    keys = list(grammar.keys())
    queue = [keys[0]]
    reachable = dict()
    front = 0

    reachable[keys[0]] = True
    while front < len(queue):
        for i in range(0, len(grammar[queue[front]])):
            for j in range(0, len(grammar[queue[front]][i])):
                term = grammar[queue[front]][i][j]
                if term in keys and term not in reachable:
                    queue.append(term)
                    reachable[term] = True

        front += 1

    for key in keys:
        if key not in reachable:
            del grammar[key]

    return grammar

