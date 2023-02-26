import sys
from operator import attrgetter


class Memory:
    def __init__(self, sign="a", rowOfDefinition="0", address="V0"):
        self.sign = sign
        self.rowOfDefinition = rowOfDefinition
        self.address = address


class Defined:
    def __init__(self, sign, row, increment):
        self.sign = sign
        self.row = row
        self.increment = increment


class Output:
    def __init__(self, used, defined, sign):
        self.used = used
        self.defined = defined
        self.sign = sign


def treci(lines):
    defined = []
    after_equal = False
    increment = 1
    last_space_num = 0
    error = False
    output = []
    green_light = False
    iterating_variable = ""
    # programming language has rule that iterating_variable could not have
    row_of_iterating_var = ""
    # been the same as some variable in the part where we define a range
    for line in lines:

        if error == True:
            break

        space_num = 0
        stop_counting = False

        for x in line:
            if(x == " " and stop_counting == False):
                space_num += 1
            else:
                stop_counting = True
                break
        trimmed_line = line.strip()
        if last_space_num > space_num or trimmed_line == "<lista_naredbi>":
            after_equal = False
        if trimmed_line[0:3] == "IDN":
            already_defined = False
            if after_equal == False:
                last_space_num = space_num
                components = trimmed_line.split(" ")
                if green_light == True:
                    iterating_variable = components[2]
                    row_of_iterating_var = components[1]
                for item in defined:
                    # and item.increment == increment
                    if item.sign == components[2] and green_light == False:
                        already_defined = True
                if already_defined == False:
                    defined.append(
                        Defined(components[2], components[1], increment))
            else:
                components = trimmed_line.split(" ")
                if components[1] == row_of_iterating_var and components[2] == iterating_variable:
                    output.append(Output("err", components[1], components[2]))
                    error = True
                else:
                    filter_by_sign = list(
                        filter(lambda x: x.sign == components[2], defined))
                    sign_max_incr = None
                    if len(filter_by_sign) != 0:
                        sign_max_incr = max(
                            filter_by_sign, key=attrgetter('increment'))

                    if sign_max_incr is None:
                        output.append(
                            Output("err", components[1], components[2]))
                        error = True
                    else:
                        if components[1] == sign_max_incr.row:
                            another_search = filter_by_sign.remove(
                                sign_max_incr)
                            if len(filter_by_sign) != 0:
                                sign_max_incr_another = max(
                                    filter_by_sign, key=attrgetter('increment'))
                                output.append(
                                    Output(components[1], sign_max_incr_another.row, components[2]))
                            else:
                                output.append(
                                    Output("err", components[1], components[2]))
                                error = True
                        else:
                            output.append(
                                Output(components[1], sign_max_incr.row, components[2]))

        elif trimmed_line[0:11] == "OP_PRIDRUZI" or trimmed_line[0:5] == "KR_OD":
            green_light = False
            after_equal = True
        elif trimmed_line[0:5] == "KR_ZA":
            green_light = True  # currently code has come to part where we can
            # define the same variable again because it is for loop definition
            # when we receive "KR_OD" we can not do that anymore
            increment += 1
        elif trimmed_line[0:5] == "KR_AZ":
            defined = list(filter(lambda x: x.increment != increment, defined))
            increment -= 1
        elif trimmed_line[0:5] == "KR_OD":
            green_light = False

    treci_labos = []
    for element in output:
        treci_labos.append("{} {} {}".format(
            element.used, element.defined, element.sign))

    return treci_labos


def memory_funtion(treci_labos):
    memory = []
    index = 0
    v = "(V{})".format(index)
    for t in treci_labos:
        elements = t.split()
        definition = elements[1]
        sign = elements[2]
        flag = False
        for m in memory:
            if m.sign == sign and m.rowOfDefinition == definition:
                flag = True
        if not flag:
            m = Memory(sign, definition, v)
            memory.append(m)
            index = index+1
            v = "(V{})".format(index)
    return memory


def handleLoadingNumber(number):
    return """
\tMOVE %D {}, R0
\tPUSH R0""".format(number)


