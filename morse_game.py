from morse import *
from bs4 import BeautifulSoup
import requests, urllib.request
from tkinter import *
from tkinter import scrolledtext, messagebox #somehow doesn't come with *
import random, time, winsound
from threading import *

bg = "black"
fg = "green"
exitflag = False
unit = 0.05#sleep time is a bit of a mess, see play function
dit_dah = {".":(700, int(1000*unit)),
          "-": (700, int(3000*unit))}

def raise_frame(frame):
    frame.tkraise()

def get_quote():#takes about 2.3 seconds to scrape quote. CAUTION: there are some arabic quotes on goodreads....
    page_no = str(random.randint(1, 100))
    quotes_url = f"https://www.goodreads.com/quotes?page={page_no}"
    #parse html etc, usual stuff
    source = requests.get(quotes_url).text
    soup = BeautifulSoup(source, 'lxml')

    #this is where the quotes are stored, pick one randomly
    quotes = soup.find_all('div', class_ = 'quoteText')
    quote = random.choice(quotes)

    #so, the quotes stard and end with a new line or something, hopefully this works, not completely sure why
    saying = quote.text.split('\n')[1].strip()#strip to remove leading and trailing whitespaces
    author = quote.find('span', class_ = 'authorOrTitle').text.split('\n')[1]#end with space instead of newline
    try:#some quotes are not from books
        book = quote.find('a', class_ = 'authorOrTitle').text
    except:
        book = None

    return saying, author, book


def get_quest(text_box, morse):#quest is short for question, sounds cooler
    quote, author, book = get_quote()

    if morse == True:
        quote = convert_to_morse(quote)

    try:
        text_box.delete(1.0, END)
        text_box.insert(1.0, quote+'\n\n\n')
        text_box.insert(INSERT, author+' ')
        if book != None:
            text_box.insert(INSERT, book)
    except:#if user closes root before t1, t2 terminate, it throws an error, because text_box no longer exists
        pass

def check_soln(text1, text2, mode, verdict_box):
    quote = text1.get(1.0, END).split('\n')[0]
    if mode == "code":
        try:
            quote = convert_to_morse(quote).strip().split(' ')#remover trailing white spaces
            answer = text2.get(1.0, END)[:-1].split(' ')#there's this newline character or something, so remove that
            quote = [item for item in quote if (item != ' ' and item != '')]
            answer = [item for item in answer if (item != ' ' and item != '')]
        except:
            verdict_box.delete(1.0, END)
            verdict_box.insert(1.0, "Wrong")
    elif mode == "decode":
        try:
            answer = text2.get(1.0, END)[:-1].replace(" ", "")
            quote = convert_to_string(quote).strip().replace(" ", "")#remove all spaces, that way we don't care how the user enters
        except Exception as e:
            print(e)
            verdict_box.delete(1.0, END)
            verdict_box.insert(1.0, "Wrong")
    else:
        pass
##    print(quote, len(quote))
##    print(answer, len(answer))
    if quote == answer:
        verdict_box.delete(1.0, END)
        verdict_box.insert(1.0, "Correct")
    else:
        verdict_box.delete(1.0, END)
        verdict_box.insert(1.0, "Wrong")

def get_soln(text1, mode, verdict_box):
    quote = text1.get(1.0, END).split('\n')[0]
    if mode == "code":
        verdict_box.delete(1.0, END)
        verdict_box.insert(1.0, convert_to_morse(quote))
    elif mode == "decode":
        verdict_box.delete(1.0, END)
        verdict_box.insert(1.0, convert_to_string(quote))
    else:
        pass


##to_play, author, book = get_quote()

def update_to_play(text_box):
    global to_play, author, book
    to_play, author, book = get_quote()
    try:
        text_box.delete(2.0, END)
        text_box.insert(INSERT, '\n'+author+' ')
        if book != None:
            text_box.insert(INSERT, book)
    except:
        pass
    
def check_soln_transcribe(quote_to_play, soln_text_box, verdict_box):
    correct_soln = convert_to_morse(quote_to_play).split(' ')
    correct_soln = [item for item in correct_soln if (item != ' ' and item != '')]

    entered_soln = soln_text_box.get(1.0, END)[:-1].split(' ')
    entered_soln = [item for item in entered_soln if (item != ' ' and item != '')]

    if correct_soln == entered_soln:
        verdict_box.delete(1.0, END)
        verdict_box.insert(1.0, "Correct")
    else:
        verdict_box.delete(1.0, END)
        verdict_box.insert(1.0, "Wrong")

def get_soln_transcribe(quote_to_play, verdict_box):
    verdict_box.delete(1.0, END)
    verdict_box.insert(1.0, convert_to_morse(quote_to_play))
    verdict_box.insert(INSERT, '\n'+quote_to_play)

