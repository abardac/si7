from random import *
from copy import deepcopy
from math import sqrt

class Player(object):

    #initialises gameboard with x's in corners
    #adding corners to corner array
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

    #will shrink gameboard to required size after certain number of moves
    #used for alpha beta so copies of resources are passed in too
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
            #adds new corners to corner array
            state.corners.clear()
            state.corners.append((1,1))
            state.corners.append((6,1))
            state.corners.append((6,6))
            state.corners.append((1,6))
            #checks for any new captures from corners now that gameboard has shrunk
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

    #checks if any new captures occur at te corners after the gameboard shrinks
    def check_corners_after_shrink(state):
        #at each corner will check if there are two adjacent opposite coloured pieces in a row
        #in a certain direction from that corner
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

    #removes piece from board and piece array passed in
    #used for alpha beta so copies of resources passed in too
    def capture_piece(loc, pieces, board):
        #print(loc)
        #print(pieces)
        #Player.print_gameboard(board)
        pieces.remove(loc)
        board[loc[0]][loc[1]] = '-'

    #after an action(placement or movement), must check if any pieces are captured
    #used for alpha beta so copies of resources passed in too
    def check_capture_after_action(self,action,state):
        if state.colour == self.colour:
            o_pieces = state.o_pieces
            e_pieces = state.e_pieces
        else:
            o_pieces = state.e_pieces
            e_pieces = state.o_pieces

        #checks for adjacent opposite colour pieces and then checks if 
        #same colour is on other side in the same direction 
        if (action[0],action[1]+1) in e_pieces and (action[0],action[1]+2) in o_pieces:
            Player.capture_piece((action[0],action[1]+1),e_pieces,state.board)
        if (action[0],action[1]-1) in e_pieces and (action[0],action[1]-2) in o_pieces:
            Player.capture_piece((action[0],action[1]-1),e_pieces,state.board)
        if (action[0]+1,action[1]) in e_pieces and (action[0]+2,action[1]) in o_pieces:
            Player.capture_piece((action[0]+1,action[1]),e_pieces,state.board)
        if (action[0]-1,action[1]) in e_pieces and (action[0]-2,action[1]) in o_pieces:
            Player.capture_piece((action[0]-1,action[1]),e_pieces,state.board)

        #checks against corners too
        if (action[0],action[1]+1) in e_pieces and (action[0],action[1]+2) in state.corners:
            Player.capture_piece((action[0],action[1]+1),e_pieces,state.board)
        if (action[0],action[1]-1) in e_pieces and (action[0],action[1]-2) in state.corners:
            Player.capture_piece((action[0],action[1]-1),e_pieces,state.board)
        if (action[0]+1,action[1]) in e_pieces and (action[0]+2,action[1]) in state.corners:
            Player.capture_piece((action[0]+1,action[1]),e_pieces,state.board)
        if (action[0]-1,action[1]) in e_pieces and (action[0]-2,action[1]) in state.corners:
            Player.capture_piece((action[0]-1,action[1]),e_pieces,state.board)

        #check for stupid move(piece moves to where itself is captured)
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

    #completes a certain move in the piece array and board passed in
    #used for alpha beta so copies of resources passed in too
    def complete_move(self,move,state):

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

        #checks whether its move caused a capture
        Player.check_capture_after_action(self,move[1],state)

    #completes the placement of a certain piece
    #used for alpha beta so copies of resources passed in too
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
    
    #checks whether a movement is possible
    #used for alpha beta so copies of resources passed in too
    def can_move(x,y,board):
        #only if within gameboard can it possibly be a legal move 
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            #only if space is free/within x boundary
            if board[x][y] == '-':
                return True
            else: 
                return False
        else:
            return False

    #checks whether a jump is possible
    #used for alpha beta so copies of resources passed in too
    def can_jump(x,y,mid_x,mid_y,state):
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            #only if theres a piece between dest and a piece's current loc
            #will it possibly be allowed to jump
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

    #finds all possible legal moves capable by a certain player
    ##used for alpha beta so copies of resources passed in too
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

        #print(moves)
        return moves

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
    
    #checks whether the game has ended (no more pieces of a colour)
    #used for alpha beta so copies of resources passed in too
    def check_game_end(state):
        #check if either piece array is empty 
        if len(state.o_pieces) < 2 or len(state.e_pieces) < 2:
            return True
        else: 
            return False

    # Checks if any of the given pieces are endangered in the placement stage.
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
    Returns True if one of the following conditions are met:
        There is an enemy piece one position to the right.
        There is an enemy piece two positions to the right (with a piece to the right of it to jump over).
    '''
    def chk_two_right(empty_x, empty_y, e_player, board):
        if empty_x < 7 and board[empty_x+1][empty_y] == e_player:
            return True
        elif (empty_x+1) < 7 and board[empty_x+2][empty_y] == e_player and board[empty_x+1][empty_y] != '-':
            return True

    # Checks if any of the given pieces are endangered in the movement stage.
    def is_edan_movement(piece, e_player, board):
        piece_x = piece[0]
        piece_y = piece[1]
        
        if 0 < piece_x < 7 and board[piece_x-1][piece_y] == '-':
            if board[piece_x+1][piece_y] == e_player or board[piece_x+1][piece_y] == 'x':
                empty_x = piece_x-1
                empty_y = piece_y

                if Player.chk_two_left(empty_x, empty_y, e_player, board): return True
                if Player.chk_two_up(empty_x, empty_y, e_player, board): return True
                if Player.chk_two_down(empty_x, empty_y, e_player, board): return True

        elif 0 < piece_x < 7 and board[piece_x+1][piece_y] == '-':
            if board[piece_x-1][piece_y] == e_player or board[piece_x-1][piece_y] == 'x':
                empty_x = piece_x+1
                empty_y = piece_y

                if Player.chk_two_right(empty_x, empty_y, e_player, board): return True
                if Player.chk_two_up(empty_x, empty_y, e_player, board): return True
                if Player.chk_two_down(empty_x, empty_y, e_player, board): return True

        elif 0 < piece_y < 7 and board[piece_x][piece_y-1] == '-':
            if board[piece_x][piece_y+1] == e_player or board[piece_x][piece_y+1] == 'x':
                empty_x = piece_x
                empty_y = piece_y-1

                if Player.chk_two_down(empty_x, empty_y, e_player, board): return True
                if Player.chk_two_left(empty_x, empty_y, e_player, board): return True
                if Player.chk_two_right(empty_x, empty_y, e_player, board): return True

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
        Returns the difference in pieces between the opponent and you.
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
        Movement Adaptation: Checks more positions (e.g. opponent pieces that can jump and capture your piece).
    '''
    def chk_edan_movement(o_pieces, e_player, board):
        num_edan = 0

        for piece in o_pieces:
            if Player.is_edan_movement(piece, e_player, board):
                num_edan += 1
        return num_edan

    #gets the weighting of the eval function in determining movements close to the gameboard shrinking
    def get_panic_weight(move_diff,piece_diff):
        if piece_diff <= 0:
            return (50*(abs(piece_diff)+1))/move_diff
        else: 
            return 100/(move_diff*piece_diff)

    def chk_shrink_edan(self,total_num_moves,state):
        edan_pieces = 0
        #endangered pieces in current player gameboard state, not from alpha beta
        curr_edan_pieces = 0
        risk = 0

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

    def move_to_centre(self,state):
        total = 0
        cen_x = 3.5
        cen_y = 3.5
        
        for p in state.o_pieces:
            total += sqrt((cen_x-p[0])**2+(cen_y-p[1])**2)

        return total

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

    # Returns the score of a given board state based on placement features.
    def eval_placement(self,state):
        total = 0

        while state is not None:
            ideal_place = Player.ideal_placement(self,state)
            num_diff_pieces = Player.num_diff_pieces(self,state)
            edan_o_pieces = Player.chk_edan_placement(state.o_pieces, 'B', state.board)
            edan_e_pieces = Player.chk_edan_placement(state.e_pieces, 'W', state.board)

            total += (3-state.depth)*(50*num_diff_pieces - edan_o_pieces + edan_e_pieces + 30*ideal_place)

            state = state.prev_state

        return total

    # Returns the score of a given board state based on movement features.
    def eval_movement(self,total_num_moves,state):
        total = 0

        while state is not None:
            num_diff_pieces = Player.num_diff_pieces(self,state)
            edan_o_pieces = Player.chk_edan_movement(state.o_pieces, 'B', state.board)
            edan_e_pieces = Player.chk_edan_movement(state.e_pieces, 'W', state.board)
            fortress = Player.maintain_fort(self,state)
            centralised = Player.move_to_centre(self,state)
            shrink_eval = 0
            if (total_num_moves > 128 and total_num_moves < 152) or (total_num_moves > 192 and total_num_moves < 216):
                shrink_eval = Player.chk_shrink_edan(self,total_num_moves,state)

            total += (3-state.depth)*(50*num_diff_pieces - edan_o_pieces + edan_e_pieces + shrink_eval - centralised+ 30*fortress)

            state = state.prev_state
        
        return total

    #COMPLETE EVALUATION FUNCTION FOR ALPHA BETA
    def evaluate(self,total_num_moves,curr_depth,state):

        # Placement stage.
        if total_num_moves < 24:
            return Player.eval_placement(self,state)

        # Movement stage.
        else:
            return Player.eval_movement(self,total_num_moves,state)

    def alpha_beta(self,state):

        best_val = -10000
        beta = 10000

        if self.total_moves >= 24:
            poss_moves = Player.legal_moves(self,state)
        else:
            poss_moves = Player.legal_placements(state)

        if len(poss_moves) == 0:
            self.best_move = None
            return
        
        for move in poss_moves:
            #must make copies of all resources before evaluating and furthering search
            #board_copy = deepcopy(state.board)
            #o_p_copy = deepcopy(state.o_pieces)
            #e_p_copy = deepcopy(state.e_pieces)
            #colour_copy = deepcopy(state.colour)
            #corners_copy = deepcopy(state.corners)

            #state_copy = State(colour_copy,o_p_copy,e_p_copy,corners_copy,board_copy,0)
            state_copy = deepcopy(state)

            #makes move in copied resources 
            if self.total_moves >= 24:
                Player.complete_move(self,move,state_copy)
            else:
                Player.complete_place(self,move,state_copy)

            if state_copy.colour == 'black':
                state_copy.colour = 'white'
            else:
                state_copy.colour = 'black'

            value = Player.min_value(self,best_val,beta,state_copy,0)

            if value > best_val:
                best_val = value
                if self.total_moves >= 24:
                    self.best_move = move
                else:
                    self.best_placement = move

    def max_value(self,alpha, beta, state, curr_depth):
        #depth limit has been reached or game has ended will cause state to be evaluated 
        if curr_depth >= self.p_depth or Player.check_game_end(state):
            score = Player.evaluate(self,self.total_moves,curr_depth,state)
            return score

        #ensures board is right size before finding all possible moves
        if self.total_moves + curr_depth == 152:
            Player.shrink_gameboard("medium",state)
        elif self.total_moves + curr_depth == 216:
            Player.shrink_gameboard("small",state)

        value = -10000
        #gets all possible moves capable by the specific player
        if self.total_moves >= 24:
            poss_moves = Player.legal_moves(self,state)
        else:
            poss_moves = Player.legal_placements(state)

        for move in poss_moves:
            #must make copies of all resources before evaluating and furthering search
            state_copy = deepcopy(state)

            state_copy.depth = curr_depth+1
            state_copy.prev_state = state

            #makes move in copied resources 
            if self.total_moves >= 24:
                Player.complete_move(self,move,state_copy)
            else:
                Player.complete_place(self,move,state_copy)

            if state_copy.colour == 'black':
                state_copy.colour = 'white'
            else:
                state_copy.colour = 'black'

            value = max(value, Player.min_value(self,alpha,beta,state_copy,curr_depth+1))

            if value >= beta:
                return value

            alpha = max(alpha, value)

        return value

    def min_value(self,alpha, beta, state, curr_depth):
        #depth limit has been reached or game has ended will cause state to be evaluated 
        if curr_depth >= self.p_depth or Player.check_game_end(state):
            score = Player.evaluate(self,self.total_moves,curr_depth,state)
            return score

        #ensures board is right size before finding all possible moves
        if self.total_moves + curr_depth == 152:
            Player.shrink_gameboard("medium",state)
        elif self.total_moves + curr_depth == 216:\
            Player.shrink_gameboard("small",state)

        value = 10000
        #gets all possible moves capable by the specific player
        if self.total_moves >= 24:
            poss_moves = Player.legal_moves(self,state)
        else:
            poss_moves = Player.legal_placements(state)

        for move in poss_moves:
            state_copy = deepcopy(state)

            state_copy.depth = curr_depth+1
            state_copy.prev_state = state

            #makes move in copied resources 
            if self.total_moves >= 24:
                Player.complete_move(self,move,state_copy)
            else:
                Player.complete_place(self,move,state_copy)

            if state_copy.colour == 'black':
                state_copy.colour = 'white'
            else:
                state_copy.colour = 'black'

            value = min(value, Player.max_value(self,alpha,beta,state_copy,curr_depth+1))

            if value <= alpha:
                return value
            beta = min(beta, value)

        return value

    def random_place(self):
        if(self.curr_turn == 'white'):
            fir_lim = 0
            sec_lim = 5
        else:
            fir_lim = 2
            sec_lim = 7
        x = randint(fir_lim,sec_lim)
        y = randint(0,7)
        invalid_places = [(0,0),(0,7),(7,0),(7,7)]
        taken = False
        while(not taken):
            if (x,y) in self.our_pieces:
                x = randint(fir_lim,sec_lim)
                y = randint(0,7)
            elif (x,y) in self.enemy_pieces:
                x = randint(fir_lim,sec_lim)
                y = randint(0,7)
            elif (x,y) in invalid_places:
                x = randint(fir_lim,sec_lim)
                y = randint(0,7)
            else: 
                taken = True

        return ((x,y))

    #reverses the ordering of the move 
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


    def __init__(self, colour):
        self.best_move = None
        self.best_placement = None
        #depth of alpha beta
        self.p_depth = 2
        self.total_moves = 0
        #tracks who's turn it is
        self.curr_turn = 'white'
        #self.our_pieces = []
        #self.enemy_pieces = []
        #self.corners = []
        self.colour = colour
        #self.gameboard = Player.init_gameboard(self)
        self.curr_state = State('white',[],[],[],[],0)
        self.curr_state.board = Player.init_gameboard(self.curr_state)


    #used for testing to see the current state of our gameboard in a formatted way
    def print_gameboard(board):
        for row in board:
            print(row)

    def action(self,turns):

        #shrinks gameboard at start of turn 128 and 192 for white player (first player to move)
        if (turns == 128 and self.colour == "white"):
            Player.shrink_gameboard("medium",self.curr_state)
        elif (turns == 192 and self.colour == "white"):
            Player.shrink_gameboard("small",self.curr_state)

        if self.total_moves < 24:
            #rand_place = Player.random_place(self)
            #Player.complete_place(rand_place,self.curr_turn,self.our_pieces,self.enemy_pieces,self.corners,self.gameboard)
            Player.alpha_beta(self,self.curr_state)
            Player.complete_place(self,self.best_placement,self.curr_state)
            
            if self.curr_turn == 'black':
                self.curr_turn = 'white'
                self.curr_state.colour = 'white'
            else:
                self.curr_turn = 'black'
                self.curr_state.colour = 'black'

            self.total_moves += 1

            #return Player.reverse_move(rand_place)
            return Player.reverse_move(self.best_placement)
        else:
            Player.alpha_beta(self,self.curr_state)

            # Added here.
            #print("selected move: ",self.best_move, "curr_turn: ",self.curr_turn, " turns: ", turns)
            # Added here.

            Player.complete_move(self,self.best_move,self.curr_state)

            if self.curr_turn == 'black':
                self.curr_turn = 'white'
                self.curr_state.colour = 'white'
            else:
                self.curr_turn = 'black'
                self.curr_state.colour = 'black'

            self.total_moves += 1

            #shrinks gameboard for black player at the end of their 127 or 191 turn to avoid any corner capture errors
            if (turns == 127 and self.colour == "black"):
                Player.shrink_gameboard("medium",self.curr_state)
            elif (turns == 191 and self.colour == "black"):
                Player.shrink_gameboard("small",self.curr_state)
            
            #print(self.our_pieces)
            #print(self.enemy_pieces)
            #Player.print_gameboard(self)
            return Player.reverse_move(self.best_move)

    def update(self, action):
        
        if action is not None:
            #checks if action is movement(tuple inside tuple) or placement(single tuple)
            if isinstance(action[0], tuple):
                Player.complete_move(self,Player.reverse_move(action),self.curr_state)
            else:
                Player.complete_place(self,Player.reverse_move(action),self.curr_state)

        if self.curr_turn == 'black':
            self.curr_turn = 'white'
            self.curr_state.colour = 'white'
        else:
            self.curr_turn = 'black'
            self.curr_state.colour = 'black'

        self.total_moves += 1

class State:

    def __init__(self,colour,o_pieces,e_pieces,corners,board,depth):
        self.colour = colour
        self.o_pieces = o_pieces
        self.e_pieces = e_pieces
        self.corners = corners
        self.board = board
        self.depth = depth
        self.prev_state = None

    def __deepcopy__(self, memo): # memo is a dict of id's to copies
        id_self = id(self)        # memoization avoids unnecesary recursion
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

