"""This game should allow one player to play the Snake game in a Python print program.
This includes snake length and a winning system
Made by FlorisFireball

I can change:
  - Automate movement, not from input of keys
    - Show next move (see if you will run into yourself)
"""

from time import sleep;
from random import randint;

class _Getch: #thank google for allowing permanent borrowing
    #Get char like input().  Does not echo to screen
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()
class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            #print("system waits for input... that's why I can't make snake move automatically every x miliseconds");
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
getch = _Getch();
lose = False; #obviously...
round = 0;
facing = "U";
sEmpty = "--"#input("--Empty: "+"--")[:2]; #this allows for complete configuration, changing your field every time you play
sApple = "xx"#input("xxApple: "+"xx")[:2];
sHead = "[]"#input("[]Head: "+"[]")[:2];
sBody = "OO"#input("OOBody: "+"OO")[:2];
sTail = "<>"#input("<>Tail: "+"<>")[:2]; #<>Tail: + <> , first one shows default, second adds if left empty, else it's invisible or unequal/bad

def restart():
    global Board, Length, PlayerX, PlayerY, size;
    print("\n\nWelcome to 'Snake'!\nUse your ARROW keys to MOVE, press Shift+Tab to STOP\n");
    Length = 4;
    PlayerX = 0;
    PlayerY = 1;
    inputx = int(input("X grid size (width):  "));
    inputy = int(input("Y grid size (height): "));
    Board = {
    1:[0]
    };
    for x in range(inputy):
        Board[x+1] = [0]*inputx
    size = inputx*inputy
    Board[PlayerY][PlayerX] = Length;
    spawnCookie();

def direction(move):
    global PlayerX, PlayerY, lose, Length, round;
    key = ["A","B","C","D","Z"];
    if (move == '\033'):
        getch()
        move = getch()
        if move in key:
            if move == key[0]: PlayerY -= 1;
            if move == key[1]: PlayerY += 1;
            if move == key[2]: PlayerX += 1;
            if move == key[3]: PlayerX -= 1;
            if move == key[4]: lose = True;
            try:
                if Board[PlayerY][PlayerX] == -1:
                    Length += 1;
                    spawnCookie();
                elif Board[PlayerY][PlayerX] > 1 and Board[PlayerY][PlayerX] < Length-1:
                    lose = True;
                    pass;
                elif Board[PlayerY][PlayerX] == Length-1: #undo movement at beginning so you stay in bounds
                    if move == key[0]: PlayerY += 1;
                    if move == key[1]: PlayerY -= 1;
                    if move == key[2]: PlayerX -= 1;
                    if move == key[3]: PlayerX += 1;
                else:
                    Move();
                    round+=1;
                Board[PlayerY][PlayerX] = Length
            except KeyError:
                lose = True;
                print("You hit the wall,",end=' ');
            except IndexError:
                lose = True;
                print("You hit the wall,",end=' ');

def Move():
    for y in Board:
        for x in range(len(Board[y])):
            if Board[y][x] > 0:
                Board[y][x] = Board[y][x]-1;

def printscreen():
    global Board, round;
    print("\nExit: Shift+Tab   "+str(round));
    for y in Board:
        for x in Board[y]:
            if x == 0:
                print("\033[0m"+sEmpty+"\033[0m", end='');
            elif x == Length:
                print("\033[0;38;42m"+sHead, end='');
            elif x == 1:
                print("\033[0;38;42m"+sTail, end='');
            elif x == -1:
                print("\033[0;35;41m"+sApple, end='');
            else:
                print("\033[0;32;42m"+sBody, end='');
        print("\033[0m");
    print;

def spawnCookie():
    global PlayerY
    temp = 0;
    print(Length,size)
    while Length<size: #test if snake is longer than grid count
        temp+=1;
        row = randint(1,len(Board));
        col = randint(0,len(Board[PlayerY]))-1;
        if Board[row][col] == 0:
            Board[row][col] = -1;
            break

restart();
while True:
    printscreen();
    direction(getch());
    if lose == True:
        print("You lost! Too bad :(");
        break
    if (Length >= size) and (round >= size-1):
        printscreen();
        print("Great job! You got the snake to the ultimate size!");
        break;
