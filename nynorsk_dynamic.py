import csv
import keyboard
from docx import Document

def getText(doc):
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return " ".join(fullText)

debug = True

with open("nynorsk.csv") as file:
    reader = csv.reader(file, delimiter=';')
    dictionary = [row for row in reader if row[0] != ""]

with open("bokmålsord.txt") as file:
    bokmålsord = file.read().split()

with open("ordliste_nynorsk.txt") as file:
    ordliste_nynorsk = file.read().split()

supplements = [("_jeg_","eg"), ("_hun_","ho"), ("_en_","ein"), ("_et_","eit"), ("_man_","ein"), ("_noe_","noko"), ("_noen_","nokon, noka, noko, nokre"), ("_de_","dei"), ("_dere_","de/dykk"), ("_dem_","dei"), ("lig_","-leg (anbehetelser)"), ("-het_","-heit (anbehetelser)"), ("_an-","anbehetelser"), ("_be-","anbehetelser"), ("-else_","-ing, (anbehetelser)"), ("_hv-","kv-"), ("-vn_", "-mn"), ("-som_","-sam"), ("-ende_","-ande"), ("-ere_", "-are (gradbøying)"), ("-est_", "-ast (gradbøying)"), ("_ikke_", "ikkje"), ("_ble_", "blei, vart"), ("-s_", "(genetiv)")]

for sup in supplements:
    dictionary.append(sup)

run = True

def end():
    run = False

keyboard.add_hotkey('esc', lambda: end())

while run:
    words = []

    for string in keyboard.get_typed_strings(keyboard.record(until='space'), allow_backspace = True):
        string = string.replace(",", "").replace(".", "").replace("!", "").replace("?", "").replace(":", "")

        if string.count(" ") > 1:
            for s in string.split():
                words.append(s)
        else:
            words.append(string)

    for word in words:
        print()
        print("WORD: ", word)

        i = len(word) + 1
        while len(word[:i]):
            if word[:i] in ordliste_nynorsk or word[:i].lower() in ordliste_nynorsk:
                break
            i -= 1

        comment = ""

        if len(word[:i]):
            comment = ", <" + word[:i] + "> er i ordlista"

        if i < len(word):
            print(word + comment)

        wrong = False

        if word in bokmålsord:
            wrong = True
            print(word, " || bokmålsord")

        word_spaced = " " + word + " "

        for i in range(len(dictionary)):
            wrong = True
            check = dictionary[i][0].replace("_", " ").replace("-", "")
            if check in word_spaced.lower():
                if dictionary[i][0].count("-") and word_spaced.replace(check, "").isspace():
                    pass
                else:
                    print(word, "(", dictionary[i][0], ") ||", dictionary[i][1])
