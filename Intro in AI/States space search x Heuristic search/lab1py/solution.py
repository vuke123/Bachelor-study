import heapq
import sys


def BFS_algorithm(s0, ops_dict, goals):
    open = [BFS_struc(s0, 0, [])]
    closed = set()
    while len(open) != 0:
        knot = open.pop(0)
        closed.add(knot.state)
        if knot.state in goals:
            knot.states.append(knot.state)
            return "yes", len(closed), len(knot.states), knot.total*1.0, knot.states
        children = sorted(ops_dict.get(knot.state), key=lambda x: x[0])
        for child in children:
            if child[0] not in closed:
                knot_states_copy = knot.states.copy()
                knot_states_copy.append(knot.state)
                open.append(BFS_struc(child[0], int(child[1]) +
                            knot.total, knot_states_copy))
    return "no", -1, -1, -1, -1


def UCS_algorithm(s0, ops_dict, goals):
    open = []
    heapq.heappush(open, UCS_struc(s0, 0, []))
    closed = set()
    while len(open) != 0:
        knot = heapq.heappop(open)
        closed.add(knot.state)
        if knot.state in goals:
            knot.states.append(knot.state)
            return "yes", len(closed), len(knot.states), knot.total*1.0, knot.states
        children = sorted(ops_dict.get(knot.state), key=lambda x: x[1])
        for child in children:
            if child[0] not in closed:
                knot_states_copy = knot.states.copy()
                knot_states_copy.append(knot.state)
                heapq.heappush(open, UCS_struc(child[0], int(
                    child[1]) + knot.total, knot_states_copy))
    return "no", -1, -1, -1, -1


class BFS_struc:
    def __init__(self, state, total, states):
        self.total = total
        self.state = state
        self.states = states

    def __lt__(self, other):
        return self.state < other.state


class UCS_struc:
    def __init__(self, state, total, states):
        self.total = total
        self.state = state
        self.states = states

    def __lt__(self, other):
        if self.total == other.total:
            return self.state < other.state
        return self.total < other.total


class Astar_struc:
    def __init__(self, heuristic, total, state, states):
        self.heuristic = heuristic
        self.total = total
        self.state = state
        self.states = states

    def __lt__(self, other):
        return self.heuristic < other.heuristic


def A_star_algorithm(s0, ops_dict, oh_dict, goals):
    open = []
    heapq.heappush(open, Astar_struc(0, 0, s0, []))
    closed = {}
    while len(open) != 0:
        knot = heapq.heappop(open)
        closed[knot.state] = knot.total
        if knot.state in goals:
            knot.states.append(knot.state)
            return "yes", len(closed), len(knot.states) + 1, knot.total*1.0, knot.states
        children = sorted(ops_dict.get(knot.state), key=lambda x: x[1])
        for child in children:
            skip = False
            real_distance = int(child[1]) + knot.total
            if closed.get(child[0]) != None:
                if closed[child[0]] > real_distance:
                    closed.clear(child[0])
                else:
                    skip = True
                    continue
            else:
                for element in open:
                    if element.state == child[0]:
                        if element.total > real_distance:
                            open_list = list(open)
                            open_list.remove(element)
                            heapq.heapify(open_list)
                        else:
                            skip = True
                        break
            if skip != True:
                knot_states_copy = knot.states.copy()
                knot_states_copy.append(knot.state)
                heapq.heappush(open, Astar_struc(
                    real_distance + int(oh_dict[child[0]]), real_distance, child[0], knot_states_copy))

    return "no", -1, -1, -1, -1


def H_C_check(ops_dict, oh_dict):
    consistent = True
    for ops, lista in ops_dict.items():
        state = ops
        for neighbour in lista:
            if neighbour[0] == "":
                break
            heuristic_parent = oh_dict[state]
            heuristic_child = oh_dict[(neighbour[0])]
            c = neighbour[1]
            if float(heuristic_parent) <= float(heuristic_child) + float(c):
                print("[CONDITION]: [OK] h({}) <= h({}) + c: {:.1f} <= {:.1f} + {:.1f}".format(
                    state, neighbour[0], float(heuristic_parent), float(heuristic_child), float(c)))
            else:
                consistent = False
                print("[CONDITION]: [ERR] h({}) <= h({}) + c: {:.1f} <= {:.1f} + {:.1f}".format(
                    state, neighbour[0], float(heuristic_parent), float(heuristic_child), float(c)))
    if consistent:
        print("[CONCLUSION]: Heuristic is consistent.")
    else:
        print("[CONCLUSION]: Heuristic is not consistent.")
    return


