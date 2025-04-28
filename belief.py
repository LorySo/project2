belief_base = ['p','-q','pI-q']

check_query = ['q']


def find_main_connective(query):
    min_priority = 100
    main_position = -1
    main_val = ''
    priorities = {'A': 2, 'U': 3, 'I': 4, '=': 5}

    level = 0  # for parentheses depth
    for i, c in enumerate(list(query)):
        if c == '(':
            level += 1
        elif c == ')':
            level -= 1
        elif c in priorities and level == 0:
            if priorities[c] < min_priority:
                min_priority = priorities[c]
                main_position = i
                main_val = c
    return main_position, main_val


def negate(query):
    list_query = list(query)

    # singleton
    if len(query) == 1:
        return '-' + query
    
    # negation (-)
    if list_query[0]=='-' and len(query) == 2:
        return query[1]

    if list_query[0]=='-' and list_query[1]=='(' and query[-1]==')':
        return query[2:-1]

    main_pos, main_op = find_main_connective(query)
    left = query[:main_pos]
    right = query[main_pos+1:]

    #conjunction (A)
    if main_op == 'A':
        return f"{negate(left)}U{negate(right)}"
    
    # disjunction (U)
    elif main_op == 'U':
        return f"{negate(left)}A{negate(right)}"
    
    # implication (I)
    elif main_op == 'I':
        return f"{left}A{negate(right)}"
    
    # biconditional (=)
    elif main_op == '=':
        return f"({left}A{negate(right)})U({negate(left)}A{right})"

    else:
        return '-' + query

def belief_to_cnf(query):
    list_query = list(query)

    #singletons
    if len(list_query) == 1 or (list_query[0]=='-' and len(list_query) == 2):
        return [query]

    # remove double negation
    if query.startswith('-(') and query.endswith(')') and list_query[2] == '-' and list_query[3] == '-' and list_query[-2] == ')':
        return belief_to_cnf(query[2:-1])
    
    main_pos, main_op = find_main_connective(query)
    left = query[:main_pos]
    right = query[main_pos+1:]

    # implication
    if main_op == 'I':
        new_query = f"{belief_to_cnf(negate(left))}U{belief_to_cnf(right)}"
        return new_query

    # biconditional
    elif main_op == '=':
        new_query = f"({belief_to_cnf(left)}A{belief_to_cnf(right)})U({belief_to_cnf(negate(left))}A{belief_to_cnf(negate(right))})"
        return new_query

    # conjuction
    elif main_op == 'A':
        return f"{belief_to_cnf(left)}A{belief_to_cnf(right)}"

    # disjunction

    # negation
    elif query.startswith('-(') and query.endswith(')'):
        return belief_to_cnf(negate(query[1:]))

    if query.startswith('(') and query.endswith(')'):
        return belief_to_cnf(query[1:-1])

    return [set([query])]


def check_entailmt(belief_set,query):
    query=negate(query)
    new_belief=belief_set+query
