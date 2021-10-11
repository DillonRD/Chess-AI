def ChessBoardSetup():
    # initialize and return a chess board - create a 2D 8x8 array that has the value for each cell
    # USE the following characters for the chess pieces - lower-case for BLACK and upper-case for WHITE
    # . for empty board cell
    # p/P for pawn
    # r/R for rook
    # t/T for knight
    # b/B for bishop
    # q/Q for queen
    # k/K for king
    white = ['r', 't', 'b', 'q', 'k', 'b', 't', 'r']
    black = [ 'R','T', 'B' ,'Q', 'K', 'B','T','R']
    pawnW = 'p'
    pawnB = 'P'
    blank = '.'
    
    count = 0
    
    row, col = (8,8)
    
    board = [[0 for x in range(col)] for x in range(row)]
    
    for i in range(col):
        board[0][i] = white[count]
        board[1][i] = pawnW 
        board[2][i] = blank
        board[3][i] = blank
        board[4][i] = blank
        board[5][i] = blank
        board[6][i] = pawnB
        board[7][i] = black[count]
        count = count + 1

    whiteKing = (0,4)
    blackKing = (7,4)
    return board



def MovePiece(board, from_piece, to_piece):
    # write code to move the one chess piece
    # you do not have to worry about the validity of the move - this will be done before calling this function
    # this function will at least take the move (from-peice and to-piece) as input and return the new board layout
    new_board = board
    new_board[to_piece[0]][to_piece[1]] = new_board[from_piece[0]][from_piece[1]]
    new_board[from_piece[0]][from_piece[1]] = '.'

    if new_board[to_piece[0]][to_piece[1]] == 'k':
      blackKing = to_piece

    if new_board[to_piece[0]][to_piece[1]] == 'k':
      whiteKing = to_piece

    return new_board

