import random



a1 = ' '
a2 = ' '
a3 = ' '
b1 = ' '
b2 = ' '
b3 = ' '
c1 = ' '
c2 = ' '
c3 = ' '

checklist = []
POSITIONS = ['a1','a2','a3','b1','b2','b3','c1','c2','c3']


# ======== PLAYER INPUT FUNCTIONS ======== #

def oplayer():
    while True:
        print("\n")
        move = input("[PLAYER O TURN] Select your position: ")
        print("\n")
        if move in checklist:
            print("Position taken! Try another.\n")
            continue
        elif move not in ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']:
            print("Invalid move! Use: a1-c3\n")
            continue
        else:

            if move == 'a1':
                global a1
                a1 = 'O'
            elif move == 'a2':
                global a2
                a2 = 'O'
            elif move == 'a3':
                global a3
                a3 = 'O'
            elif move == 'b1':
                global b1
                b1 = 'O'
            elif move == 'b2':
                global b2
                b2 = 'O'
            elif move == 'b3':
                global b3
                b3 = 'O'
            elif move == 'c1':
                global c1
                c1 = 'O'
            elif move == 'c2':
                global c2
                c2 = 'O'
            elif move == 'c3':
                global c3
                c3 = 'O'

            board = f'a |{a1}|{a2}|{a3}|\n'\
                f'b |{b1}|{b2}|{b3}|\n'\
                f'c |{c1}|{c2}|{c3}|\n'\
                '   1 2 3'
            print("┌────────┐")
            print(board)
            print("└────────┘")
            checklist.append(move)
            return move


# ======== PLAYER X (HUMAN) ======== #

def xplayer():
    while True:
        print("\n")
        move = input("[PLAYER X TURN] Select your position: ")
        print("\n")
        if move in checklist:
            print("Position taken! Try another.\n")
            continue
        elif move not in ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']:
            print("Invalid move! Use: a1-c3\n")
            continue
        else:

            if move == 'a1':
                global a1
                a1 = 'X'
            elif move == 'a2':
                global a2
                a2 = 'X'
            elif move == 'a3':
                global a3
                a3 = 'X'
            elif move == 'b1':
                global b1
                b1 = 'X'
            elif move == 'b2':
                global b2
                b2 = 'X'
            elif move == 'b3':
                global b3
                b3 = 'X'
            elif move == 'c1':
                global c1
                c1 = 'X'
            elif move == 'c2':
                global c2
                c2 = 'X'
            elif move == 'c3':
                global c3
                c3 = 'X'

            board = f'a |{a1}|{a2}|{a3}|\n'\
                f'b |{b1}|{b2}|{b3}|\n'\
                f'c |{c1}|{c2}|{c3}|\n'\
                '   1 2 3'
            print("┌────────┐")
            print(board)
            print("└────────┘")
            checklist.append(move)
            return move


# ======== COMPUTER AI ======== #

def computer_move(difficulty='medium'):
    avail = [p for p in POSITIONS if p not in checklist]
    if not avail:
        return None

    if difficulty == 'easy':
        move = random.choice(avail)
    elif difficulty == 'hard':
        move = find_winning_move(avail) or find_blocking_move(avail) or choose_strategic(avail)
    else:
        move = 'b2' if 'b2' in avail else (random.choice([p for p in ['a1','a3','c1','c3'] if p in avail]) if any(p in avail for p in ['a1','a3','c1','c3']) else random.choice(avail))

    if move == 'a1':
        global a1
        a1 = 'O'
    elif move == 'a2':
        global a2
        a2 = 'O'
    elif move == 'a3':
        global a3
        a3 = 'O'
    elif move == 'b1':
        global b1
        b1 = 'O'
    elif move == 'b2':
        global b2
        b2 = 'O'
    elif move == 'b3':
        global b3
        b3 = 'O'
    elif move == 'c1':
        global c1
        c1 = 'O'
    elif move == 'c2':
        global c2
        c2 = 'O'
    elif move == 'c3':
        global c3
        c3 = 'O'

    board = f'a |{a1}|{a2}|{a3}|\n'\
        f'b |{b1}|{b2}|{b3}|\n'\
        f'c |{c1}|{c2}|{c3}|\n'\
        '   1 2 3'
    print("┌────────┐")
    print(board)
    print("└────────┘")
    checklist.append(move)
    return move


