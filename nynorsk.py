from lib.lib import *
import keyboard

ordlister_init()

web = ""
while web != "y" and web != "n":
    web = input("use web? (y/n)")
web = web == "y"

if web:
    driver_launch()

while 1:
    words = []

    for string in keyboard.get_typed_strings(keyboard.record(until = 'space'), allow_backspace = True):
        string = "".join((char for char in string if char.isalpha() or char == " "))

        if string.count(" "):
            for word in string.split():
                words.append(word)
        else:
            words.append(string)

    check_grammar(words, web = web)
