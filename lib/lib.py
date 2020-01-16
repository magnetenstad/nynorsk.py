import sys
import csv
import keyboard
import time
from selenium import webdriver
from docx import Document

def restart():
    global web, conjugate
    web = False
    conjugate = False

    while web != "y" and web != "n":
        web = input("use web? (y/n)")
    web = web == "y"

    if web:
        while conjugate != "y" and conjugate != "n":
            conjugate = input("show cunjugation? (y/n)")
        conjugate = conjugate == "y"

        driver = driver_launch()

    print("thank you, you may start typing, write rx to restart\n")

def driver_launch():
    global driver

    if sys.platform == "win32": driver = webdriver.Chrome("lib/chromedriver.exe")
    if sys.platform == "darwin": driver = webdriver.Chrome("lib/chromedriver")

    driver.get("https://ordbok.uib.no/")

    return driver

def ordlister_init():
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

def check_grammar(words, print_all = True):
    for word in words:
        if not (word + " ").isspace():
            output = ""

            if word in ordliste_bokmål:
                output += "| BOKMÅLSORD! |\n"

            word_spaced = " " + word.lower() + " "

            for feil in ordliste_feil:
                if feil[0].replace("_", " ").replace("-", "") in word_spaced:
                    if feil[0] and word_spaced.replace(feil[0], "").isspace():
                        pass
                    else:
                        output += "(" + feil[0] + ") | " + feil[1] + " |\n"

            for i in range(len(word) + 1, 0, -1):
                if word[:i].lower() in ordliste_nynorsk or word[:i] in ordliste_nynorsk:
                    if web:
                        output += "\n<" + word[:i] + "> i ordboka:\n"
                        driver.find_element_by_id("felt").clear()
                        driver.find_element_by_id("felt").send_keys(word[:i])
                        driver.find_element_by_id("knappnn").click()

                        if conjugate:
                            conjugations = []

                            for button in driver.find_elements_by_class_name("oppsgramordklasse"):
                                driver.execute_script("arguments[0].click();", button)

                            time.sleep(0.02)

                            for window in driver.find_elements_by_class_name("paradigmetabell"):
                                while window.text.count("vent litt"):
                                    pass
                                conjugations.append(window.text)

                            for close in driver.find_elements_by_class_name("ui-dialog-titlebar-close"):
                                driver.execute_script("arguments[0].click();", close)

                            for content in conjugations:
                                content = content.replace("\n", " \n ").split(" ")
                                add = []
                                add_prev = False
                                forbidden_words = ["bunden", "form", "hankjønn", "og", "hokjønn", "perfektum", "partisipp"]

                                for i in range(1, len(content)):
                                    if ((content[i] + " ").isspace() and content[i] != "\n") or content[i][0].isupper() or (content[i] in forbidden_words and not add_prev):
                                        add_prev = False
                                    else:
                                        add.append(content[i])
                                        add_prev = True

                                output += " ".join(add) + "\n"

                    elif print_all or i < len(word):
                        output += "<" + word[:i] + "> i ordlista\n"

                    break

            if print_all or output != "":
                if print_all:
                    for i in range(50):
                        print("")
                print("[" + word + "]\n" + output + "\n")