def DrawBoard(board):
    # write code to print the board - following is one print example
    # r t b q k b t r
    # p p p p p p p p
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # P P P P P P P P
    # R T B Q K B T R
    for i in range(8):
        for j in range(8):
            print(board[i][j], end = " ")
        print()


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!       
# return True if the input move (from-square and to-square) is legal, else False
# this is the KEY function which contains the rules for each piece type 
# return True if the input move (from-square and to-square) is legal, else False
# this is the KEY function which contains the rules for each piece type 
def IsMoveLegal(board, from_square, to_square):
    # input is from-square and to-square
    # use the input and the board to get the from-piece and to-piece
    if from_square is None or to_square is None:
        return False
    
    y = from_square[0]
    x = from_square[1]
    y_to = to_square[0]
    x_to = to_square[1]

    piece = board[y][x]
    
    piece_to = board[y_to][x_to]
    
    x_abs = abs(x - x_to)
    y_abs = abs(y - y_to)
    
    isLegal = False
    
    try:
        slope = abs((float(y) - y_to) / (x - x_to)) 
    except:
        slope = 0
        
    if x_to > 7 or x_to < 0 or y_to > 7 or y_to < 0:
        return False
    
    # Pawn
    if piece == "p": # black pawn
        ## case - pawn wants to move one step forward (or backward if white)
        if piece_to == '.' and x_to == x and y + 1 == y_to:
            return True
        ## case - pawn can move two spaces forward (or backward if white) ONLY if pawn on starting row
        if y == 1 and y_to == y + 2 and piece_to == '.' and isStraightClear(from_square, to_square, board) and x_to == x:
            return True   
        ## case - pawn attacks the enemy piece if diagonal
        if piece_to.isupper() and y + 1 == y_to and (x_to == x - 1 or x_to == x + 1):
            return True
    elif piece == "P": # white pawn
        
        ## case - pawn wants to move one step forward (or backward if white)
        if piece_to == '.' and x_to == x and y - 1 == y_to:
            return True
        ## case - pawn can move two spaces forward (or backward if white) ONLY if pawn on starting row
        if y == 6 and y_to == y - 2 and piece_to == '.' and isStraightClear(from_square, to_square, board) and x_to == x:
            return True   
        ## case - pawn attacks the enemy piece if diagonal
        if piece_to.islower() and y - 1 == y_to and (x_to == x - 1 or x_to == x + 1):
            return True
    # Rook
    elif piece == "r": # black rook
        if x_to == x or y == y_to:
            if (piece_to == '.' or piece_to.isupper()) and isStraightClear(from_square, to_square, board):
                return True
    elif piece == "R": # white rook
        if x_to == x or y == y_to: #checks to see if its the same row or column
            if (piece_to == '.' or piece_to.islower()) and isStraightClear(from_square, to_square, board): #checks if enemy or blank and pathing
                return True
    
    # Knight
    elif piece == "t": # black knight
        if (piece_to == '.' or piece_to.isupper()) and ((x_abs == 2 and y_abs == 1) or (y_abs == 2 and x_abs == 1)):
            return True
    elif piece == "T": # white knight
        if (piece_to == '.' or piece_to.islower()) and ((x_abs == 2 and y_abs == 1) or (y_abs == 2 and x_abs == 1)):
            return True
    # Bishop
    elif piece == "b": # black bishop
        if x == x_to:
            return False  
        if slope == 1  and (piece_to == '.' or piece_to.isupper()) and isDiagonalClear(from_square, to_square, board):
            return True

    elif piece == "B": # white bishop
        if x == x_to:
            return False
        if slope == 1 and (piece_to == '.' or piece_to.islower()) and isDiagonalClear(from_square, to_square, board):
            return True
    # Queen
    elif piece == "q": # black queen
        #side and up/down
        if x_to == x or y == y_to:
            if (piece_to == '.' or piece_to.isupper()) and isStraightClear(from_square, to_square, board):
                return True
        #diagonal
        if slope == 1 and (piece_to == '.' or piece_to.isupper()) and isDiagonalClear(from_square, to_square, board):
            return True
    elif piece == "Q": # white queen
        #side and up/down
        if x_to == x or y == y_to: #checks to see if its the same row or column
            if (piece_to == '.' or piece_to.islower()) and isStraightClear(from_square, to_square, board): #checks if enemy or blank and pathing
                return True
         #diagonal      
        if slope == 1 and (piece_to == '.' or piece_to.islower()) and isDiagonalClear(from_square, to_square, board):
            return True
    # King
    elif piece == "k": # black king
         if x_abs <= 1 and y_abs <= 1 and (piece_to == '.' or piece_to.isupper()):
             return True
    elif piece == "K": # white king
        if x_abs <= 1 and y_abs <= 1 and (piece_to == '.' or piece_to.islower()):
             return True
    else:
       return False
        
    return isLegal


# helper function to figure out if a move is legal for straight-line moves (rooks, bishops, queens, pawns)
# returns True if the path is clear for a move (from-square and to-square), non-inclusive
# helper function to figure out if a move is legal for straight-line moves (rooks, bishops, queens, pawns)
# returns True if the path is clear for a move (from-square and to-square), non-inclusive
def isStraightClear(from_square, to_square, board):
    
    y = from_square[0]
    x = from_square[1]
    y_to = to_square[0]
    x_to = to_square[1]

    y_diff = y - y_to
    x_diff = x - x_to


    #checks above straight
    if x == x_to and y > y_to:
        for i in range(1 ,abs(y_diff)):
            
            if board[y-i][x] != '.':
                return False
        return True
    #checks below straight
    if x == x_to and y < y_to:
        for i in range(1 ,abs(y_diff)):
            
            if board[y+i][x] != '.':
                return False
        return True
    #checks right
    if y == y_to and x < x_to:
        for i in range(1 ,abs(x_diff)):
            
            if board[y][x+i] != '.':
                return False
        return True
    #checks left
    if y == y_to and x > x_to:
        for i in range(1 ,abs(x_diff)):
            
            if board[y][x-i] != '.':
                return False
        return True
    