def handleLoadingFromAddress(address):  # NE LOADA S LOKACIJE
    return """
\tLOAD R0, {}
\tPUSH R0""".format(address)


def handleAdd():
    return """
\tPOP R1
\tPOP R0
\tADD R0, R1, R2
\tPUSH R2"""


def handleSub():
    return """
\tPOP R0
\tPOP R1
\tSUB R0, R1, R2
\tPUSH R2"""


def handleMulWithMinusOne():
    return """\n\tPOP R0""" + handleLoadingNumber("-1") + """\n\tCALL MULL"""


def handleMul():
    return """
\tCALL MUL"""


def handleDiv():
    return """
\tPOP R0
\tPOP R1
\tPUSH R0
\tPUSH R1
\tCALL DIV"""


def handleStoring(save_to):
    return """
\tPOP R0
\tSTORE R0, {}""".format(save_to)


def handleLoop(no_petlja):
    return """
L{}""".format(no_petlja)


def handleIncrement(address):
    return """
\tLOAD R0, {}
\tADD R0, 1, R0
\tSTORE R0, {}
""".format(address, address)


def handleJump(address, no_petlja):
    return """
\tLOAD R0, {}
\tPOP R1
\tCMP R0, R1
\tJP_SLE L{}""".format(address, no_petlja)


def handleSubMethods():
    return """
\nMD_SGN MOVE 0, R6
    XOR R0, 0, R0
    JP_P MD_TST1
    XOR R0, -1, R0
    ADD R0, 1, R0
    MOVE 1, R6
MD_TST1 XOR R1, 0, R1
    JP_P MD_SGNR
    XOR R1, -1, R1
    ADD R1, 1, R1
    XOR R6, 1, R6
MD_SGNR RET
MD_INIT POP R4 ; MD_INIT ret addr
    POP R3 ; M/D ret addr
    POP R1 ; op2
    POP R0 ; op1
    CALL MD_SGN
    MOVE 0, R2 ; init rezultata
    PUSH R4 ; MD_INIT ret addr
    RET
MD_RET XOR R6, 0, R6 ; predznak?
    JP_Z MD_RET1
    XOR R2, -1, R2 ; promijeni predznak
    ADD R2, 1, R2
MD_RET1 POP R4 ; MD_RET ret addr
    PUSH R2 ; rezultat
    PUSH R3 ; M/D ret addr
    PUSH R4 ; MD_RET ret addr
    RET
MUL CALL MD_INIT
    XOR R1, 0, R1
    JP_Z MUL_RET ; op2 == 0
    SUB R1, 1, R1
MUL_1 ADD R2, R0, R2
    SUB R1, 1, R1
    JP_NN MUL_1 ; >= 0?
MUL_RET CALL MD_RET
    RET
DIV CALL MD_INIT
    XOR R1, 0, R1
    JP_Z DIV_RET ; op2 == 0
DIV_1 ADD R2, 1, R2
    SUB R0, R1, R0
    JP_NN DIV_1
    SUB R2, 1, R2
DIV_RET CALL MD_RET
    RET\n"""


def handleDW(address):
    return """
{} DW 0""". format(address)


def handleHalt(address):
    return """
\n\tLOAD R6, {}
\tHALT\n""".format(address)


def isOperator(c):
    return (not (c >= 'a' and c <= 'z') and not(c >= '0' and c <= '9') and not(c >= 'A' and c <= 'Z') and not (c == "'"))


def getPriority(C):
    if (C == '-' or C == '+'):
        return 1
    elif (C == '*' or C == '/'):
        return 2
    elif (C == '^'):
        return 3
    return 0


