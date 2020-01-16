from lib.lib import *

ordlister_init()

restart()

while 1:
    words = []

    for string in keyboard.get_typed_strings(keyboard.record(until = 'space'), allow_backspace = True):
        string = "".join((char for char in string if char.isalpha() or char == " "))

        if string.count(" "):
            for word in string.split():
                words.append(word)
                if word == "rx": restart()
        else:
            words.append(string)
            if string == "rx": restart()

    check_grammar(words)
