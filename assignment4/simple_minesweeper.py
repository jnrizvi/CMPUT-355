import random

# choose a difficulty level
def level():
    while True:
        number = input("Please choose the difficulty level from 1 to 3: ")
        try:
            number = int(number)
        except ValueError:
            print("Please enter a number, please enter again. ")
            continue
        if number == 1:
            mn=5
            return mn,4,5
        elif number == 2:
            mn=10
            return mn,8,10
        elif number == 3:
            mn=40
            return mn,16,40
        else:
            print("Please enter 1 or 2 or 3, please enter again. ")
            continue

# set up mines randomly and set up values of other grids (how many mines in its neighbours)
def setValues(gridSize,minesNum,state):
    n = 0
    while n < minesNum:
        r = random.randint(0, gridSize-1)
        c = random.randint(0, gridSize-1)
        if state[r][c] != 'F':
            state[r][c] = 'F'
            n += 1
    
    for i in range(gridSize):
        for j in range(gridSize):
            if state[i][j] != 'F':
                num = 0
                if i>0 and j>0 and state[i-1][j-1] == 'F':
                    num += 1
                if i>0 and state[i-1][j] == 'F':
                    num += 1
                if i>0 and j<gridSize-1 and state[i-1][j+1] == 'F':
                    num += 1
                if j>0 and state[i][j-1] == 'F':
                    num += 1
                if j<gridSize-1 and state[i][j+1] == 'F':
                    num += 1
                if i<gridSize-1 and j>0 and state[i+1][j-1] == 'F':
                    num += 1
                if i<gridSize-1 and state[i+1][j] == 'F':
                    num += 1
                if i<gridSize-1 and j<gridSize-1 and state[i+1][j+1] == 'F':
                    num += 1
                state[i][j] = num

# show the layout                
def showNum(gridSize,show):
    global flag
    global mn
    print()
    for r in show:
        print("  ".join(str(v) for v in r))      
    rf = mn-len(flag)
    print("Remaining flags: " + str(rf))

# use recursion to explore adjacent 0 value neighbours
def explore(x,y):
    global state
    global show
    global flag
    global gridSize
    global seen
    if ([x,y] not in seen) and ([x,y] not in flag):
        seen.append([x,y])
        if state[x][y] == 0:
            show[x][y] = state[x][y]
            if x>0:
                explore(x-1,y)
            if x>0 and y>0:
                explore(x-1,y-1)
            if x>0 and y<gridSize-1:
                explore(x-1,y+1)            
            if x<gridSize-1:
                explore(x+1,y)
            if y>0:
                explore(x,y-1)
            if y<gridSize-1:
                explore(x,y+1)
            if x<gridSize-1 and y>0:
                explore(x+1,y-1)
            if x<gridSize-1 and y<gridSize-1:
                explore(x+1,y+1)
        else:
            show[x][y] = state[x][y]

# check if the player win or not
def check(gridSize,show,state):
    n = 0
    for i in range(gridSize):
        for j in range(gridSize):
            if show[i][j] != state[i][j]:
                return False
    return True

if __name__ == "__main__":
    print("Welcome to Minesweeper\n")
        
    mn,gridSize,minesNum = level()
    
    # display rules
    print()
    print("Pick position 1 2      1 2 p")
    print("Flag position 2 3      2 3 f")
    print()
    
    state = [[0 for i in range(gridSize)] for x in range(gridSize)] 
    show = [['-' for i in range(gridSize)] for x in range(gridSize)]    

    setValues(gridSize,minesNum,state)
            
    #for i in state:
        #print(i)
    
    # check the player's input
    flag = []
    game = True
    while game == True:
        lose = False
        showNum(gridSize,show)
        cmd = input("Enter your value: ").split()
        if len(cmd) == 3:
            if cmd[2] != 'p' and cmd[2] != 'f':
                print("Wrong input, please enter again. ")
                continue
            try:
                cmd[0] = int(cmd[0])
            except ValueError:
                print("Wrong input, please enter again. ")
                continue
            try:
                cmd[1] = int(cmd[1])
            except ValueError:
                print("Wrong input, please enter again. ")
                continue     
            if cmd[0]<=0 or cmd[0]>gridSize or cmd[1]<=0 or cmd[1]>gridSize:
                print("Wrong input, please enter again. ")
                continue
        else:
            print("Wrong input, please enter again. ")
            continue
        
        x = cmd[0]-1
        y = cmd[1]-1 
        
        # if the player flags a position
        if cmd[2] == 'f':
            if [x,y] in flag:
                print("The position is already flagged, please enter again. ")
                continue
            if len(flag) >= minesNum:
                print("There are two many flags, please enter again. ")
                continue      
            if show[x][y] != '-':
                print("The position is already existed, please enter again. ")
                continue            
            if ([x,y] not in flag) and len(flag) < minesNum:
                flag.append([x,y])
                show[x][y] = 'F'
                
        # if the player picks a position
        if cmd[2] == 'p':
            if [x,y] in flag:
                flag.remove([x,y])
            if show[x][y] != '-' and show[x][y] != 'F':
                print("The position is already existed, please enter again. ")
                continue     
            # if the player lands on a mine, the game is over
            if state[x][y] == 'F':
                show[x][y] == 'F'
                for i in range(gridSize):
                    for j in range(gridSize):
                        if state[i][j] == 'F':
                            show[i][j] = 'X'
                showNum(gridSize,show)
                lose = True
                print("Game Over! :(")
                #break
            # if the player picks a cell with 0 value
            elif state[x][y] == 0:
                show[x][y] == 0
                seen = []
                explore(x,y)
            else:
                show[x][y] = state[x][y]
        # display message if the player wins
        if lose != True:
            if (check(gridSize,show,state)):
                showNum(gridSize,show)
                print("You Win! :)")
                break
        else:
            # ask the player if he/she wants to play again
            good = False
            while not good:
                answer = input("Do you want to play again? Enter 'Y' for yes or 'N' for no.\n")
                if answer == "N":
                    game = False
                    break
                elif answer == "Y":
                    gridSize,minesNum = level()
                    state = [[0 for i in range(gridSize)] for x in range(gridSize)] 
                    show = [['-' for i in range(gridSize)] for x in range(gridSize)]    
                    setValues(gridSize,minesNum,state)
                    break
                