def infixToPrefix(infix):
    operators = []
    variable = ""
    operands = []
    sign = ""

    for i in range(len(infix)):
        if (infix[i] == '('):
            operators.append(infix[i])

        elif (infix[i] == ')'):
            if variable != "":
                operands.append(variable + "")
                variable = ""
            while (len(operators) != 0 and operators[-1] != '('):
                op1 = operands[-1]
                operands.pop()
                op2 = operands[-1]
                operands.pop()
                op = operators[-1]
                operators.pop()
                tmp = op + op2 + op1
                operands.append(tmp)
            operators.pop()

        elif (not isOperator(infix[i])):
            #operands.append(infix[i] + "")
            if i + 1 < len(infix):
                if sign != "" and infix[i] == "'":
                    variable = infix[i] + sign
                    sign = ""
                else:
                    variable = variable + infix[i]
            else:
                variable = variable + infix[i]
                operands.append(variable + "")

        else:
            if variable != "":
                operands.append(variable + "")
                variable = ""
            bool = True

            if infix[i] == "-" or infix[i] == "+":
                if i == 0 or infix[i-1] == "+" or infix[i-1] == "-" or infix[i-1] == "/" or infix[i-1] == "*" or infix[i-1] == "(" or infix[i-1] == "=" or infix[i-1] == " ":
                    sign = infix[i]
                    bool = False
            if bool:
                while (len(operators) != 0 and getPriority(infix[i]) <= getPriority(operators[-1])):
                    op1 = operands[-1]
                    operands.pop()
                    op2 = operands[-1]
                    operands.pop()
                    op = operators[-1]
                    operators.pop()
                    tmp = op + op2 + op1
                    operands.append(tmp)

                operators.append(infix[i])
    while (len(operators) != 0):
        op1 = operands[-1]
        operands.pop()
        op2 = operands[-1]
        operands.pop()
        op = operators[-1]
        operators.pop()
        tmp = op + op2 + op1
        operands.append(tmp)

    infix = operands[-1]

    list_1 = infix.split("'")
    list = []
    for l in list_1:
        if(l == ""):
            pass
        elif (len(l) > 1):
            if("*" == l[1] or "/" == l[1] or "+" == l[1] or "-" == l[1]):
                for i in l:
                    list.append(i)
            else:
                list.append(l)
        else:
            list.append(l)
    return list


def convert_to_prefix(str):
    lista = infixToPrefix(str)
    lista.reverse()
    return lista


def desna_strana(naredbe, memory, treci_rezultat):
    code = ""
    lokacije = []
    infix = ""
    for n in naredbe:
        elms = n.split()
        if ("IDN" in n):
            infix = infix + "'" + elms[2] + "'"
            rowOfAppearing = elms[1]
            lokacija = Memory()
            row = ""
            for t in treci_rezultat:
                a = t.split()
                if(a[0] == rowOfAppearing and a[2] == elms[2]):
                    row = a[1]
                    break
            for m in memory:  # provjeri !!!!!
                if(m.sign == elms[2] and m.rowOfDefinition == row):
                    lokacija = m
                    break
            lokacije.append(lokacija)
        elif("BROJ" in n):
            infix = infix + "'" + elms[2] + "'"
        elif("OP_MINUS" in n):
            infix = infix + "-"
        elif("OP_PLUS" in n):
            infix = infix + "+"
        elif("OP_PUTA" in n):
            infix = infix + "*"
        elif("OP_DIJELI" in n):
            infix = infix + "/"
        elif("L_ZAGRADA" in n):
            infix = infix + "("
        elif("D_ZAGRADA" in n):
            infix = infix + ")"
    prefix = []
    pom = infix.split("'")
    list = []
    for l in pom:
        if(l == ""):
            pass
        elif("*" in l or "/" in l or "+" in l or "-" in l):
            for i in l:
                list.append(i)
        else:
            list.append(l)
    if(len(list) == 1):
        prefix.append(list[0])
    else:
        prefix = convert_to_prefix(infix)

    for el in prefix:
        bez_prvog = el[1:]
        if(el.isdigit() or bez_prvog.isdigit()):
            code = code + handleLoadingNumber(el)
        elif(el == "*"):
            code = code + handleMul()
        elif(el == "/"):
            code = code + handleDiv()
        elif(el == "+"):
            code = code + handleAdd()
        elif(el == "-"):
            code = code + handleSub()
        else:  # IDN
            predznak = ""
            if(not el[0].isalpha()):
                predznak = el[0]
                el = bez_prvog
            address = ""
            for l in lokacije:
                if(l.sign == el):
                    address = l.address
            code = code + handleLoadingFromAddress(address)
            if predznak == "-":
                code = code + handleMulWithMinusOne()

    return code