# helper function to figure out if a move is legal for straight-line moves (rooks, bishops, queens, pawns)
# returns True if the path is clear for a move (from-square and to-square), non-inclusive
def isDiagonalClear(from_square, to_square, board):

    y = from_square[0]
    x = from_square[1]
    y_to = to_square[0]
    x_to = to_square[1]

    try:
        
        slope = (float(y) - y_to) / (x - x_to)
    except:
        slope = 0

    print(slope)
    
    y_diff = y - y_to
   
    #right slope Down
    if slope == -1 and y > y_to:
        for i in range(1 ,abs(y_diff)):
            if board[y-i][x+i] != '.':
                return False
        return True
    #right slope up
    elif slope == 1 and y < y_to:
        for i in range(1 ,abs(y_diff)):
            if board[y+i][x+i] != '.':
                return False
        return True
    #left Slope Up
    elif slope == -1 and y < y_to:
        for i in range(1 ,abs(y_diff)):
            
            if board[y+i][x-i] != '.':
                return False
        return True
    #left slope down
    elif slope == 1 and y > y_to:      
        for i in range(1 ,abs(y_diff)):
            
            if board[y-i][x-i] != '.':
                
                return False
        return True
    return False

def GetListOfLegalMoves(board, turn):
    legalMoves = {}
    for frm_y in range(0, 8):
        for frm_x in range(0, 8):
            if turn == 'white' and board[frm_y][frm_x].isupper():
                to_list = []
                for to_y in range(0, 8):
                    for to_x in range(0, 8):
                        temp = copy.deepcopy(board)
                        if IsMoveLegal(temp, (frm_y, frm_x), (to_y, to_x)) and DoesMovePutPlayerInCheck(temp, (frm_y, frm_x), (to_y, to_x), "white") is False:
                            to_list.append((to_y,to_x))         
                    if len(to_list) != 0:
                        legalMoves.update({(frm_y, frm_x):to_list})
            if turn == 'black' and board[frm_y][frm_x].islower():
                to_list = []
                for to_y in range(0, 8):
                  for to_x in range(0, 8):
                    temp = copy.deepcopy(board)
                    if IsMoveLegal(temp, (frm_y, frm_x), (to_y, to_x)) and DoesMovePutPlayerInCheck(temp, (frm_y, frm_x), (to_y, to_x), "black") is False:
                        to_list.append((to_y,to_x))
                if len(to_list) != 0:
                    legalMoves.update({(frm_y, frm_x):to_list})
    #print(legalMoves, "\n")
    return legalMoves

def IsInCheck(board, turn):
    king_piece = 'K'
    king_loc = (None, None)
    if turn == "black":
        king_piece = 'k'
    for row in range(0, len(board)):
        for col in range(0, len(board[row])):
            if board[row][col] == king_piece:
                king_loc = (row, col)
    for row in range(0, 8):
        for col in range(0, 8):
            if turn == "black" and board[row][col].isupper():
                if IsMoveLegal(board, (col, row), king_loc):
                    return True
            elif board[row][col].islower():
                if IsMoveLegal(board, (col, row), king_loc):
                    return True
    return False
def DoesMovePutPlayerInCheck(board, from_square, to_square, turn):

    isCheck = IsInCheck(MovePiece(board, from_square, to_square), turn)
    
    return isCheck

board = ChessBoardSetup()
DrawBoard(board)
board[0][0] = 'r'
board[0][1] = '.'
board[0][2] = 'P'
board[0][3] = '.'
board[0][4] = 'q'
board[0][5] = 'k'
board[0][6] = 't'
board[0][7] = '.'
board[1][0] = '.'
board[1][1] = '.'
board[1][2] = 't'
board[1][3] = '.'
board[1][4] = 'P'
board[1][5] = 'p'
board[1][6] = '.'
board[1][7] = 'r'
board[2][6] = 'p'
board[3][0] = 'p'
board[3][4] = 'P'
board[3][7] = 'p'
board[4][0] = 'P'
board[4][4] = 'P'
board[5][0] = 'R'
board[5][7] = 'P'
board[6][0] = '.'
board[6][1] = '.'
board[6][2] = '.'
board[6][3] = '.'
board[6][4] = '.'
board[6][7] = '.'

to = (4,7)
from_ = (3,7)
print()
DrawBoard(board)
print(DoesMovePutPlayerInCheck(board, from_, to, 'black')