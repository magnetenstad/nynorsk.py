import sys
import csv
import time
from selenium import webdriver

def driver_launch():
    global driver

    if sys.platform == "win32": driver = webdriver.Chrome("lib/chromedriver.exe")
    if sys.platform == "darwin": driver = webdriver.Chrome("lib/chromedriver")

    driver.execute_script("window.open('about:blank', 'uib');")
    driver.switch_to.window("uib")
    driver.get("https://ordbok.uib.no/")
    driver.execute_script("window.open('about:blank', 'lexin');")
    driver.switch_to.window("lexin")
    driver.get("https://lexin.oslomet.no/#/findwords/message.bokmal-nynorsk")

    return driver

def ordlister_init():
    global ordliste_bokmål, ordliste_feil, ordliste_nynorsk

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
    for word in words:
        if not (word + " ").isspace():
            output = ""

            if word in ordliste_bokmål:
                output += "| BOKMÅLSORD |\n"

            word_spaced = " " + word.lower() + " "

            for feil in ordliste_feil:
                replaced = feil[0].replace("_", " ").replace("-", "")
                if replaced in word_spaced and not (feil[0].count("-") and word_spaced.replace(replaced, "").isspace()):
                    output += "(" + feil[0] + ") | " + feil[1] + " |\n"

            for i in range(len(word) + 1, 0, -1):
                if word[:i].lower() in ordliste_nynorsk or word[:i] in ordliste_nynorsk:
                    if print_all or i < len(word):
                        output += "<" + word[:i] + "> i ordlista\n"
                    break
                elif i < len(word) and (word[:i] + "e").lower() in ordliste_nynorsk:
                    if print_all or i < len(word):
                        output += "<" + word[:i] + "e> i ordlista\n"
                    break

            if web:
                _input = driver.find_element_by_class_name("form-input")
                while 1:
                    try:
                        _input.clear()
                        _input.send_keys(word + "\n")
                        try:
                            text = driver.find_element_by_xpath('//*[@id="fetchedText"]/div/ul/div/div/li[1]/div/div[2]').text
                            output += "<" + text + "> ifølge lexin\n"
                            driver.switch_to.window("uib")
                            driver.find_element_by_id("felt").clear()
                            driver.find_element_by_id("felt").send_keys(text)
                            driver.find_element_by_id("knappnn").click()
                            driver.switch_to.window("lexin")
                            break
                        except:
                            text = driver.find_element_by_xpath("//div[contains(text(), 'Ingen treff.')]")
                            break

                    except:
                         time.sleep(10**-6)

            if print_all or output != "":
                print("[" + word + "]\n" + output)
