import sys
import csv
import keyboard
from selenium import webdriver
from docx import Document

def driver_launch():
    global driver

    if sys.platform == "win32": driver = webdriver.Chrome("lib/chromedriver.exe")
    if sys.platform == "darwin": driver = webdriver.Chrome("lib/chromedriver")

    driver.get("https://ordbok.uib.no/")

    return driver

def ordlister():
    global ordliste_nynorsk, ordliste_bokmål, ordliste_feil

    with open("lib/ordliste_nynorsk.txt") as file:
        ordliste_nynorsk = file.read().split("\n")

    with open("lib/ordliste_bokmål_eksklusiv.txt") as file:
        ordliste_bokmål = file.read().split("\n")

    with open("lib/ordliste_språkrådet.csv") as file:
        reader = csv.reader(file, delimiter=';')
        ordliste_feil = [row for row in reader if row[0] != ""]

    with open("lib/ordliste_user.csv") as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row[0] != "":
                ordliste_feil.append(row)

    return ordliste_nynorsk, ordliste_bokmål, ordliste_feil

def document_get_text(doc):
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return " ".join(text)

def check_grammar(words, web = False, print_all = True):
    if not (words[0] + " ").isspace():
        for word in words:
            output = ""

            if word in ordliste_bokmål:
                output += word + " || bokmålsord\n"

            word_spaced = " " + word.lower() + " "

            for feil in ordliste_feil:
                if feil[0].replace("_", " ").replace("-", "") in word_spaced:
                    if feil[0] and word_spaced.replace(feil[0], "").isspace():
                        pass
                    else:
                        output += word + " (" + feil[0] + ") ||" + feil[1] + "\n"

            for i in range(len(word) + 1, 0, -1):
                if word[:i].lower() in ordliste_nynorsk or word[:i] in ordliste_nynorsk:
                    if web:
                        driver.find_element_by_id("felt").send_keys(word)
                        driver.find_element_by_id("knappbegge").click()
                        output += driver.find_element_by_xpath('//*[@id="kolonnenn"]').text + "\n"

                    elif print_all or i < len(word):
                        output += "<" + word[:i] + "> i ordlista\n"

                    break

            if print_all or output != "":
                print("WORD: <" + word + ">\n" + output)
