import sys
from operator import attrgetter

#file = open("syntax.txt", "r")
#lines = file.readlines()


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

for line in sys.stdin:

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
                    output.append(Output("err", components[1], components[2]))
                    error = True
                else:
                    if components[1] == sign_max_incr.row:
                        another_search = filter_by_sign.remove(sign_max_incr)
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

for element in output:
    print(element.used + " " + element.defined + " " + element.sign)
