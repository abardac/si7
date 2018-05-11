from random import *
from copy import deepcopy
from math import sqrt

'''
Class of the gameboard state.
Used to store relevant info about that state and,
used while searching to differentiate the states appropriately.
'''
class State:

    '''
    Initialises a gameboard state with relevant attributes.
    '''
    def __init__(self,colour,o_pieces,e_pieces,corners,board,depth):
        self.colour = colour #the colour of the player who's turn it is in that state
        self.o_pieces = o_pieces
        self.e_pieces = e_pieces
        self.corners = corners
        self.board = board
        self.depth = depth
        self.prev_state = None #the state previous to this one in the alpha beta

    '''
    Creates a copy of the state to be used while searching.
    '''
    def __deepcopy__(self, memo): # memo is a dict of id's to copies.
        id_self = id(self)        # memorization avoids unnecessary recursion.
        _copy = memo.get(id_self)
        if _copy is None:
            _copy = type(self)(
                deepcopy(self.colour, memo), 
                deepcopy(self.o_pieces, memo),
                deepcopy(self.e_pieces, memo),
                deepcopy(self.corners, memo),
                deepcopy(self.board, memo),
                0)
            memo[id_self] = _copy 
        return _copy

'''
Our final AI player class that includes:
    Minimax,
    Alpha beta,
    Custom Evaluation Function & Features.
'''
class Player(object):

    '''
    Initialises gameboard with x's in corners.
    Adds corners to the corner array for future reference.
    '''
    def init_gameboard(state):
        gameboard = [
        ['x','-','-','-','-','-','-','x']
        ,['-','-','-','-','-','-','-','-']
        ,['-','-','-','-','-','-','-','-']
        ,['-','-','-','-','-','-','-','-']
        ,['-','-','-','-','-','-','-','-']
        ,['-','-','-','-','-','-','-','-']
        ,['-','-','-','-','-','-','-','-']
        ,['x','-','-','-','-','-','-','x']]

        state.corners.append((0,0))
        state.corners.append((0,7))
        state.corners.append((7,0))
        state.corners.append((7,7))

        return gameboard

    '''
    Initialises the player, with relevant attributes to keep track of.
        E.g. Gameboard, search depth, total moves, etc.
    '''
    def __init__(self, colour):
        self.best_move = None
        self.best_placement = None
        self.p_depth = 2          # Depth of alpha beta.
        self.total_moves = 0
        self.curr_turn = 'white'  # Tracks who's turn it is.
        self.colour = colour
        self.curr_state = State('white',[],[],[],[],0)
        self.curr_state.board = Player.init_gameboard(self.curr_state)

    '''
    Removes the given piece from the board and appropriate player piece array.
    Note: Part of alpha beta, so it's given copied state resources to work with.
    '''
    def capture_piece(loc, pieces, board):
        pieces.remove(loc)
        board[loc[0]][loc[1]] = '-'

    '''
    Checks if any captures occur at the new corners after the gameboard shrinks.
    '''
    def check_corners_after_shrink(state):
      
        # Appropriately checks if there are two adjacent opposite coloured pieces in a row at each corner.
        for c in state.corners:
            if (c[0]+1,c[1]) in state.o_pieces and (c[0]+2,c[1]) in state.e_pieces:
                Player.capture_piece((c[0]+1,c[1]),state.o_pieces,state.board)
            if (c[0]+1,c[1]) in state.e_pieces and (c[0]+2,c[1]) in state.o_pieces:
                Player.capture_piece((c[0]+1,c[1]),state.e_pieces,state.board)
            if (c[0]-1,c[1]) in state.o_pieces and (c[0]-2,c[1]) in state.e_pieces:
                Player.capture_piece((c[0]-1,c[1]),state.o_pieces,state.board)
            if (c[0]-1,c[1]) in state.e_pieces and (c[0]-2,c[1]) in state.o_pieces:
                Player.capture_piece((c[0]-1,c[1]),state.e_pieces,state.board)
            if (c[0],c[1]+1) in state.o_pieces and (c[0],c[1]+2) in state.e_pieces:
                Player.capture_piece((c[0],c[1]+1),state.o_pieces,state.board)
            if (c[0],c[1]+1) in state.e_pieces and (c[0],c[1]+2) in state.o_pieces:
                Player.capture_piece((c[0],c[1]+1),state.e_pieces,state.board)
            if (c[0],c[1]-1) in state.o_pieces and (c[0],c[1]-2) in state.e_pieces:
                Player.capture_piece((c[0],c[1]-1),state.o_pieces,state.board)
            if (c[0],c[1]-1) in state.e_pieces and (c[0],c[1]-2) in state.o_pieces:
                Player.capture_piece((c[0],c[1]-1),state.e_pieces,state.board)

    '''
    Shrinks the gameboard to the required size after a certain number of moves.
    Makes sure to eliminate out-of-bound pieces and make any appropriate corner captures.
    Note: Part of alpha beta, so it's given copied state resources to work with.
    '''
    def shrink_gameboard(size,state):
        if size == "medium":
            for i in range(8):
                for j in range(8):
                    if i == 0 or i == 7 or j == 0 or j == 7 or (i,j) == (1,1) or (i,j) == (1,6) or (i,j) == (6,1) or (i,j) == (6,6):
                        if (i,j) in state.o_pieces: state.o_pieces.remove((i,j))
                        if (i,j) in state.e_pieces: state.e_pieces.remove((i,j))
                        state.board[i][j] = 'O'
            state.board[1][1] = 'x'
            state.board[1][6] = 'x'
            state.board[6][1] = 'x'
            state.board[6][6] = 'x'

            # Adds new corners to the corner array.
            state.corners.clear()
            state.corners.append((1,1))
            state.corners.append((6,1))
            state.corners.append((6,6))
            state.corners.append((1,6))

            # Checks for any new captures from corners now that the gameboard has shrunk.
            Player.check_corners_after_shrink(state)
            
        elif size == "small": 
            for i in range(1,7):
                for j in range(1,7):
                    if i == 1 or i == 6 or j == 1 or j == 6 or (i,j) == (2,2) or (i,j) == (2,5) or (i,j) == (5,2) or (i,j) == (5,5):
                        if (i,j) in state.o_pieces: state.o_pieces.remove((i,j))
                        if (i,j) in state.e_pieces: state.e_pieces.remove((i,j))
                        state.board[i][j] = 'O'

            state.board[2][2] = 'x'
            state.board[2][5] = 'x'
            state.board[5][2] = 'x'
            state.board[5][5] = 'x'

            state.corners.clear()
            state.corners.append((2,2))
            state.corners.append((5,2))
            state.corners.append((5,5))
            state.corners.append((2,5))

            Player.check_corners_after_shrink(state)
    
    '''
    After an action (in placement or movement), check if any pieces have been captured.
    Note: Part of alpha beta, so it's given copied state resources to work with.
    '''
    def check_capture_after_action(self,action,state):
        #ensures we are using the correct resources for 'our' move or enemy's
        if state.colour == self.colour:
            o_pieces = state.o_pieces
            e_pieces = state.e_pieces
        else:
            o_pieces = state.e_pieces
            e_pieces = state.o_pieces

        '''
        Checks for adjacent opposite colour pieces and then,
        checks if the same colour is on the other side in the same direction.
        '''
        if (action[0],action[1]+1) in e_pieces and (action[0],action[1]+2) in o_pieces:
            Player.capture_piece((action[0],action[1]+1),e_pieces,state.board)
        if (action[0],action[1]-1) in e_pieces and (action[0],action[1]-2) in o_pieces:
            Player.capture_piece((action[0],action[1]-1),e_pieces,state.board)
        if (action[0]+1,action[1]) in e_pieces and (action[0]+2,action[1]) in o_pieces:
            Player.capture_piece((action[0]+1,action[1]),e_pieces,state.board)
        if (action[0]-1,action[1]) in e_pieces and (action[0]-2,action[1]) in o_pieces:
            Player.capture_piece((action[0]-1,action[1]),e_pieces,state.board)

        # Checks against corners too.
        if (action[0],action[1]+1) in e_pieces and (action[0],action[1]+2) in state.corners:
            Player.capture_piece((action[0],action[1]+1),e_pieces,state.board)
        if (action[0],action[1]-1) in e_pieces and (action[0],action[1]-2) in state.corners:
            Player.capture_piece((action[0],action[1]-1),e_pieces,state.board)
        if (action[0]+1,action[1]) in e_pieces and (action[0]+2,action[1]) in state.corners:
            Player.capture_piece((action[0]+1,action[1]),e_pieces,state.board)
        if (action[0]-1,action[1]) in e_pieces and (action[0]-2,action[1]) in state.corners:
            Player.capture_piece((action[0]-1,action[1]),e_pieces,state.board)

        # Checks for stupid moves (piece moves to where it will be captured).
        if (action[0]-1,action[1]) in e_pieces and (action[0]+1,action[1]) in e_pieces:
            Player.capture_piece(action,o_pieces,state.board)
        elif (action[0],action[1]-1) in e_pieces and (action[0],action[1]+1) in e_pieces:
            Player.capture_piece(action,o_pieces,state.board)
        elif (action[0]-1,action[1]) in e_pieces and (action[0]+1,action[1]) in state.corners:
            Player.capture_piece(action,o_pieces,state.board)
        elif (action[0]-1,action[1]) in state.corners and (action[0]+1,action[1]) in e_pieces:
            Player.capture_piece(action,o_pieces,state.board)
        elif (action[0],action[1]-1) in e_pieces and (action[0],action[1]+1) in state.corners:
            Player.capture_piece(action,o_pieces,state.board)
        elif (action[0],action[1]-1) in state.corners and (action[0],action[1]+1) in e_pieces:
            Player.capture_piece(action,o_pieces,state.board)

    '''
    Completes a given move with the given state.
    Note: Part of alpha beta, so it's given copied state resources to work with.
    '''
    def complete_move(self,move,state):
        #ensures we are using the correct resources for the movement
        if state.colour == self.colour:
            pieces = state.o_pieces
        else:
            pieces = state.e_pieces
        
        move_index = pieces.index(move[0])
        pieces[move_index] = move[1]
        state.board[move[0][0]][move[0][1]] = '-'

        if state.colour == 'black':
            state.board[move[1][0]][move[1][1]] = 'B'
        else:
            state.board[move[1][0]][move[1][1]] = 'W'

        # Checks whether the move caused a capture.
        Player.check_capture_after_action(self,move[1],state)

    '''
    Completes the placement of a certain piece.
    Note: Part of alpha beta, so it's given copied state resources to work with.
    '''
    def complete_place(self,action,state):

        if state.colour == self.colour:
            pieces = state.o_pieces
        else:
            pieces = state.e_pieces
        
        if action not in pieces:
            pieces.append(action)

        if state.colour == 'black':
            state.board[action[0]][action[1]] = 'B'
        else:
            state.board[action[0]][action[1]] = 'W'

        Player.check_capture_after_action(self,action,state)
    
    '''
    Checks whether a move is possible & legal.
    Note: Part of alpha beta, so it's given copied state resources to work with.
    '''
    def can_move(x,y,board):
        
        # Only a legal move if within the gameboard.
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:

            # Only if space is free/within x boundary.
            if board[x][y] == '-':
                return True
            else: 
                return False
        else:
            return False

    '''
    Checks whether a jump is possible.
    Note: Part of alpha beta, so it's given copied state resources to work with.
    '''
    def can_jump(x,y,mid_x,mid_y,state):
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            '''
            Only if there's a piece between the dest and,
            a piece's current loc will it possibly be allowed to jump.
            '''
            if (mid_x,mid_y) in state.o_pieces:
                if state.board[x][y] == '-':
                    return True
                else: 
                    return False
            elif (mid_x,mid_y) in state.e_pieces:
                if state.board[x][y] == '-':
                    return True
                else: 
                    return False
            else: 
                return False
        else:
            return False

    '''
    Finds all possible legal moves capable by a certain player.
    Note: Part of alpha beta, so it's given copied state resources to work with.
    '''
    def legal_moves(self,state):
        if state.colour == self.colour:
            pieces = state.o_pieces
        else:
            pieces = state.e_pieces

        moves = []

        for p in pieces:
            if Player.can_move(p[0]+1,p[1],state.board): moves.append((p,(p[0]+1,p[1])))
            if Player.can_move(p[0]-1,p[1],state.board): moves.append((p,(p[0]-1,p[1])))
            if Player.can_move(p[0],p[1]+1,state.board): moves.append((p,(p[0],p[1]+1)))
            if Player.can_move(p[0],p[1]-1,state.board): moves.append((p,(p[0],p[1]-1)))
            if Player.can_jump(p[0]+2,p[1],p[0]+1,p[1],state): moves.append((p,(p[0]+2,p[1])))
            if Player.can_jump(p[0]-2,p[1],p[0]-1,p[1],state): moves.append((p,(p[0]-2,p[1])))
            if Player.can_jump(p[0],p[1]+2,p[0],p[1]+1,state): moves.append((p,(p[0],p[1]+2)))
            if Player.can_jump(p[0],p[1]-2,p[0],p[1]-1,state): moves.append((p,(p[0],p[1]-2)))

        return moves

    '''
    Finds all possible legal placements capable by a certain player.
    Note: Part of alpha beta, so it's given copied state resources to work with.
    '''
    def legal_placements(state):
        if(state.colour == 'white'):
            fir_lim = 0
            sec_lim = 5
        else:
            fir_lim = 2
            sec_lim = 7

        placements = []

        for i in range(fir_lim,sec_lim):
            for j in range(8):
                if state.board[i][j] == '-':
                    placements.append((i,j))

        return placements
    
    '''
    Checks whether the game has ended.
    If either player has less than 2 pieces left.
    Note: Part of alpha beta, so it's given copied state resources to work with.
    '''
    def check_game_end(state):
        if len(state.o_pieces) < 2 or len(state.e_pieces) < 2:
            return True
        else: 
            return False

    '''
    Checks if any of the given pieces are endangered in the placement stage.
    By checking whether there's an opponent piece next to any of their pieces.
    '''
    def is_edan_placement(piece, e_player, board):
        piece_x = piece[0]
        piece_y = piece[1]
        
        if 0 < piece_x < 7 and board[piece_x-1][piece_y] == '-':
            if board[piece_x+1][piece_y] == e_player or board[piece_x+1][piece_y] == 'x':
                return True
        elif 0 < piece_x < 7 and board[piece_x+1][piece_y] == '-':
            if board[piece_x-1][piece_y] == e_player or board[piece_x-1][piece_y] == 'x':
                return True
        elif 0 < piece_y < 7 and board[piece_x][piece_y-1] == '-':
            if board[piece_x][piece_y+1] == e_player or board[piece_x][piece_y+1] == 'x':
                return True
        elif 0 < piece_y < 7 and board[piece_x][piece_y+1] == '-':
            if board[piece_x][piece_y-1] == e_player or board[piece_x][piece_y-1] == 'x':
                return True
        return False

    '''
    Checks if any enemy pieces are dangerously nearby (upwards).
    Returns True if one of the following conditions are met:
        There is an enemy piece one position above.
        There is an enemy piece two positions above (with a piece below it to jump over).
    '''
    def chk_two_up(empty_x, empty_y, e_player, board):
        if empty_y < 7 and board[empty_x][empty_y+1] == e_player:
            return True
        elif (empty_y+1) < 7 and board[empty_x][empty_y+2] == e_player and board[empty_x][empty_y+1] != '-':
            return True

    '''
    Checks if any enemy pieces are dangerously nearby (downwards).
    Returns True if one of the following conditions are met:
        There is an enemy piece one position below.
        There is an enemy piece two positions below (with a piece above it to jump over).
    '''
    def chk_two_down(empty_x, empty_y, e_player, board):
        if 0 < empty_y and board[empty_x][empty_y-1] == e_player:
            return True
        elif 0 < (empty_y-1) and board[empty_x][empty_y-2] == e_player and board[empty_x][empty_y-1] != '-':
            return True

    '''
    Checks if any enemy pieces are dangerously nearby (to th left).
    Returns True if one of the following conditions are met:
        There is an enemy piece one position to the left.
        There is an enemy piece two positions to the left (with a piece to the right of it to jump over).
    '''
    def chk_two_left(empty_x, empty_y, e_player, board):
        if 0 < empty_x and board[empty_x-1][empty_y] == e_player:
            return True
        elif 0 < (empty_x-1) and board[empty_x-2][empty_y] == e_player and board[empty_x-1][empty_y] != '-':
            return True

    '''
    Checks if any enemy pieces are dangerously nearby (to the right).
    Returns True if one of the following conditions are met:
        There is an enemy piece one position to the right.
        There is an enemy piece two positions to the right (with a piece to the right of it to jump over).
    '''
    def chk_two_right(empty_x, empty_y, e_player, board):
        if empty_x < 7 and board[empty_x+1][empty_y] == e_player:
            return True
        elif (empty_x+1) < 7 and board[empty_x+2][empty_y] == e_player and board[empty_x+1][empty_y] != '-':
            return True

    '''
    Checks if the given piece is endangered in the movement stage and,
    can be captured next round by the opponent, given the positioning of their pieces.
    '''
    def is_edan_movement(piece, e_player, board):
        piece_x = piece[0]
        piece_y = piece[1]
        
        # If an opponent's piece is to the right, check other direction vulnerabilities.
        if 0 < piece_x < 7 and board[piece_x-1][piece_y] == '-':
            if board[piece_x+1][piece_y] == e_player or board[piece_x+1][piece_y] == 'x':
                empty_x = piece_x-1
                empty_y = piece_y

                if Player.chk_two_left(empty_x, empty_y, e_player, board): return True
                if Player.chk_two_up(empty_x, empty_y, e_player, board): return True
                if Player.chk_two_down(empty_x, empty_y, e_player, board): return True

        # If an opponent's piece is to the left, check other direction vulnerabilities.
        elif 0 < piece_x < 7 and board[piece_x+1][piece_y] == '-':
            if board[piece_x-1][piece_y] == e_player or board[piece_x-1][piece_y] == 'x':
                empty_x = piece_x+1
                empty_y = piece_y

                if Player.chk_two_right(empty_x, empty_y, e_player, board): return True
                if Player.chk_two_up(empty_x, empty_y, e_player, board): return True
                if Player.chk_two_down(empty_x, empty_y, e_player, board): return True

        # If an opponent's piece is above, check other direction vulnerabilities.
        elif 0 < piece_y < 7 and board[piece_x][piece_y-1] == '-':
            if board[piece_x][piece_y+1] == e_player or board[piece_x][piece_y+1] == 'x':
                empty_x = piece_x
                empty_y = piece_y-1

                if Player.chk_two_down(empty_x, empty_y, e_player, board): return True
                if Player.chk_two_left(empty_x, empty_y, e_player, board): return True
                if Player.chk_two_right(empty_x, empty_y, e_player, board): return True

        # If an opponent's piece is below, check other direction vulnerabilities.
        elif 0 < piece_y < 7 and board[piece_x][piece_y+1] == '-':
            if board[piece_x][piece_y-1] == e_player or board[piece_x][piece_y-1] == 'x':
                empty_x = piece_x
                empty_y = piece_y+1

                if Player.chk_two_up(empty_x, empty_y, e_player, board): return True
                if Player.chk_two_left(empty_x, empty_y, e_player, board): return True
                if Player.chk_two_right(empty_x, empty_y, e_player, board): return True

        return False

    '''
    Feature 1:
        Returns the change in the number of their pieces vs our pieces,
        based on piece numbers in the original gameboard vs that of the current explored gameboard.
    '''
    def num_diff_pieces(self,state):
        return (len(self.curr_state.e_pieces)-len(state.e_pieces)) - (len(self.curr_state.o_pieces)-len(state.o_pieces))

    '''
    Feature 2 & 3:
        Returns how many of the given player's pieces are endangered,
        By either the opponent's pieces or a corner piece.
    '''
    def chk_edan_placement(o_pieces, e_player, board):
        num_edan = 0
        for piece in o_pieces:
            if Player.is_edan_placement(piece, e_player, board):
                num_edan += 1
        return num_edan

    '''
    Feature 2 & 3:
        Returns how many of the given player's pieces are endangered,
        By either the opponent's pieces or a corner piece.
        Movement Adaptation: Checks more positions (e.g. opponent pieces that can jump and capture a piece).
    '''
    def chk_edan_movement(o_pieces, e_player, board):
        num_edan = 0

        for piece in o_pieces:
            if Player.is_edan_movement(piece, e_player, board):
                num_edan += 1
        return num_edan

    '''
    Calculates the weighting for determining movements close to the gameboard shrinking.
    '''
    def get_panic_weight(move_diff,piece_diff):
        '''
        if we are at a piece disadvantage, moving away from the edges is in our best 
        interests, if at an advantage then we can afford to give up some pieces if necessary
        '''
        if piece_diff <= 0:
            return (50*(abs(piece_diff)+1))/move_diff
        else: 
            return 100/(move_diff*piece_diff)

    '''
    Number of pieces that are endangered by the shrinking of the gameboard,
    with an increasing "panic" weight to get pieces out before its shrunk.
    '''
    def chk_shrink_edan(self,total_num_moves,state):
        risk = 0
        edan_pieces = 0

        # Endangered pieces in the current player gameboard state, not from alpha beta.
        curr_edan_pieces = 0

        # For the first shrinking phase.
        if total_num_moves > 128 and total_num_moves < 152:
            corners = [(1,1),(1,6),(6,1),(6,6)]
            move_diff = 152 - total_num_moves
            for piece in state.o_pieces:
                if piece[0] == 0 or piece[1] == 0 or piece[0] == 7 or piece[1] == 7 or piece in corners:
                    edan_pieces += 1
            for piece in self.curr_state.o_pieces:
                if piece[0] == 0 or piece[1] == 0 or piece[0] == 7 or piece[1] == 7 or piece in corners:
                    curr_edan_pieces += 1
            panic_weight = Player.get_panic_weight(move_diff,len(state.o_pieces)-len(state.e_pieces))
            risk = panic_weight*(curr_edan_pieces-edan_pieces)

        # For the second shrinking phase.
        # Note: More weight for this stage, as all remaining pieces are valuable at this stage.
        else:
            corners = [(2,2),(2,5),(5,2),(5,5)]
            move_diff = 216 - total_num_moves
            for piece in state.o_pieces:
                if piece[0] == 1 or piece[1] == 1 or piece[0] == 6 or piece[1] == 6 or piece in corners:
                    edan_pieces += 1
            for piece in self.curr_state.o_pieces:
                if piece[0] == 1 or piece[1] == 1 or piece[0] == 6 or piece[1] == 6 or piece in corners:
                    curr_edan_pieces += 1
            panic_weight = Player.get_panic_weight(move_diff,len(state.o_pieces)-len(state.e_pieces))
            risk = 2*panic_weight*(curr_edan_pieces-edan_pieces)

        return risk

    '''
    Calculates the distance of the piece to the center,
    in an effort to get stranded/isolated pieces to a safer location.
    '''
    def move_to_centre(self,state):
        total = 0
        cen_x = 3.5
        cen_y = 3.5
        
        for p in state.o_pieces:
            total += sqrt( (cen_x-p[0])**2 + (cen_y-p[1])**2 )

        return total

    '''
    Rewards movement that helps build a 2x2 fort,
    with three different fort positions to prioritise the best one,
    while considering other positions in case we can't get the most ideal.
    '''
    def maintain_fort(self,state):
        total = 0
        if self.colour == 'white':
            ideal_fort1 = [(4,3),(4,4),(3,3),(3,4)]
            ideal_fort2 = [(3,3),(3,4),(2,3),(2,4)]
            ideal_fort3 = [(1,3),(1,4),(2,3),(2,4)]
        else:
            ideal_fort1 = [(4,3),(4,4),(3,3),(3,4)]
            ideal_fort2 = [(4,3),(4,4),(5,3),(5,4)]
            ideal_fort3 = [(5,3),(5,4),(6,3),(6,4)]

        if (all(x in state.o_pieces for x in ideal_fort1)):
            total += 3
        if (all(x in state.o_pieces for x in ideal_fort2)):
            total += 2
        if (all(x in state.o_pieces for x in ideal_fort3)):
            total += 1

        return total

    '''
    Rewards placements based on the given weights of each position in the gameboard.
    Note: Helps setup the "fortress" strategy in the movement phase.
    '''
    def ideal_placement(self,state):
        total = 0
        
        if self.colour == 'white':
            weighted_board = [
            [0,0,0,0,0,0,0,0]
            ,[0,0,1,2,2,1,0,0]
            ,[0,1,3,4,4,3,1,0]
            ,[0,1,3,5,5,3,1,0]
            ,[0,0,1,6,6,1,0,0]
            ,[0,0,0,1,1,0,0,0]
            ,[0,0,0,0,0,0,0,0]
            ,[0,0,0,0,0,0,0,0]]
        else:
            weighted_board = [
            [0,0,0,0,0,0,0,0]
            ,[0,0,0,0,0,0,0,0]
            ,[0,0,0,1,1,0,0,0]
            ,[0,0,1,6,6,1,0,0]
            ,[0,1,3,5,5,3,1,0]
            ,[0,1,3,4,4,3,1,0]
            ,[0,0,1,2,2,1,0,0]
            ,[0,0,0,0,0,0,0,0]]

        for p in state.o_pieces:
            total += weighted_board[p[0]][p[1]]
        
        return total

    '''
    Returns the score of a given board state based on placement features.
    '''
    def eval_placement(self,state):
        total = 0

        #loops through all states that led to the terminal state
        while state is not None:
            num_diff_pieces = Player.num_diff_pieces(self,state)
            edan_o_pieces = Player.chk_edan_placement(state.o_pieces, 'B', state.board)
            edan_e_pieces = Player.chk_edan_placement(state.e_pieces, 'W', state.board)
            ideal_place = Player.ideal_placement(self,state)

            #give a greater weighting to earlier stages to ensure we making the better choices early on
            total += (3-state.depth)*(150*num_diff_pieces - 120*edan_o_pieces + 20*edan_e_pieces + 5*ideal_place)
            state = state.prev_state

        return total

    '''
    Returns the score of a given board state based on movement features.
    '''
    def eval_movement(self,total_num_moves,state):
        total = 0

        while state is not None:
            num_diff_pieces = Player.num_diff_pieces(self,state)
            edan_o_pieces = Player.chk_edan_movement(state.o_pieces, 'B', state.board)
            edan_e_pieces = Player.chk_edan_movement(state.e_pieces, 'W', state.board)
            centralised = Player.move_to_centre(self,state)
            fortress = Player.maintain_fort(self,state)

            shrink_eval = 0
            if (total_num_moves > 128 and total_num_moves < 152) or (total_num_moves > 192 and total_num_moves < 216):
                shrink_eval = Player.chk_shrink_edan(self,total_num_moves,state)

            total += (3-state.depth)*(150*num_diff_pieces - 120*edan_o_pieces + 30*edan_e_pieces + 40*shrink_eval - 20*centralised + 15*fortress)
            state = state.prev_state
        
        return total

    '''
    Evaluates the score of a move/state based on features in the:
    Placement and movement stages appropriately.
    '''
    def evaluate(self,total_num_moves,curr_depth,state):

        # Placement stage.
        if total_num_moves < 24:
            return Player.eval_placement(self,state)
        # Movement stage.
        else:
            return Player.eval_movement(self,total_num_moves,state)

    '''
    Our alpha beta implementation.
    '''
    def alpha_beta(self,state):
        beta = 10000
        alpha = -10000

        #Gets all possible moves capable by the specific player.
        if self.total_moves >= 24:
            poss_moves = Player.legal_moves(self,state)
        else:
            poss_moves = Player.legal_placements(state)

        #If no possible moves then must return a 'None' move to referee.
        if len(poss_moves) == 0:
            self.best_move = None
            return
        
        for move in poss_moves:
            #Makes a copy of the state before searching.
            state_copy = deepcopy(state)

            # Makes move in the copied state.
            if self.total_moves >= 24:
                Player.complete_move(self,move,state_copy)
            else:
                Player.complete_place(self,move,state_copy)

            #Change colour of new state as the other player must now make their move
            state_copy.colour = Player.change_colour(state_copy.colour)

            value = Player.min_value(self,alpha,beta,state_copy,0)

            #If returned value is greater than the current alpha then that is the best action so far
            if value > alpha:
                #This greater value is the new alpha
                alpha = value
                if self.total_moves >= 24:
                    self.best_move = move
                else:
                    self.best_placement = move

    '''
    Calculates and returns the maximum evaluation score for states at a certain depth.
    '''
    def max_value(self,alpha, beta, state, curr_depth):
        value = -10000

        # Depth limit has been reached or game has ended will cause the state to be evaluated.
        if curr_depth >= self.p_depth or Player.check_game_end(state):
            score = Player.evaluate(self,self.total_moves,curr_depth,state)
            return score

        # Ensures board is the right size before finding all possible moves.
        if self.total_moves + curr_depth == 152:
            Player.shrink_gameboard("medium",state)
        elif self.total_moves + curr_depth == 216:
            Player.shrink_gameboard("small",state)

        # Gets all possible moves capable by the specific player.
        if self.total_moves >= 24:
            poss_moves = Player.legal_moves(self,state)
        else:
            poss_moves = Player.legal_placements(state)

        for move in poss_moves:
            # Makes a copy of the state before searching.
            state_copy = deepcopy(state)

            state_copy.depth = curr_depth+1
            #Adds previous state in record for better evaluation 
            state_copy.prev_state = state

            # Makes the move in the copied state.
            if self.total_moves >= 24:
                Player.complete_move(self,move,state_copy)
            else:
                Player.complete_place(self,move,state_copy)

            state_copy.colour = Player.change_colour(state_copy.colour)

            value = max(value, Player.min_value(self,alpha,beta,state_copy,curr_depth+1))

            '''
            prunes the rest of poss_moves if score returned is greater than beta
            because even if score would increase (since it is maximising player),
            beta will never get smaller and theres no point checking the rest as the 
            minimising player wouldn't choose anything down this branch. 
            '''
            if value >= beta:
                return value

            alpha = max(alpha, value)

        return value

    '''
    Calculates and returns the minimum evaluation score for states at a certain depth.
    '''
    def min_value(self,alpha, beta, state, curr_depth):
        value = 10000

        # Depth limit has been reached or game has ended will cause the state to be evaluated.
        if curr_depth >= self.p_depth or Player.check_game_end(state):
            score = Player.evaluate(self,self.total_moves,curr_depth,state)
            return score

        # Ensures board is the right size before finding all possible moves.
        if self.total_moves + curr_depth == 152:
            Player.shrink_gameboard("medium",state)
        elif self.total_moves + curr_depth == 216:
            Player.shrink_gameboard("small",state)

        # Gets all possible moves capable by the specific player.
        if self.total_moves >= 24:
            poss_moves = Player.legal_moves(self,state)
        else:
            poss_moves = Player.legal_placements(state)

        for move in poss_moves:
            # Makes a copy of the state before searching.
            state_copy = deepcopy(state)

            state_copy.depth = curr_depth+1
            state_copy.prev_state = state

            # Makes the move in the copied state.
            if self.total_moves >= 24:
                Player.complete_move(self,move,state_copy)
            else:
                Player.complete_place(self,move,state_copy)

            state_copy.colour = Player.change_colour(state_copy.colour)

            value = min(value, Player.max_value(self,alpha,beta,state_copy,curr_depth+1))

            '''
            prunes the rest of poss_moves if value is less than alpha
            because even if the minimising player gets a better (lower) score, it 
            will never be higher than alpha and so is not important for the
            topmost maximising player, and so min player will return its best (min) score
            which is its beta value
            '''
            if value <= alpha:
                return value

            beta = min(beta, value)

        return value

    '''
    Reverses the ordering of the move.
    ''' 
    def reverse_move(action):
        if isinstance(action[0], tuple):
            fir_x = action[0][0]
            fir_y = action[0][1]
            sec_x = action[1][0]
            sec_y = action[1][1]

            return ((fir_y,fir_x),(sec_y,sec_x))
        else:
            fir_x = action[0]
            fir_y = action[1]

            return (fir_y,fir_x)

    '''
    Changes the player to the other colour
    '''
    def change_colour(colour):
        if colour == 'black':
            return 'white'
        else:
            return 'black'

    '''
    Decides on an action based on variables such as:
        Gameboard phase (Placement/Movement)
    Uses alpha beta to finding the best outcome action.
    '''
    def action(self,turns):

        # Shrinks gameboard at start of turn 128 and 192 for white player (first player to move).
        if (turns == 128 and self.colour == "white"):
            Player.shrink_gameboard("medium",self.curr_state)
        elif (turns == 192 and self.colour == "white"):
            Player.shrink_gameboard("small",self.curr_state)

        # If in placement stage.
        if self.total_moves < 24:
            Player.alpha_beta(self,self.curr_state)
            Player.complete_place(self,self.best_placement,self.curr_state)

            #Changes colour in the player and state for who's turn it is
            self.curr_turn = Player.change_colour(self.curr_turn)
            self.curr_state.colour = Player.change_colour(self.curr_state.colour)

            self.total_moves += 1

            return Player.reverse_move(self.best_placement)

        # If in movement stage.
        else:
            Player.alpha_beta(self,self.curr_state)
            if self.best_move is not None:
                Player.complete_move(self,self.best_move,self.curr_state)

            #Changes colour in the player and state for who's turn it is
            self.curr_turn = Player.change_colour(self.curr_turn)
            self.curr_state.colour = Player.change_colour(self.curr_state.colour)

            self.total_moves += 1

            # Shrinks gameboard for black player at the end of turn 127 and 191 to avoid any corner capture errors.
            if (turns == 127 and self.colour == "black"):
                Player.shrink_gameboard("medium",self.curr_state)
            elif (turns == 191 and self.colour == "black"):
                Player.shrink_gameboard("small",self.curr_state)
            
            return Player.reverse_move(self.best_move)

    '''
    Updates the state of the game for each player's turn.
    '''
    def update(self, action):

        # Checks if the action is movement or placement.
        if action is not None:
            if isinstance(action[0], tuple):
                Player.complete_move(self,Player.reverse_move(action),self.curr_state)
            else:
                Player.complete_place(self,Player.reverse_move(action),self.curr_state)

        #Changes colour in the player and state for who's turn it is
        self.curr_turn = Player.change_colour(self.curr_turn)
        self.curr_state.colour = Player.change_colour(self.curr_state.colour)

        self.total_moves += 1