def find_winning_move(avail):
    for pos in avail:
        test_board = {'a1':a1,'a2':a2,'a3':a3,'b1':b1,'b2':b2,'b3':b3,'c1':c1,'c2':c2,'c3':c3}
        test_board[pos] = 'O'
        if check_win_with_board(test_board):
            return pos
    return None


def find_blocking_move(avail):
    for pos in avail:
        test_board = {'a1':a1,'a2':a2,'a3':a3,'b1':b1,'b2':b2,'b3':b3,'c1':c1,'c2':c2,'c3':c3}
        test_board[pos] = 'X'
        if check_win_with_board(test_board):
            return pos
    return None


def choose_strategic(avail):
    if 'b2' in avail:
        return 'b2'
    corners = [p for p in ['a1','a3','c1','c3'] if p in avail]
    if corners:
        return random.choice(corners)
    return random.choice(avail)


def check_win_with_board(board):
    a1, a2, a3, b1, b2, b3, c1, c2, c3 = board['a1'], board['a2'], board['a3'], board['b1'], board['b2'], board['b3'], board['c1'], board['c2'], board['c3']
    if a1 == a2 == a3 != ' ' or b1 == b2 == b3 != ' ' or c1 == c2 == c3 != ' ' or a1 == b1 == c1 != ' ' or a2 == b2 == c2 != ' ' or a3 == b3 == c3 != ' ' or a1 == b2 == c3 != ' ' or a3 == b2 == c1 != ' ':
        return True
    return False


# ======== WIN/DRAW CHECKERS ======== #

def check_win():
    if a1 == a2 == a3 != ' ' or b1 == b2 == b3 != ' ' or c1 == c2 == c3 != ' ' or a1 == b1 == c1 != ' ' or a2 == b2 == c2 != ' ' or a3 == b3 == c3 != ' ' or a1 == b2 == c3 != ' ' or a3 == b2 == c1 != ' ':
        return True

    else:
        return False


def check_draw():
    if len(checklist) == 9:
        return True
    return False


# ======== DISPLAY FUNCTION ======== #

def display_board():
    global board
    board = f'a |{a1}|{a2}|{a3}|\n'\
        f'b |{b1}|{b2}|{b3}|\n'\
        f'c |{c1}|{c2}|{c3}|\n'\
        '   1 2 3'
    print("┌────────┐")
    print(board)
    print("└────────┘")


# ======== MAIN GAME LOOP ======== #

def play_game(mode='2', difficulty='medium'):
    print("\n=== TIC TAC TOE ===")
    display_board()

    while True:
        xplayer()
        if check_win():
            print("\n╔═══════════════════════════╗")
            print("║    X WINS THE GAME!       ║")
            print("╚═══════════════════════════╝\n")
            break
        if check_draw():
            print("\n╔═══════════════════════════╗")
            print("║    IT'S A DRAW MATCH!     ║")
            print("╚═══════════════════════════╝\n")
            break

        if mode == '1':
            computer_move(difficulty)
        else:
            oplayer()

        if check_win():
            print("\n╔═══════════════════════════╗")
            print("║    O WINS THE GAME!       ║")
            print("╚═══════════════════════════╝\n")
            break
        if check_draw():
            print("\n╔═══════════════════════════╗")
            print("║    IT'S A DRAW MATCH!     ║")
            print("╚═══════════════════════════╝\n")
            break


# ======== MAIN ENTRY POINT ======== #

if __name__ == "__main__":
    print("Choose mode:")
    print("1) Play vs Computer")
    print("2) Two players")
    mode = ''
    while mode not in ['1','2']:
        mode = input("Enter 1 or 2: ")
    
    difficulty = 'medium'
    if mode == '1':
        print("\nChoose difficulty:")
        print("1) Easy")
        print("2) Medium")
        print("3) Hard")
        diff_choice = ''
        while diff_choice not in ['1','2','3']:
            diff_choice = input("Enter 1, 2, or 3: ")
        difficulty = ['easy','medium','hard'][int(diff_choice)-1]
    
    play_game(mode, difficulty)
