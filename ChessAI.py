
import string
import random
import os
import sys
import time
import copy

horizontal = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}
vertical = {0:"8", 1:"7", 2:"6", 3:"5", 4:"4", 5:"3", 6:"2", 7:"1"}

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

    return board



def MovePiece(board, from_piece, to_piece):
    # write code to move the one chess piece
    # you do not have to worry about the validity of the move - this will be done before calling this function
    # this function will at least take the move (from-peice and to-piece) as input and return the new board layout
    new_board = copy.deepcopy(board)
    new_board[to_piece[0]][to_piece[1]] = new_board[from_piece[0]][from_piece[1]]
    new_board[from_piece[0]][from_piece[1]] = '.'

    if new_board[to_piece[0]][to_piece[1]] == 'P' and to_piece[0] == 0:
        new_board[to_piece[0]][to_piece[1]] = 'Q'
    if new_board[to_piece[0]][to_piece[1]] == 'p' and to_piece[0] == 7:
        new_board[to_piece[0]][to_piece[1]] = 'q'

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


# gets a list of legal moves for a given piece
# input = from-square
# output = list of to-square locations where the piece can move to
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



# returns True if the current player is in checkmate, else False
def IsCheckmate(board, turn):
    if IsInCheck(board, turn) and GetListOfLegalMoves(board, turn) == {}:
        return True
    else:
        return False

# returns True if the given player is in Check state
def IsInCheck(board, turn):
    king_piece = 'K'
    king_loc = (None, None)
    if turn == "black":
        king_piece = 'k'
    for row in range(0, len(board)):
        for col in range(0, len(board[row])):
            if board[row][col] == king_piece:
                king_loc = (row, col)
    if king_loc == (None, None):
        return True
    for row in range(0, 8):
        for col in range(0, 8):
            if turn == "black" and board[row][col].isupper():
                if IsMoveLegal(board, (row, col), king_loc):
                    return True
            elif board[row][col].islower():
                if IsMoveLegal(board, (row, col), king_loc):
                    return True
    return False
                
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

def DoesMovePutPlayerInCheck(board, from_square, to_square, turn):

    isCheck = IsInCheck(MovePiece(board, from_square, to_square), turn)
    
    return isCheck
  

def GetRandomMove(board, turn):
    # pick a random piece and a random legal move for that piece
    moves = GetListOfLegalMoves(board, turn)
    if len(moves) == 0:
        return None

    rand_piece = random.randint(0, len(moves) - 1 )
    random_move = None
    i = 0
    
    for piece in moves:
        if i == rand_piece:
            rand_move = random.randint(0, len(moves.get(piece)) - 1)
            j=0
            for move in moves.get(piece):
                if j == rand_move:
                    random_move = (piece, move)
                j+=1
            break
        i+=1
    return random_move


def evl(board):
    piece_to_points = {
        "p": -1,
        "P": 1,
        "r":-5,
        "R":5,
        "t":-3,
        "T":3,
        "b":-3,
        "B":3,
        "q":-9,
        "Q":9,
        "k":-1500,
        "K":1500,
        ".":0
    }
    board_eval = 0
    for row in board:
        for piece in row:
            board_eval+=piece_to_points.get(piece)
    return board_eval # Negative means black is winning, Postivie means white is winning


def GetMinMaxMove(board, depth, turn): # Returns the best move 

    legalMoves = GetListOfLegalMoves(board, turn)
    best_board = None
    best_move =  None
    for piece in legalMoves:
        for to in legalMoves.get(piece):
            test_board = MovePiece(board, piece, to)
            if turn == "black":
                board_rating = MinMax(test_board, depth-1, True)
                if best_board is None or best_board > board_rating:
                    best_board = board_rating
                    best_move = [piece, to]
            else:
                board_rating = MinMax(test_board, depth-1, False)

                if best_board is None or best_board < board_rating:
                    best_board = board_rating
                    best_move = [piece, to]
    return best_move
               


def MinMax(board, depth, move): # Returns  value of the board
     # Base Case
    if depth == 0:
        return evl(board)
     # Recurive Case
    if move:
        value = -5000
        legalMoves = GetListOfLegalMoves(board, "white")
        for piece in legalMoves:
            for to in legalMoves.get(piece):
                test_board = MovePiece(board, piece, to)
                value = max(value, MinMax(test_board, depth-1, move))
        return value
    else:
        value = 5000
        legalMoves = GetListOfLegalMoves(board, "black") 
        for piece in legalMoves:
            for to in legalMoves.get(piece):
                test_board = MovePiece(board, piece, to)
                value = min(value, MinMax(test_board, depth-1, move))
        return value


