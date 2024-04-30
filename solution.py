from collections import defaultdict
from typing import Dict, List


def sortUtility(adjancency_list: Dict, LHS_to_index_mapping: Dict) -> List:
    in_degrees = { node: 0 for node in adjancency_list }
    for node in adjancency_list:
        for neighbour in adjancency_list[node]:
            in_degrees[neighbour] += 1
    nodes_with_in_deg_zero = []
    for node in adjancency_list:
        if in_degrees[node] == 0:
            nodes_with_in_deg_zero.append(node)
    visited_nodes = 0
    topological_order = []
    while nodes_with_in_deg_zero:
        dequeued_node = nodes_with_in_deg_zero.pop(0)
        # Only add nodes (variables) that are on the LHS of expressions
        if dequeued_node in LHS_to_index_mapping:
            topological_order.append(dequeued_node)
        for node in adjancency_list[dequeued_node]:
            in_degrees[node] -= 1
            if in_degrees[node] == 0:
                nodes_with_in_deg_zero.append(node)
        visited_nodes += 1
    
    # Check for cycle
    if visited_nodes != len(adjancency_list):
        return False
    return topological_order
        

def sortExpressions(expressions: List) -> Dict:
    '''
    Assumptions;
    - Variables can be x, y, z1, xyz, etc i.e they start with a letter
    - There is no guaratee that there will be space between operands and operators
    - A cycle can be created between more than two
    '''
    if len(expressions) < 2:
        return expressions
    separators = '()*/+- '
    dependent_expressions = defaultdict(list)
    LHS_to_index_mapping = {}
    
    # We are interested in variables
    for expr in enumerate(expressions):
        LHS, RHS = expr[1].split('=')
        LHS = LHS.strip()
        LHS_to_index_mapping[LHS] = expr[0]
        if LHS not in dependent_expressions:
            dependent_expressions[LHS] = []
        length_of_RHS = len(RHS)
        i = j = 0
        while i < length_of_RHS:
            if RHS[i].isalpha():
                # We then find where this ends and add that as a variable
                # and set i to value of last item of variable
                j = i
                while j < length_of_RHS:
                    if RHS[j] in separators:
                        # sigals end of variable
                        variable = RHS[i:j].strip()
                        dependent_expressions[variable].append(LHS)
                        i = j
                        j += 1
                        break
                    if j == length_of_RHS - 1:
                        variable = RHS[i:].strip()
                        dependent_expressions[variable].append(LHS)
                        j += 1
                        i = j
                        break
                    j += 1
            else:
                i += 1
    sorted = sortUtility(dependent_expressions, LHS_to_index_mapping)
    if not sorted:
        return ["cyclic_dependency"]
    return [ expressions[LHS_to_index_mapping[item]] for item in sorted ]

if __name__ == "__main__":
    returned = sortExpressions(["x = a * y", "y = x * 5"])
    print(returned)
    second = sortExpressions(["x = y + 6", "y = 7 * 4", "z = ( x * y )"])
    print(second)
    returned = sortExpressions(["x = a * y", "y = 7 * 5"])
    print(returned)
    returned = sortExpressions(["x = ap * y", "y = 7 * 5"])
    print(returned)
    returned = sortExpressions(["x = 2 * 3", "y = 7 * 5"])
    print(returned)
    returned = sortExpressions(["x = ap * y", "y = 7 * 5", "ap = 6 * y"])
    print(returned)