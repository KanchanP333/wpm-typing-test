import curses #Allows for the styling of the terminal
from curses import wrapper #Allows to initialize the curses module
from words import words #Used to import the words array
import random
import time

def startScreen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Typing Test!")
    stdscr.addstr("\nPress any key to begin...")
    stdscr.refresh()
    stdscr.getkey() #Waits for the user to type something and then close the program

def loadText():
    text=[]
    length=random.randint(10,15)
    for i in range (length):
        text.append(random.choice(words))
    return text
    


def displayText(stdscr,targetText,currentText,wpm=0): #wpm is the optional parameter
    stdscr.addstr(targetText)
    stdscr.addstr(1,0, f"WPM: {wpm}") #1 row below the text

    for i, char in enumerate(currentText):
        if char==targetText[i]: #Checking the right character has been entered
            stdscr.addstr(0,i, char, curses.color_pair(1))
        else:
            stdscr.addstr(0,i, char, curses.color_pair(2))


def wpmTest(stdscr):
    targetText=" ".join(loadText())
    currentText=[]
    wpm=0
    startTime=time.time() #Time when we start the loop
    stdscr.nodelay(True)

    while True:
        timeElapsed = max(time.time() - startTime,1) #To avoid a division by zero errors
        wpm=round((len(currentText)/(timeElapsed/60))/5) #Assuming that the average word has 5 characters

        stdscr.clear()
        displayText(stdscr, targetText, currentText,wpm)
        stdscr.refresh()

        if "".join(currentText)==targetText:
            stdscr.nodelay(False) #To wait for the user to enter a key
            break

        try:
            key = stdscr.getkey()
        except:
            continue #Skips the rest of the code when the user has not entered a key
        
        if ord(key)==27: #ASCII value of the escape key
            break
        if key in ("KEY_BACKSPACE","\b","\x7f"): #Different types of backspace
            if len(currentText)>0:
                currentText.pop()
        elif len(currentText)<len(targetText):
            currentText.append(key)




        
def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) #1 is the ID of the pair
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    startScreen(stdscr)
    
    while True:
        wpmTest(stdscr)
        stdscr.addstr(2,0,"You have completed the test! Press any key to continue...")
        key = stdscr.getkey()
        if ord(key)==27:
            break

wrapper(main)
