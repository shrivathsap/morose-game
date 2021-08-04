import winsound, time

dit_dah = {".":(3000, 500),
          "-": (3000, 1500)}


morse_phrase = "... --- ..."

for moo in morse_phrase:
    print(moo)
    if moo == ' ':
        time.sleep(0.4)
    else:
        winsound.Beep(dit_dah[moo][0], dit_dah[moo][1])
