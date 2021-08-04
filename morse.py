morse_dict = {"a":".-",
              "b":"-...",
              "c":"-.-.",
              "d":"-..",
              "e":".",
              "f":"..-.",
              "g":"--.",
              "h":"....",
              "i":"..",
              "j":".---",
              "k":"-.-",
              "l":".-..",
              "m":"--",
              "n":"-.",
              "o":"---",
              "p":".--.",
              "q":"--.-",
              "r":".-.",
              "s":"...",
              "t":"-",
              "u":"..-",
              "v":"...-",
              "w":".--",
              "x":"-..-",
              "y":"-.--",
              "z":"--..",
              "1":".----",
              "2":"..---",
              "3":"...--",
              "4":"....-",
              "5":".....",
              "6":"-....",
              "7":"--...",
              "8":"---..",
              "9":"----.",
              "0":"-----"
    }

def reverse_dict(dictionary):
    new_dict = {}
    for key in dictionary.keys():
        value = dictionary[key]
        new_dict[value] = key

    return new_dict

char_dict = reverse_dict(morse_dict)

def convert_to_morse(string):
    lower_string = string.lower()
    morse = ""
    for char in lower_string:
        try:
            morse += morse_dict[char]
            morse += ' '
        except:
            #morse += char
            morse += ' '#space when character is not identified?

    return morse

def convert_to_string(morse_code):#just so you know, spaces are necessary
    msg = ""
    for string in morse_code.split(' '):
        try:
            msg += char_dict[string]
        except:
            msg += ''
        msg += ' '

    return msg

def check(morse_input):
    letters = morse_input.split(' ')
    for item in letters:
        if len(item)>5 or item not in char_dict.keys():
            return False
    return True
        

def main_control():
    mode = input("Enter 0 to convert from morse to text, and 1 to convert from text to morse: ")
    while mode != '0' and mode != '1':
        mode = input("Enter 0 to convert from morse to text, and 1 to convert from text to morse: ")

    if mode == '0':
        morse_input = input("Enter morse code:")
        while not check(morse_input):
            morse_input = input("One or more letters entered where incorrect, please re-enter: ")
        print("You entered: ", morse_input)
        print(convert_to_string(morse_input))
    else:
        text_input = input("Enter text:")
        print("You entered: ", text_input)
        print(convert_to_morse(text_input))

if __name__ == "__main__":
    main_control()
