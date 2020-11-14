def create_board():
    # We'll just do a beginner sized board here
    # Beginner is 8x8 with 10 mines (official rules)
    board = []
    for i in range(8):
        board.append([])
    pass

def main():
    print("CMPUT 355 Assignment 4 - Minesweeper")
    move = input("Enter f <coordinate> to place a flag, d <coordinate> to dig")
main()