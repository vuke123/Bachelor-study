import sys


class Clause:
    def __init__(self, content, parent1=None, parent2=None):
        self.content = content
        self.parent1 = parent1
        self.parent2 = parent2

    def __eq__(self, other):
        if isinstance(other, Clause):
            content_equal = set(self.content.split(" v ")) == set(
                other.content.split(" v "))
            return content_equal
        return False

    def __hash__(self):
        content_hash = frozenset(self.content.split(" v "))
        return hash((content_hash))


def Complement(clause):
    new_clauses = set()
    for element in clause.split(" v "):
        new_clause = ""
        if element[0] == "~":
            new_clause += element[1:]
        else:
            new_clause += ("~" + element)
        new_clauses.add(Clause(new_clause))
    return new_clauses


def LoadClauses(clauses_path, is_cooking):
    clauses = set()
    sos = set()
    goal = None
    with open(clauses_path, 'r') as f:
        lines = [line.lower() for line in f.readlines()]
        for line in lines[:-1]:
            if line.startswith("#") != True:
                clauses.add(Clause(line.strip()))
        if is_cooking == True:
            clauses.add(Clause(lines[-1].strip()))
        else:
            complement_goal = Complement(lines[-1].strip())
            goal = lines[-1].strip()
            clauses.update(complement_goal)
            sos.update(complement_goal)
        f.close()
    return clauses, sos, goal


def LoadCommands(command_path):
    commands = []
    with open(command_path, 'r') as f:
        lines = [line.lower() for line in f.readlines()]
        for line in lines:
            if line.startswith("#") != True:
                commands.append(line.strip())
        f.close()
    return commands


def plResolve(clause1, clause2):
    resolved_element = None
    clause1_set = set(clause1.content.split(" v "))
    clause2_set = set(clause2.content.split(" v "))
    for element1 in clause1_set:
        if element1[0] == "~":
            if element1[1:] in clause2_set:
                resolved_element = element1[1:]
        else:
            if ("~" + element1) in clause2_set:
                resolved_element = element1
    if resolved_element is not None:
        union_set = clause1_set | clause2_set
        union_set.discard(resolved_element)
        union_set.discard("~" + resolved_element)
        if len(union_set) == 0:
            union_set = "NIL"
            return Clause(union_set, clause1, clause2)
        else:
            str_elements = [str(e) for e in union_set]
            union_set = " v ".join(str_elements)
            return Clause(union_set, clause1, clause2)
    else:
        return ""


def NewClausesCheck(new_clauses, clauses):
    for new_clause in new_clauses:
        for clause in clauses:
            if new_clause != clause:
                return True
    return False


def Factorize(new_clauses):
    new_clauses_copy = new_clauses.copy()
    for new_clause in new_clauses_copy:
        new_clause_set = set(new_clause.content.split(" v "))
        for literal in new_clause_set:
            if literal[1:] in new_clause_set or ("~" + literal) in new_clause_set:
                if new_clause in new_clauses:
                    new_clauses.remove(new_clause)
    return new_clauses


def Absorbe(clauses, sos):
    updated_clauses = clauses.copy()
    updated_sos = sos.copy()

    for i, s1 in enumerate(clauses):
        for j, s2 in enumerate(clauses):
            s1_set = set(s1.content.split(" v "))
            s2_set = set(s2.content.split(" v "))
            if s1_set.issubset(s2_set) and i != j:
                if s2 in updated_clauses:
                    updated_clauses.remove(s2)

    for i, s1 in enumerate(sos):
        for j, s2 in enumerate(sos):
            s1_set = set(s1.content.split(" v "))
            s2_set = set(s2.content.split(" v "))
            if s1_set.issubset(s2_set) and i != j:
                if s2 in updated_sos:
                    updated_sos.remove(s2)

    return updated_clauses, updated_sos


def plResolution(clauses, sos):
    resolved_pairs = set()
    new_clauses = set()
    while True:
        for clause1 in clauses:
            for clause2 in clauses:
                if clause1 == clause2 or (clause1, clause2) in resolved_pairs or (clause2, clause1) in resolved_pairs:
                    continue
                if clause1 not in sos and clause2 not in sos:
                    continue
                clause3 = plResolve(clause1, clause2)
                resolved_pairs.add((clause1, clause2))
                if clause3 == "":
                    continue
                elif clause3.content == "NIL":
                    return True
                else:
                    new_clauses.add(clause3)
        if len(new_clauses) == 0 or NewClausesCheck(new_clauses, clauses) == False:
            return False
        new_clauses = Factorize(new_clauses)
        sos.update(new_clauses)
        clauses.update(new_clauses)
        clauses, sos = Absorbe(clauses, sos)
        new_clauses.clear()


def main():
    clauses = set()
    sos = set()
    goal = ""
    for i, sys_arg in enumerate(sys.argv):
        if sys_arg == "resolution":
            clauses, sos, goal = LoadClauses(sys.argv[i+1], False)
            if (plResolution(clauses, sos)):
                print("[CONCLUSION]: {} is true".format(goal))
            else:
                print("[CONCLUSION]: {} is unknown".format(goal))
            continue
        elif sys_arg == "cooking":
            path = sys.argv[i+1]
            commands_path = sys.argv[i+2]
            clauses, _, _ = LoadClauses(path, True)
            commands = LoadCommands(commands_path)
            for command in commands:
                clause1 = command[:-1]
                procedure = command[-1]
                clause = Clause(clause1.strip())
                if procedure == "+":
                    clauses.add(clause)
                elif procedure == "-":
                    if clause in clauses:
                        clauses.remove(clause)
                else:
                    sos.clear()
                    sos.update(Complement(clause.strip()))
                    clauses.update(Complement(clause.strip()))
                    print("User’s command: {} ?".format(clause))
                    if(plResolution(clauses, sos)):
                        print("[CONCLUSION]: {} is true".format(clause))
                    else:
                        print("[CONCLUSION]: {} is unknown".format(clause))


if __name__ == "__main__":
    main()
