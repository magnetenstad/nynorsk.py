from lib.lib import *

ordliste_nynorsk, ordliste_bokmål, ordliste_feil = ordlister()

driver = driver_launch()

while 1:
    words = []

    for string in keyboard.get_typed_strings(keyboard.record(until = 'space'), allow_backspace = True):
        string = "".join((char for char in string[:-1] if char.isalpha() or char == " "))

        if string.count(" "):
            for word in string.split():
                words.append(word)
        else:
            words.append(string)

    check_grammar(words, web = True)
