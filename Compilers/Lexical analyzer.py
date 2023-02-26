import sys
printing = False
string = ''
uniformChars = ''

index = 0

for line in sys.stdin:
    index += 1
    line = line.split('//')[0]
    for c in line:
        if c.isspace() and string != "":
            printing = True
        elif c.isalnum():
            string += c
        elif not c.isspace():
            if(c == '='):
                uniformChars = "OP_PRIDRUZI"
            elif(c == '-'):
                uniformChars = "OP_MINUS"
            elif(c == '+'):
                uniformChars = "OP_PLUS"
            elif(c == '*'):
                uniformChars = "OP_PUTA"
            elif(c == '/'):
                uniformChars = "OP_DIJELI"
            elif(c == '('):
                uniformChars = "L_ZAGRADA"
            elif(c == ')'):
                uniformChars = "D_ZAGRADA"
            if(string != ""):
                if(string[0].isalpha()):
                    uniformChars = "IDN"
                elif(string.charAt(0).isnumber()):
                    uniformChars = "BROJ"
                print(uniformChars + " " + str(index) + " " + string)
            string = c
            printing = True

        if printing:
            printing = False
            if(c == '='):
                uniformChars = "OP_PRIDRUZI"
            elif(c == '-'):
                uniformChars = "OP_MINUS"
            elif(c == '+'):
                uniformChars = "OP_PLUS"
            elif(c == '*'):
                uniformChars = "OP_PUTA"
            elif(c == '/'):
                uniformChars = "OP_DIJELI"
            elif(c == '('):
                uniformChars = "L_ZAGRADA"
            elif(c == ')'):
                uniformChars = "D_ZAGRADA"
            elif(string == "za"):
                uniformChars = "KR_ZA"
            elif(string == "od"):
                uniformChars = "KR_OD"
            elif(string == "do"):
                uniformChars = "KR_DO"
            elif(string == "az"):
                uniformChars = "KR_AZ"
            elif(string[0].isalpha()):
                uniformChars = "IDN"
            elif(string[0].isnumeric()):
                uniformChars = "BROJ"
            print(uniformChars + " " + str(index) + " " + string)
            string = ""