def player (board, move):
    possible_moves = {}
    
    for i in move.keys():
        temp_P = (horizontal[i[1]], vertical[i[0]])
        possible_moves_to = []
        for j in move[i]:
            possible_moves_to.append((horizontal[j[1]], vertical[j[0]]))
            
            
        possible_moves[temp_P] =  possible_moves_to
    print("\nPossible moves that you can make")
    for keys in possible_moves.keys():
        print(keys[0] + "" + keys[1] + " to ", end="")
        for value in possible_moves[keys]:
            print(value[0] + " or " + value[1] + " ", end="")
        print()
    while True:
        print()
        break


# Main Game Loop
def main():
    game_mode = False
    board = ChessBoardSetup()
    turns = 0
    turn = "white" 
    stalemate = False

    #choose game mode to play
    
    print("Choose 1 for player VS AI anything else for AI vs AI: ")
    option = str(input()).lower()
    if option == "1":
        game_mode = True
        
    else:
        print("AI verses AI has been selected")
            
    
    # AI
    if game_mode == False:
        # "white" or "black" for the random ai
        while True:
            print("Enter which side you would like to be the random AI (white or black): ")
            randomSide = str(input()).lower()
            if randomSide == "black" or randomSide == "white":
                break  
            else:
                print("please try again incorrect input")
        # number of turns to look ahead for the min-max
        while True:
            print("Enter the depth of moves you would like the min-max AI to look ahead: ")
            depth = input()
            if depth.isdigit() :
                print(depth + " been selected as depth of moves the min-max will look ahead")
                depth = int(depth)
                break  
            else:
                print("please try again incorrect input")
    # Player
    else:
        #chose AI
        print("Choose the AI 1 for min-max anything else is the random AI: ")
        option = str(input()).lower()
        if option == "1":
            option = "min_max"
        
        else:
            option = "random"

        if option == "min_max":
            while True:
                print("Enter the depth of moves you would like the min-max AI to look ahead: ")
                depth = input()
                if depth.isdigit() :
                    print(depth + " been selected as depth of moves the min-max will look ahead")
                    depth = int(depth)
                    break  
                else:
                    print("please try again incorrect input")
        
        print("Enter Black to start on black side and anything else for white: ")
        side = str(input()).lower()
        if not side == "black":
            side = "white"

            

        
    # Limit before end the program and stalemate is called
    while True:
        print("Enter the limit of moves you would like ex(100, 50, 500): ")
        N = input()
        if N.isdigit() :
            print(N + " been selected as the limit of moves")
            N = int(N)
            break  
        else:
            print("please try again incorrect input")
    
    # Continue while not in checkmate or stalemate (<N turns)
    while not IsCheckmate(board, turn) and turns < N and not stalemate:
        
        print("%s to move:" % (turn))
        DrawBoard(board)
        
        # Get the best move for turn, or get the random move for turn based off of randomSide
        move = None
        if game_mode == False:
            if randomSide == turn:
                move = GetRandomMove(board, turn)

                if move is None:
                    
                    stalemate = True
                    continue
            else:
                move = GetMinMaxMove(board, depth, turn)
                
                if move is None:
                    stalemate = True
                    continue
        else:
            if turn == side:
                move = player(board, GetListOfLegalMoves(board, turn))
                
                if move is None:
                    stalemate = True
                    continue
            else:
                if option == "random":
                    move = GetRandomMove(board, turn)

                    if move is None:
                    
                        stalemate = True
                        continue
                else:
                    move = GetMinMaxMove(board, depth, turn)
                
                    if move is None:
                        stalemate = True
                        continue

        # Return will look like move = [(x_from, y_from), (x_to, y_to)]
        board = MovePiece(board, move[0], move[1])

        # write code to take turns and move the pieces
        time.sleep(0.5)
        # clears the board after each turn
        os.system('cls')

        # Changes
        if turn == "white":
            turn = "black"
        else:
            turn = "white"
            turns+=1

    print("%s to move:" % (turn))
    DrawBoard(board)

    # Declare Winner
    if IsCheckmate(board, turn):
        # Switchback
        if turn == "white":
            turn = "black"
        else:
            turn = "white"
        print(turn + " has CHECKMATE")
      
    else:
        # Switchback
        if turn == "white":
            turn = "black"
        else:
            turn = "white"
        print(turn + " has STALEMATE")


if __name__ == "__main__":
    main()