def play():
##    morse_phrase = convert_to_morse(to_play).strip()
    for char in to_play.lower():
        if not exitflag:#see if exitflag is true or not
            if char in morse_dict.keys():
                moo = morse_dict[char]
                for di_da in moo:
                    winsound.Beep(dit_dah[di_da][0], dit_dah[di_da][1])
                    time.sleep(unit)#one unit between dots and dashes
            elif char == ' ':
                time.sleep(7*unit)#7 units between words
            else:
                time.sleep(unit)
        time.sleep(3*unit)#three unit between letters

def play_thread():
    t = Thread(target = play)
    t.start()#start the thread, no need to end it
    
    
root = Tk()
root.geometry("700x415")
root.title("The Morse Code Game")
root.call('wm', 'iconphoto', root._w, PhotoImage(file='C:\Python\My Programs\Morse\icon.png'))

def on_quit():
    global exitflag, root
    #code used to confirm exit, so as to buy time to finish threads, but realised flaw elsewhere
##    #a cheat, this seems to take just the right amount of time for t1, t2, t3 to terminate, but not completely satisfactory
##    if messagebox.askokcancel("Quit", "Do you want to quit?", default = 'cancel'):#change default so that the user will not hit enter and break it
    exitflag = True
    root.destroy()
    

root.protocol("WM_DELETE_WINDOW", on_quit)#upon closing this function is followed

#frames
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)

home = Frame(root)
code = Frame(root)
decode = Frame(root)
transcribe = Frame(root)
about = Frame(root)

#doing this means no need to pack the frames, basically put all the frames in the same place and then stretch them using sticky
for frame in (home, decode, code, transcribe, about):
    for i in range(12):
        frame.columnconfigure(i, weight = 1)
    for i in range(10):
        frame.rowconfigure(i, weight = 1)
    frame.grid(row=0, column=0, sticky='news')
    
#homepage
welcome_msg = Text(home, bg = "black", fg = "green", height = 6, font = ("Courier", 12))
welcome_msg.insert(INSERT, '''Welcome! All our quotes are taken from https://www.goodreads.com/quotes.
The goal of this game is for you to practice morse code, decoding and so on blah blah.
\nCode page: Convert the given quote to morse. Just the quote, not the author and book. Skip punctuation marks.
\nDecode page: Convert morse to text, again, only the morse code part.
\nTranscribe page: Click the play button, transcribe. Upon closing, you may hear the last character being relayed, it's not a but, it's a feature.
\nAbout page: About page''')
welcome_msg.grid(row = 0, column = 0, columnspan = 12, rowspan = 9, sticky = 'news')

code_button = Button(home, text = "Code", command = lambda:raise_frame(code),
                     bg = bg, fg = fg, font = ("Courier", 12)).grid(row = 9, column = 0, columnspan = 3, sticky = 'news')
decode_button = Button(home, text = "Decode", command = lambda:raise_frame(decode),
                       bg = bg, fg = fg, font = ("Courier", 12)).grid(row = 9, column = 3, columnspan = 3, sticky = 'news')
transcribe_button = Button(home, text = "Transcribe", command = lambda:raise_frame(transcribe),
                           bg = bg, fg = fg, font = ("Courier", 12)).grid(row = 9, column = 6, columnspan = 3, sticky = 'news')
about_button = Button(home, text = "About", command = lambda:raise_frame(about),
                           bg = bg, fg = fg, font = ("Courier", 12)).grid(row = 9, column = 9, columnspan = 3, sticky = 'news')

#code page
code_label = Label(code, text = "This is the code page", bg = bg, fg = fg, height = 2, font = ("Courier", 12)).grid(row = 0, columnspan = 12, sticky = 'news')

plain_text = scrolledtext.ScrolledText(code, bg = bg, fg = fg, wrap = WORD)
plain_text.grid(row = 1, column = 0, rowspan = 8, columnspan = 6, sticky = 'news')

sol_text_plain = Text(code)
sol_text_plain.grid(row = 1, column = 6, rowspan = 8, columnspan = 6, sticky = 'news')

code_verdict = scrolledtext.ScrolledText(code, bg = bg, fg = fg, height = 7, wrap = WORD)
code_verdict.grid(row = 10, column = 0, columnspan = 12, sticky = 'news')

home_code = Button(code, text = "Back", bg = bg, fg = fg, command = lambda:raise_frame(home), font = ("Courier", 12), height = 2)
home_code.grid(row = 9, column = 0, columnspan = 3, sticky = 'news')
check_code = Button(code, text = "Check", bg = bg, fg = fg, command = lambda:check_soln(plain_text, sol_text_plain, "code", code_verdict),
                    font = ("Courier", 12), height = 2)
check_code.grid(row = 9, column = 3, columnspan = 3, sticky = 'news')
reveal_code = Button(code, text = "Reveal", bg = bg, fg = fg, command = lambda:get_soln(plain_text, "code", code_verdict), font = ("Courier", 12), height = 2)
reveal_code.grid(row = 9, column = 6, columnspan = 3, sticky = 'news')
next_code = Button(code, text = "Next", bg = bg, fg = fg, command = lambda:get_quest(plain_text, False), font = ("Courier", 12), height = 2)
next_code.grid(row = 9, column = 9, columnspan = 3, sticky = 'news')


