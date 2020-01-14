import csv
from docx import Document

def doc_get_text(doc):
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return " ".join(fullText)

debug = True

with open("ordliste_språkrådet.csv") as file:
    reader = csv.reader(file, delimiter=';')
    dictionary = [row for row in reader if row[0] != ""]

with open("ordliste_bokmål_eksklusiv.txt") as file:
    bokmålsord = file.read().split()

with open("ordliste_nynorsk.txt") as file:
    ordliste_nynorsk = file.read().split()

supplements = [("_jeg_","eg"), ("_hun_","ho"), ("_en_","ein"), ("_et_","eit"), ("_man_","ein"), ("_noe_","noko"), ("_noen_","nokon, noka, noko, nokre"), ("_de_","dei"), ("_dere_","de/dykk"), ("_dem_","dei"), ("lig_","-leg (anbehetelser)"), ("-het_","-heit (anbehetelser)"), ("_an-","anbehetelser"), ("_be-","anbehetelser"), ("-else_","-ing, (anbehetelser)"), ("_hv-","kv-"), ("-vn_", "-mn"), ("-som_","-sam"), ("-ende_","-ande"), ("-ere_", "-are (gradbøying)"), ("-est_", "-ast (gradbøying)"), ("_ikke_", "ikkje"), ("_ble_", "blei, vart"), ("-s_", "(genetiv)")]

for sup in supplements:
    dictionary.append(sup)

if debug:
    filename = "Heimeoppgåve.docx"
else:
    filename = input("input filename:")

text = ""

if ".txt" in filename:
    with open(filename, "r") as file:
        text = file.read()
elif ".docx" in filename:
    document = Document(filename)
    text = doc_get_text(document)

word_list = [word for word in text.replace(",", "").replace(".", "").split()]

print()
print("# Ikke i ordlista #")
print()

for word in word_list:
    i = len(word)
    while len(word[:i]):
        if word[:i] in ordliste_nynorsk or word[:i].lower() in ordliste_nynorsk:
            break
        i -= 1

    comment = ""

    if len(word[:i]):
        comment = ", <" + word[:i] + "> er i ordlista"

    if i < len(word):
        print(word + comment)

print()
print("# Annet #")
print()

for word in word_list:
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
