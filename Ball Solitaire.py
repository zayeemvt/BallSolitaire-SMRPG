


def printHelp():
    print()
    print("+=== *BALL SOLITAIRE* ===+")
    print("-   Based on the puzzle  -")
    print("-   from Super Mario RPG -")
    print("+------------------------+")
    print()
    print("+======== *RULES* =======+")
    print("- Choose a square with a -")
    print("- ball, then choose a    -")
    print("- direction. This will   -")
    print("- attempt to kick the    -")
    print("- ball in that direction.-")
    print("-                        -")
    print("- When you kick a ball,  -")
    print("- it'll leapfrog an      -")
    print("- adjacent ball, which   -")
    print("- will then disappear.   -")
    print("- Keep making balls      -")
    print("- disappear until only   -")
    print("- one remains!           -")
    print("-                        -")
    print("- You can't kick a ball  -")
    print("- into a space already   -")
    print("- occupied by another    -")
    print("- ball! The ball you kick-")
    print("- must always leapfrog   -")
    print("- another ball.          -")
    print("+------------------------+")
    print()
    print("+====== *COMMANDS* ======+")
    print("| help - prints this     |")
    print("|        help guide      |")
    print("|------------------------|")
    print("| reset - restarts the   |")
    print("|         game           |")
    print("|------------------------|")
    print("| quit - exits the game  |")
    print("|------------------------|")
    print("| Enter game inputs with |")
    print("| the following format:  |")
    print("|                        |")
    print("| [c][r] [d]             |")
    print("|                        |")
    print("| [c] - the column       |")
    print("|       corresponding to |")
    print("|       the ball you     |")
    print("|       want to kick.    |")
    print("|       This will always |")
    print("|       be a letter: 'A',|")
    print("|       'B', 'C', or 'D' |")
    print("| ---                    |")
    print("| [r] - the row          |")
    print("|       corresponding to |")
    print("|       the ball you     |")
    print("|       want to kick.    |")
    print("|       This will always |")
    print("|       be a number: 1,  |")
    print("|       2, 3, or 4       |")
    print("| ---                    |")
    print("| [d] - the direction    |")
    print("|       you want to kick |")
    print("|       the ball toward. |")
    print("|       This will always |")
    print("|       be a letter:     |")
    print("|                        |")
    print("|       'u' - up         |")
    print("|       'd' - down       |")
    print("|       'l' - left       |")
    print("|       'r' - right      |")
    print("|                        |")
    print("| EXAMPLES:              |")
    print("| a1 r   [kick to right] |")
    print("| c4 u   [kick upward]   |")
    print("| b2 d   [kick downward] |")
    print("| d3 l   [kick to left]  |")
    print("+------------------------+")
    print()
    input("Press Enter to close help guide.")
    print()

class BallSolitaire:
    def __init__(self):
        self.board = [['O' for _ in range(4)] for _ in range(4)]
        self.board[0][2] = ' '
        self.ball_count = 15
        self.move_sequence = []

    # def readBlock(self, row: int, col: int):
    #     return self.board[row][col]

    def printBoard(self):
        print("    A B C D  ")
        print("  + - - - - +")

        boardString = ""
        for i in range(0,4):
            for j in range(0,4):
                boardString += self.board[i][j]

                if j < 3:
                    boardString += " "
            
            print(f"%i | %s |" % (i+1, boardString))
            boardString = ""

        print("  + - - - - +")
    
    def processInput(self, command: str) -> str:
        valid = [0, 1, 2, 3]

        col = ord(command[0].lower()) - ord('a')
        row = ord(command[1]) - ord('1')

        if row not in valid:
            return "Invalid row"
        elif col not in valid:
            return "Invalid col"
        
        dir = command[3]

        down_dir = 0
        right_dir = 0

        match dir:
            case 'u':
                if row < 2:
                    return "Can't kick up"
                else:
                    down_dir = -1
                
            case 'd':
                if row > 1:
                    return "Can't kick down"
                else:
                    down_dir = 1

            case 'l':
                if col < 2:
                    return "Can't kick left"
                else:
                    right_dir = -1

            case 'r':
                if col > 1:
                    return "Can't kick right"
                else:
                    right_dir = 1

            case _:
                return "Invalid direction"
        
        if (self.validateMove(row, col, down_dir, right_dir)):
            self.processMove(row, col, down_dir, right_dir)
        else:
            return "Illegal move"
        
        self.move_sequence.append(command)
        return "Success"
    
    def validateMove(self, start_row: int, start_col: int, down_dir: int, right_dir: int) -> bool:
        if self.board[start_row][start_col] != 'O':
            return False
        
        jumped = self.board[start_row + down_dir][start_col + right_dir]
        landed = self.board[start_row + 2*down_dir][start_col + 2*right_dir]

        return ((jumped == 'O') and (landed == ' '))

    def processMove(self, start_row: int, start_col: int, down_dir: int, right_dir: int):
        self.board[start_row][start_col] = ' '
        self.board[start_row + down_dir][start_col + right_dir] = ' '
        self.board[start_row + 2*down_dir][start_col + 2*right_dir] = 'O'

        self.ball_count -= 1
        





def main():
    game = BallSolitaire()

    printHelp()

    print(" === GAME START ===\n")

    while(game.ball_count > 1):
        game.printBoard()

        command = input("Input: ")

        if command.lower() == "reset":
            game = BallSolitaire()
            print("\n === GAME START ===")
        elif command.lower() in ["quit", "exit", "stop"]:
            quit()
        elif command.lower() == "help":
            printHelp()
        else:
            try:
                status = game.processInput(command)
                if status != "Success":
                    print(status)
            except IndexError:
                print("Invalid input")
        
        print()

    
    game.printBoard()
    print()
    print("=== YOU SOLVED THE PUZZLE! ===")
    print()
    input("Press Enter to continue.")
    print()
    print("Your move sequence: ")

    for sequence in game.move_sequence:
        print(sequence)
    
    print()
    input("Press Enter to close the game.")

main()