def H_O_check(ops_dict, oh_dict, goals):
    optimistic = True
    for ops, lista in ops_dict.items():
        estimate = float(oh_dict[ops])
        _, _, _, real, _ = UCS_algorithm(ops, ops_dict, goals)
        if estimate <= real:
            print(
                "[CONDITION]: [OK] h({}) <= h*: {} <= {}".format(ops, estimate, real))
        else:
            optimistic = False
            print(
                "[CONDITION]: [ERR] h({}) <= h*: {} <= {}".format(ops, estimate, real))
    if optimistic:
        print("[CONCLUSION]: Heuristic is optimistic.")
    else:
        print("[CONCLUSION]: Heuristic is not optimistic.")
    return


def Read_heuristics(file):
    oh_dict = {}
    with open(file, 'r') as f:
        for line in f:
            if line.startswith("#") != True:
                key = line.split(":")[0]
                value = line.split(":")[1].strip()
                oh_dict[key] = value
        f.close()
    return oh_dict


def Read_space(file):
    ops_dict = {}
    s0 = None
    with open(file, 'r') as f:
        for line in f:
            if line.startswith("#") != True:
                if line.find(":") == -1 and s0 == None:
                    s0 = line.strip()
                elif line.find(":") == -1 and s0 != None:
                    goals = line.strip().split(" ")
                else:
                    key = line.split(":")[0]
                    value = line.split(":")[1]
                    value_splitted = value.strip().split(" ")
                    list_of_tuples = []
                    for v in value_splitted:
                        list_of_tuples.append(tuple(v.split(",")))
                    ops_dict[key] = list_of_tuples
        f.close()
    return ops_dict, s0, goals


def main():

    ops_dict = {}
    oh_dict = {}
    s0 = None
    goals = None

    optimistic_check = False
    consistent_check = False

    algorithm = ""
    path_space = ""
    optimistic_check = ""
    path_heuristic = ""
    consistent_check = ""

    for i, sys_arg in enumerate(sys.argv):
        if sys_arg == "--alg":
            algorithm = sys.argv[i+1]
        elif sys_arg == "--ss":
            path_space = sys.argv[i+1]
        elif sys_arg == "--h":
            path_heuristic = sys.argv[i+1]
        elif sys_arg == "--check-optimistic":
            optimistic_check = True
        elif sys_arg == "--check-consistent":
            consistent_check = True

    if algorithm != "":
        found_solution = ""
        states_visited = 0
        path_length = 0
        total_cost = 0
        path_string = ""
        if algorithm == "bfs":

            ops_dict, s0, goals = Read_space(path_space)
            found_solution, states_visited, path_length, total_cost, path = BFS_algorithm(
                s0, ops_dict, goals)
            path_string = ""
            for p in path:
                path_string = path_string + p + " => "
            print("# BFS")

        elif algorithm == "ucs":
            ops_dict, s0, goals = Read_space(path_space)
            found_solution, states_visited, path_length, total_cost, path = UCS_algorithm(
                s0, ops_dict, goals)
            path_string = ""
            for p in path:
                path_string = path_string + p + " => "
            print("# UCS")

        elif algorithm == "astar":
            ops_dict, s0, goals = Read_space(path_space)
            oh_dict = Read_heuristics(path_heuristic)

            found_solution, states_visited, path_length, total_cost, path = A_star_algorithm(
                s0, ops_dict, oh_dict, goals)
            path_string = ""
            for p in path:
                path_string = path_string + p + " => "
            print("# A-STAR {}".format(path_heuristic))

        print("[FOUND_SOLUTION]: {}".format(found_solution))

        if (found_solution == "yes"):
            print("[STATES_VISITED]: {}".format(str(states_visited)))
            print("[PATH_LENGTH]: {}".format(str(path_length)))
            print("[TOTAL_COST]: {}".format(str(total_cost)))
            print("[PATH]: {}".format(path_string[:-3]))

    else:
        ops_dict, s0, goals = Read_space(path_space)
        oh_dict = Read_heuristics(path_heuristic)
        if optimistic_check is True:

            print("# HEURISTIC-OPTIMISTIC {}".format(path_heuristic))
            H_O_check(ops_dict, oh_dict, goals)

        elif consistent_check is True:
            print("# HEURISTIC-CONSISTENT {}".format(path_heuristic))
            H_C_check(ops_dict, oh_dict)


if __name__ == "__main__":
    main()
