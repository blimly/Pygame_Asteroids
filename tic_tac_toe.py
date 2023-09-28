def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_full(board):
    return all(cell != " " for row in board for cell in row)

def get_user_input():
    while True:
        move = input("Enter your move (e.g., a1, b2, c3): ").lower()
        if len(move) == 2 and move[0] in "abc" and move[1] in "123":
            return move

def update_state(board, move, current_player):
    row, col = ord(move[0]) - ord("a"), int(move[1]) - 1

    if board[row][col] == " ":
        board[row][col] = current_player

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)
        move = get_user_input()
        update_state(board, move, current_player)

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        elif is_full(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

play_game()