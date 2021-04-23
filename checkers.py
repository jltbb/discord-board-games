class Gold:
    tile = '⬜'
    piece = '🌕'
    king = '📀'
    name = 'Gold'

class Gray:
    tile = '🟦'
    piece = '🌑'
    king = '💿'
    name = 'Gray'

class Player():
    GRAY = Gray()
    GOLD = Gold()

def create_board():
    blank_board = [['⬜', '🟦', '⬜', '🟦', '⬜', '🟦', '⬜', '🟦'],
                   ['🟦', '⬜', '🟦', '⬜', '🟦', '⬜', '🟦', '⬜'],
                   ['⬜', '🟦', '⬜', '🟦', '⬜', '🟦', '⬜', '🟦'],
                   ['🟦', '⬜', '🟦', '⬜', '🟦', '⬜', '🟦', '⬜'],
                   ['⬜', '🟦', '⬜', '🟦', '⬜', '🟦', '⬜', '🟦'],
                   ['🟦', '⬜', '🟦', '⬜', '🟦', '⬜', '🟦', '⬜'],
                   ['⬜', '🟦', '⬜', '🟦', '⬜', '🟦', '⬜', '🟦'],
                   ['🟦', '⬜', '🟦', '⬜', '🟦', '⬜', '🟦', '⬜']]

    for i in range(3):
        for j, tile in enumerate(blank_board[i]):
            if tile == Gray.tile:
                blank_board[i][j] = Gold.piece

        i_rev = -i - 1

        for j, tile in enumerate(blank_board[i_rev]):
            if tile == Gray.tile:
                blank_board[i_rev][j] = Gray.piece

    return blank_board

class Game():
    current_player = Player.GRAY
    board = create_board()

# Global game variable
game = Game()

# Global message buffer variable
msg_buffer = None

# Player name variables


def initialize_game():
    game.board = create_board()


def split_coordinates(pos):
    row = int(pos[1]) - 1
    col = ord(pos[0]) - ord('a')

    return row, col

def switch_current_player():
    if game.current_player == Player.GRAY:
        game.current_player = Player.GOLD
    else:
        game.current_player = Player.GRAY

def check_if_illegal(start_coord, end_coord):
    global msg_buffer

    def is_empty_tile(row, col):
        return game.board[row][col] in [Gold.tile, Gray.tile]

    def is_legal_position(row, col):
        return row >= 0 and row < 8 and col >= 0 and col < 8

    def is_own_piece(row, col):
        return game.board[row][col] in [game.current_player.piece, game.current_player.king]

    def is_king(row, col):
        return game.board[row][col] == game.current_player.king

    def is_diagonal(start_row, start_col, end_row, end_col):
        return start_row != end_row and start_col != end_col

    def is_legal_distance(start_row, start_col, end_row, end_col):
        distance = abs(end_row - start_row) + abs(end_col - start_col)
        if distance == 2:
            return True
        elif distance == 4:
            # A jump may be possible
            halfway_row = (start_row + end_row) // 2
            halfway_col = (start_col + end_col) // 2

            return not is_empty_tile(halfway_row, halfway_col) and \
                   not is_own_piece(halfway_row, halfway_col)
        else:
            return False

    start_row, start_col = start_coord
    end_row, end_col = end_coord

    # Make sure player cannot start outside the board
    if not is_legal_position(start_row, start_col):
        msg_buffer = 'Error: Start tile is outside of bounds'
        return False

    # Make sure player cannot move board tiles
    if is_empty_tile(start_row, start_col):
        msg_buffer = 'Error: Start tile is empty'
        return False

    # Make sure player cannot modify enemy pieces
    if not is_own_piece(start_row, start_col):
        msg_buffer = 'Error: Start tile is not own piece'
        return False

    # Make sure player cannot escape board
    if not is_legal_position(end_row, end_col):
        msg_buffer = 'Error: End tile is outside of bounds'
        return False

    # Make sure player cannot go to own player's piece
    if is_own_piece(end_row, end_col):
        msg_buffer = 'Error: End tile is own piece'
        return False

    # Make sure player cannot land on enemy's piece
    if not is_own_piece(end_row, end_col) and \
       not is_empty_tile(end_row, end_col):
        msg_buffer = 'Error: End tile is enemy piece'
        return False

    # Make sure move is diagonal
    if not is_diagonal(start_row, start_col, end_row, end_col):
        msg_buffer = 'Error: Move is not diagonal'
        return False

    # Make sure move is of right length, taking into account potential jumps
    if not is_legal_distance(start_row, start_col, end_row, end_col):
        msg_buffer = 'Error: Move is not of correct distance'
        return False

    # Make sure player (if not kinged) cannot move backwards
    if not is_king(start_row, start_col):
        row_dif = end_row - start_row
        if game.current_player == Player.GRAY and row_dif > 0:
            msg_buffer = 'Error: Cannot move backwards if not kinged'
            return False
        if game.current_player == Player.GOLD and row_dif < 0:
            msg_buffer = 'Error: Player cannot move backwards if not kinged'
            return False

    return True

def move_piece(start_pos, end_pos):
    board = game.board

    global msg_buffer

    msg_buffer = None

    def is_jump(start_row, start_col, end_row, end_col):
        return abs(end_row - start_row) + abs(end_col - start_col) == 4

    def get_halfway_coord(start_row, start_col, end_row, end_col):
        halfway_row = (start_row + end_row) // 2
        halfway_col = (start_col + end_col) // 2
        return halfway_row, halfway_col

    # Get board coordinates from user
    start_row, start_col = split_coordinates(start_pos)
    end_row, end_col = split_coordinates(end_pos)

    if not check_if_illegal((start_row, start_col), (end_row, end_col)):
        return

    # If a player jumps over another player's piece, remove the piece.
    if is_jump(start_row, start_col, end_row, end_col):
        halfway_row, halfway_col = get_halfway_coord(start_row, start_col, end_row, end_col)

        game.board[halfway_row][halfway_col] = Gray.tile

    # Move piece to next location
    game.board[end_row][end_col] = game.board[start_row][start_col]
    game.board[start_row][start_col] = Gray.tile

    # Player has reached the end of the board, king them
    if game.current_player == Player.GOLD and end_row == 7 or \
       game.current_player == Player.GRAY and end_row == 0:
        game.board[end_row][end_col] = game.current_player.king

    # Collect number of pieces of each color
    num_gold = num_gray = 0

    for row in game.board:
        for tile in row:
            if tile in [Gold.piece, Gold.king]:
                num_gold += 1
            if tile in [Gray.piece, Gray.king]:
                num_gray += 1

    # Win conditions
    if num_gold == 0:
        msg_buffer = 'Gray has won!'

    if num_gray == 0:
        msg_buffer = 'Gold has won!'

    # Update current player
    switch_current_player()

def draw_board():
    regional_indicators = [f':regional_indicator_{chr(ord("a") + x)}:' for x in range(8)]

    numerical_symbols = [':one:', ':two:', ':three:', ':four:',
                         ':five:', ':six:', ':seven:', ':eight:']

    output = ''
    output += game.current_player.piece + ''.join(regional_indicators) + '\n'

    for i, row in enumerate(game.board):
        output += numerical_symbols[i] + "".join(row) + "\n"

    return output