#decode page
decode_label = Label(decode, text = "This is the decode page", bg = bg, fg = fg, height = 2, font = ("Courier", 12)).grid(row = 0, columnspan = 12, sticky = 'news')

morse_text = scrolledtext.ScrolledText(decode, bg = bg, fg = fg, wrap = WORD)
morse_text.grid(row = 1, column = 0, rowspan = 8, columnspan = 6, sticky = 'news')

sol_text_morse = Text(decode)
sol_text_morse.grid(row = 1, column = 6, rowspan = 8, columnspan = 6, sticky = 'news')

decode_verdict = scrolledtext.ScrolledText(decode, bg = bg, fg = fg, height = 7, wrap = WORD)
decode_verdict.grid(row = 10, column = 0, columnspan = 12, sticky = 'news')

home_decode = Button(decode, text = "Back", bg = bg, fg = fg, command = lambda:raise_frame(home), font = ("Courier", 12), height = 2)
home_decode.grid(row = 9, column = 0, columnspan = 3, sticky = 'news')
check_decode = Button(decode, text = "Check", bg = bg, fg = fg, command = lambda:check_soln(morse_text, sol_text_morse, "decode", decode_verdict),
                      font = ("Courier", 12), height = 2)
check_decode.grid(row = 9, column = 3, columnspan = 3, sticky = 'news')
reveal_decode = Button(decode, text = "Reveal", bg = bg, fg = fg, command = lambda:get_soln(morse_text, "decode", decode_verdict), font = ("Courier", 12), height = 2)
reveal_decode.grid(row = 9, column = 6, columnspan = 3, sticky = 'news')
next_decode = Button(decode, text = "Next", bg = bg, fg = fg, command = lambda:get_quest(morse_text, True), font = ("Courier", 12), height = 2)
next_decode.grid(row = 9, column = 9, columnspan = 3, sticky = 'news')


#transcribe page
transcribe_label = Label(transcribe, text = "This is the transcribe page", bg = bg, fg = fg, height = 2,
                         font = ("Courier", 12)).grid(row = 0, columnspan = 12, sticky = 'news')
morse_sound = Text(transcribe, bg = bg, fg = fg)
morse_sound.grid(row = 1, column = 0, rowspan = 8, columnspan = 6, sticky = 'news')
sol_sound = Text(transcribe)
sol_sound.grid(row = 1, column = 6, rowspan = 8, columnspan = 6, sticky = 'news')

transcribe_verdict = scrolledtext.ScrolledText(transcribe, bg = bg, fg = fg, height = 7, wrap = WORD)
transcribe_verdict.grid(row = 10, column = 0, columnspan = 12, sticky = 'news')

play_button = Button(morse_sound, text = "Play", bg = bg, fg = fg, command = lambda:play_thread())
morse_sound.window_create(END, window = play_button)

home_transcribe = Button(transcribe, text = "Back", bg = bg, fg = fg, command = lambda:raise_frame(home), font = ("Courier", 12), height = 2)
home_transcribe.grid(row = 9, column = 0, columnspan = 3, sticky = 'news')

check_transcribe = Button(transcribe, text = "Check", bg = bg, fg = fg, command = lambda:check_soln_transcribe(to_play, sol_sound, transcribe_verdict),
                      font = ("Courier", 12), height = 2)
check_transcribe.grid(row = 9, column = 3, columnspan = 3, sticky = 'news')

reveal_transcribe = Button(transcribe, text = "Reveal", bg = bg, fg = fg, command = lambda:get_soln_transcribe(to_play, transcribe_verdict),
                           font = ("Courier", 12), height = 2)
reveal_transcribe.grid(row = 9, column = 6, columnspan = 3, sticky = 'news')

next_transcribe = Button(transcribe, text = "Next", bg = bg, fg = fg, command = lambda:update_to_play(morse_sound), font = ("Courier", 12), height = 2)
next_transcribe.grid(row = 9, column = 9, columnspan = 3, sticky = 'news')

#about page
wall_of_text = '''Developed by : Hermes McBagel\nDeveloped with : Python 3.x \nDeveloped for : fun'''

about_text = Text(about, bg = bg, fg = fg, font = ("Courier", 14))
about_text.tag_configure("center", justify='center')
about_text.insert(INSERT, wall_of_text)
about_text.tag_add("center", "1.0", "end")

about_text.grid(row = 0, column = 0, columnspan = 12, rowspan = 9, sticky = 'news')

about_back = Button(about, text = "Back", bg = bg, fg = fg, command = lambda:raise_frame(home), font = ("Courier", 12), height = 2)
about_back.grid(row = 9, column = 0, columnspan = 12, sticky = 'news')


#start the program, just takes time to scrape stuff, oh well
t1 = Thread(target = get_quest, args = (plain_text, False,))
t2 = Thread(target = get_quest, args = (morse_text, True,))
t3 = Thread(target = update_to_play, args = (morse_sound,))
##for i in [t1, t2, t3]:
##    i.daemon = True
t1.start()
t2.start()
t3.start()
raise_frame(home)
root.mainloop()