def find_by_sign_and_row(sign, row, memory):
    for m in memory:
        if(m.sign == sign and m.rowOfDefinition == row):
            return m
    return None


def find_by_sign(sign, memory):
    for m in memory:
        if(m.sign == sign):
            return m
    return None


def od_do_petlja(naredbe, memory, no_petlja, treci_rezultat):
    naredbe.reverse()
    od = naredbe.pop().split()
    naredbe.reverse()
    m = find_by_sign_and_row(od[2], od[1], memory)
    od_flag = False
    od_naredbe = []
    do_naredbe = []
    for n in naredbe:
        if("KR_OD" in n):
            od_flag = True
        elif("KR_DO" in n):  # obradi iterator
            od_flag = False
        elif(od_flag):
            od_naredbe.append(n)
        else:
            do_naredbe.append(n)
    od_rezultat = desna_strana(od_naredbe, memory, treci_rezultat) + \
        handleStoring(m.address) + handleLoop(no_petlja)
    do_rezultat = handleIncrement(
        m.address) + desna_strana(do_naredbe, memory, treci_rezultat) + handleJump(m.address, no_petlja)
    return od_rezultat, do_rezultat


def inspect(lines, memory, treci_rezultat):
    frisc_code = """
\tMOVE 40000, R7
    """
    naredbe = []
    naredbe_petlje = []
    pridruzivanje = False
    petlja = False
    no_petlje = []
    global_no_petlje = -1
    petlje = []
    save_to = ""
    for i in range(len(lines)):
        line = lines[i]

        # handle pridruzivanje

        # a u petlji ne mora biti i nista
        if("IDN" in line and "<naredba_pridruzivanja>" in lines[i-1]):
            if(petlja):
                petlja = False
                if(len(no_petlje) == 0):
                    no_petlje.append(global_no_petlje)
                else:
                    no_petlje.append(global_no_petlje+1)
                od_code, do_code = od_do_petlja(
                    naredbe_petlje, memory, no_petlje[len(no_petlje)-1], treci_rezultat)
                petlje.append(do_code)
                frisc_code = frisc_code + od_code
                naredbe_petlje = []
            pridruzivanje = True
            elms = line.split()
            rowAppearing = elms[1]
            lokacija = None
            for m in memory:
                if(m.sign == elms[2] and m.rowOfDefinition == rowAppearing):  # provjeri!!!!!!
                    lokacija = m
                    break
            if(lokacija == None):
                lokacija = find_by_sign(elms[2], memory)
            save_to = lokacija.address
        elif("<lista_naredbi>" in line and pridruzivanje):  # ili je kraj -> nanodaj taj uvjet
            frisc_code = frisc_code + \
                desna_strana(naredbe, memory, treci_rezultat)
            frisc_code = frisc_code + handleStoring(save_to)
            naredbe = []
            pridruzivanje = False
        elif(pridruzivanje and "<" not in line and "$" not in line):
            naredbe.append(line)
        elif("KR_ZA" in line):
            global_no_petlje += 1
            petlja = True
        elif(petlja and "<" not in line and "$" not in line):
            naredbe_petlje.append(line)
        elif("KR_AZ" in line):  # stavi cmp i skok na petlju
            frisc_code = frisc_code + petlje.pop()
            no_petlje.pop()

    return frisc_code


def main():
    file = sys.stdin
    lines = file.read().split('\n')
    file.close()
    treci_rezultat = treci(lines)
    memory = memory_funtion(treci_rezultat)
    flag = True
    for m in memory:
        if(m.sign == "rez"):
            flag = False
    if(flag):  # nema rez u memoriji
        memory.append(Memory("rez", "1", "(V{})".format(len(memory))))

    frisc = inspect(lines, memory, treci_rezultat)
    rez = find_by_sign("rez", memory)
    frisc = frisc + handleHalt(rez.address)
    frisc = frisc + handleSubMethods()
    for m in memory:
        address = m.address[1:-1]
        frisc = frisc + handleDW(address)
    file = open("a.frisc", "w")
    file.write(frisc)
    file.close()


main()
