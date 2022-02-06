import copy
import random
from termcolor import colored
import colorama

# Вызов функции для корректной работы termcolor на Windows 10
colorama.init()

DRAW = 'draw'


def display_welcome():
    """Выводит на экран приветствие."""
    print(
        """
        Добро пожаловать в игру "Обратные крестики-нолики".
        Для победы тебе необходимо, чтобы компьютер собрал вертикальный, 
        горизонтальный или диагональный ряд из пяти своих фигур.
        Удачи!\n
        """
    )


def pieces():
    """Определяет принадлежность перового хода."""
    go_first = None
    while go_first not in ('y', 'n'):
        go_first = input("Хочешь ходить первым? (y, n): ")
        if go_first == "y":
            print("\nТы играешь крестикими.")
            human = 'X'
            computer = 'O'
        else:
            print("\nТы играешь ноликами")
            computer = 'X'
            human = 'O'
        return computer, human


def new_board():
    """Создает новое игровое поле"""
    return [[i + (j * 10) for i in range(0, 10)] for j in range(0, 10)]


def print_board(board):
    """Выводит игровое поле"""
    for line in board:
        print('---------------------------------------------------')
        for cell in line:
            if type(cell) is int and cell < 10:
                print(f'| 0{cell} ', end='')
            elif cell == 'X':
                print(f'|  {colored(cell, "green")} ', end='')
            elif cell == 'O':
                print(f'|  {colored(cell, "red")} ', end='')
            else:
                print(f'| {cell} ', end='')
        print('|')

    print('---------------------------------------------------')


def next_turn(turn):
    """Осуществляет переход хода."""
    if turn == 'X':
        return 'O'
    else:
        return 'X'


def legal_moves(board):
    """Создаёт список доступных ходов."""
    moves = []
    for line in board:
        for cell in line:
            if type(cell) is int:
                moves.append(cell)
    return moves


def human_move(board, human):
    """Получает ход человека"""
    legal = legal_moves(board)
    move = None
    while move not in legal:
        try:
            move = int(input('Введи число от 0 до 99: '))
            if move not in legal:
                print("\nЭто поле уже занято. Выбери другое.\n")
        except ValueError:
            print('Некорректный ввод')
    board[move // 10][move % 10] = human
    return board


def computer_move(board, computer):
    """Получает ход компьютера"""
    temp_moves = legal_moves(board)[:]
    while temp_moves:
        temp_board = copy.deepcopy(board)
        move = random.choice(temp_moves)
        temp_board[move // 10][move % 10] = computer
        if losser(temp_board, computer):
            temp_moves.remove(move)
        else:
            board[move // 10][move % 10] = computer
            print(f'Компьютер выбират число: {colored(move, "red")}')
            return board
    move = legal_moves(board)[0]
    board[move // 10][move % 10] = computer
    print(f'Компьютер выбират число: {colored(move, "red")}')
    return board


def losser(board, player):
    """Определяет проигравшего в игре."""
    horizontal_count = 0
    vertical_count = 0
    diagonal_right_count = 0
    diagonal_left_count = 0

    # Проверка по горизонтали
    for line in board:
        for cell in line:
            if cell == player:
                horizontal_count += 1
            else:
                horizontal_count = 0
            if horizontal_count >= 5:
                return player
        horizontal_count = 0

    # Проверка по вертикали
    for i in range(10):
        for line in board:
            if line[i] == player:
                vertical_count += 1
            else:
                vertical_count = 0
            if vertical_count >= 5:
                return player
        vertical_count = 0

    # Проверка по диагонали
    for j in range(6):
        i = j
        for line in board:
            if line[i] == player:
                diagonal_right_count += 1
                i += 1
            else:
                i = j
                diagonal_right_count = 0
            if diagonal_right_count >= 5:
                return player
        diagonal_right_count = 0

    for i in range(9, 3, -1):
        for line in board:
            if line[i] == player:
                diagonal_left_count += 1
                if i - 1 >= 0:
                    i -= 1
                else:
                    break
            else:
                diagonal_left_count = 0
            if diagonal_left_count >= 5:
                return player
        diagonal_left_count = 0

    if not legal_moves(board):
        return DRAW

    return False


def congrat_winner(losser_flag, computer, human):
    """Поздравляет победителя игры."""
    if losser_flag == computer:
        print('Поздравляю!!! В этот раз победа за тобой.')
    elif losser_flag == human:
        print('К сожалению, в этот раз победа за компьютером.')
    else:
        print('В этот раз ничья.')


def restart():
    restart_response = None
    while restart_response not in ('y', 'n'):
        restart_response = input("Хочешь сыграть еще раз? (y, n): ")
        if restart_response == "y":
            return main()
        else:
            break


def main():
    display_welcome()
    computer, human = pieces()
    board = new_board()
    print_board(board)
    turn = 'X'
    losser_flag = False
    while not losser_flag:
        if turn == human:
            board = human_move(board, human)
        else:
            board = computer_move(board, computer)
        print_board(board)
        losser_flag = losser(board, turn)
        turn = next_turn(turn)
    congrat_winner(losser_flag, computer, human)
    restart()


main()
