"""This game should allow one player to play the Snake game in a Python print program.
This includes snake length and a winning system
Made by FlorisFireball

I can change:
  - Automate movement, not from input of keys
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
round = 0; #optional, for keeping score?
#facing = "U"; #unused.
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
    }; #Set 1 grid to prevent crash of KeyError/IndexError
    for x in range(inputy): #is the height, repeating for each row
        Board[x+1] = [0]*inputx #is the width
    size = inputx*inputy
    #multiply to find out size of board. Used to see when user "wins"
    Board[PlayerY][PlayerX] = Length;
    spawnCookie();

def direction(move):
    global PlayerX, PlayerY, lose, Length, round;
    key = ["A","B","C","D","Z"];
    if (move == '\033'):
        getch()
        move = getch()
        if move in key:
            #arrow keys use a code: \033[#, where # is a letter. Tab uses the same: \033[Z
            #depending on letter code, change the position of the head in the grid.
            if move == key[0]:
                PlayerY -= 1;
            if move == key[1]:
                PlayerY += 1;
            if move == key[2]:
                PlayerX += 1;
            if move == key[3]:
                PlayerX -= 1;
            if move == key[4]:
                #if Shift+Tab is pressed, set lose to True and exit the game
                lose = True;
            try:
                if Board[PlayerY][PlayerX] == -1:
                    #If position of the head is occupied by a cookie, increase snake length.
                    Length += 1;
                    spawnCookie();
                elif Board[PlayerY][PlayerX] > 1 and Board[PlayerY][PlayerX] < Length-1:
                    lose = True;
                elif Board[PlayerY][PlayerX] == Length-1:
                    #undo movement to prevent moving backwards and lose.
                    if move == key[0]: PlayerY += 1;
                    if move == key[1]: PlayerY -= 1;
                    if move == key[2]: PlayerX -= 1;
                    if move == key[3]: PlayerX += 1;
                else:
                    Move();
                    round+=1;
                Board[PlayerY][PlayerX] = Length
            except KeyError:
                #if Head position is out of bounds
                lose = True;
                print("You hit the wall,",end=' ');
            except IndexError:
                lose = True;
                print("You hit the wall,",end=' ');

def Move():
    #lower the value of each number above 0
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
                #if the item in the grid has no value / is 0, then it's empty, and printed as -- by default
            elif x == Length:
                print("\033[0;38;42m"+sHead, end='');
                #if it has the value of head / the length, which is the highest, print the value for head []
            elif x == 1:
                print("\033[0;38;42m"+sTail, end='');
                #same thing here, but print 'sTail' instead
            elif x == -1:
                print("\033[0;35;41m"+sApple, end='');
                #if the value is -1, the value of an apple, it prints xx for visual
            else:
                print("\033[0;32;42m"+sBody, end='');
                #if none is printed, it mustn't be the tail, head, empty, or the candy, and must instead be the body of the snake.
        print("\033[0m");
    print;
    #last print to print an enter, otherwise it's a continuous line instead of a grid of multiple high.

def spawnCookie():
    global PlayerY
    temp = 0;
    #test if snake is longer than grid count, prevent continuous searching for new place for apple
    while Length<size:
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
    #if the snake is bigger than the grid, set win 1
    #if the snake has been able to move its entire body after the startup, set win 2
    # this is to ensure at least movement has been done before grabbing all candies and winning.
    if (Length >= size) and (round >= size-1):
        printscreen();
        print("Great job! You got the snake to the ultimate size!");
        break;
