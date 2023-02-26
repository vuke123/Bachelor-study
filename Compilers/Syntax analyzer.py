import sys

file = open("lexicon.txt", "r")
lines = file.readlines()

primjeni = {"<program>":  [["IDN", "KR_ZA", "end"]],
            "<lista_naredbi>": [["IDN", "KR_ZA"], ["KR_AZ", "end"]],
            "<naredba>": [["IDN"], ["KR_ZA"]],
            "<naredba_pridruzivanja>": [["IDN"]],
            "<za_petlja>": [["KR_ZA"]],
            "<E>": [["IDN", "BROJ", "OP_PLUS", "OP_MINUS", "L_ZAGRADA"]],
            "<E_lista>": [["OP_PLUS"], ["OP_MINUS"], ["IDN", "KR_ZA", "KR_AZ", "KR_DO", "D_ZAGRADA", "end"]],
            "<T>": [["IDN", "BROJ", "OP_PLUS", "OP_MINUS", "L_ZAGRADA"]],
            "<T_lista>": [["OP_PUTA"], ["OP_DIJELI"], ["IDN", "KR_ZA", "KR__AZ", "OP_PLUS", "OP_MINUS", "D_ZAGRADA", "end"]],
            "<P>": [["OP_PLUS"], ["OP_MINUS"], ["L_ZAGRADA"], ["IDN"], ["BROJ"]]
            }

produkcije = {"<program>": [["<lista_naredbi>"]],
              "<lista_naredbi>": [["<naredba>", "<lista_naredbi>"], ["epsilon"]],
              "<naredba>": [["<naredba_pridruzivanja"], ["za_petlja"]],
              "<naredba_pridruzivanja>": [["IDN", "OP_PRIDRUZI", "<E>"]],
              "<za_petlja>": [["KR_ZA", "IDN", "KR_OD", "<E>", "KR_DO", "<E>", "<lista_naredbi>", "KR_AZ"]],
              "<E>": [["<T>", "<E_lista>"]],
              "<E_lista>": [["OP_PLUS"], ["OP_MINUS"], ["epsilon"]],
              "<T>": [["<P>", "<T_lista>"]],
              "<T_lista>": [["OP_PUTA", "<T>"], ["OP_DIJELI", "<T>"], ["epsilon"]],
              "<P>": [["OP_PLUS"], ["OP_MINUS"], ["L_ZAGRADA", "D_ZAGRADA"], ["IDN"], ["BROJ"]]
              }
ispis = []
i = 0
stog = []
stog.append("<program>")
stog.append(0)
error = False

while i < len(lines) and error == False:
    cijeli_znak = []
    cijeli_znak = lines[i].split(" ")
    tip = cijeli_znak[0]
    red = cijeli_znak[1]
    znak = cijeli_znak[2]

    vrh_stoga = stog[len(stog)-2]

    if vrh_stoga[0] != '<':
        if vrh_stoga == tip:
            razina = stog.pop()
            stog.pop()
            ispis.append(razina*" " + tip + " " + red + " " + znak)
            i += 1
        else:
            print("err " + tip + " " + red + " " + znak)
            error = True
    else:
        indeks_produkcije = -1
        for j, primjeni_skup in enumerate(primjeni.get(vrh_stoga)):
            if tip in primjeni_skup:
                indeks_produkcije = j
        if indeks_produkcije != -1:
            novo = produkcije.get(vrh_stoga)[indeks_produkcije]
            if novo[0] == "epsilon":
                razina = stog.pop()
                staro = stog.pop()
                ispis.append(razina*" " + staro)
            else:
                novoReverse = novo[::-1]
                razina = stog.pop()
                staro = stog.pop()
                for stanje in novoReverse:
                    stog.append(stanje)
                    stog.append(razina + 1)
                ispis.append(razina*" " + staro)

        else:
            print("err " + tip + " " + red + " " + znak)
            error = True

if error == False:
    for linija in ispis:
        print(linija)


# 1) stog append ( {vrijednost: razina:})
# 2) if len(stog) == 0 a još imamo ulaznih, prekini odbaci
# 3) break i continue di treba doradi
