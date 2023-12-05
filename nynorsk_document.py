from lib.lib import *
from docx import Document

ordlister_init()

filename = input("input path:")

text = ""

if ".txt" in filename:
    with open(filename, "r") as file:
        text = file.read()
elif ".docx" in filename:
    document = Document(filename)
    text = document_get_text(document)

text = "".join((char for char in text if char.isalpha() or char == " "))

words = text.split()

check_grammar(words, print_all = False)

input()
