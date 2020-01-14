from lib.lib import *

ordliste_nynorsk, ordliste_bokmål, ordliste_feil = ordlister()

filename = "C:/Users/Magne Tenstad/Desktop/same.docx"#input("input path:")

text = ""

if ".txt" in filename:
    with open(filename, "r") as file:
        text = file.read()
elif ".docx" in filename:
    document = Document(filename)
    text = document_get_text(document)

text = "".join((char for char in text if char.isalpha() or char == " "))

words = [word for word in text.split()]

check_grammar(words, print_all = False)

input()
