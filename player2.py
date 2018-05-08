from random import *
import copy

class Player(object):

    #initialises gameboard with x's in corners
    #adding corners to corner array
    def init_gameboard(self):
        gameboard = [
        ['x','-','-','-','-','-','-','x']
        ,['-','-','-','-','-','-','-','-']
        ,['-','-','-','-','-','-','-','-']
        ,['-','-','-','-','-','-','-','-']
        ,['-','-','-','-','-','-','-','-']
        ,['-','-','-','-','-','-','-','-']
        ,['-','-','-','-','-','-','-','-']
        ,['x','-','-','-','-','-','-','x']]

        self.corners.append((0,0))
        self.corners.append((0,7))
        self.corners.append((7,0))
        self.corners.append((7,7))

        return gameboard

    #will shrink gameboard to required size after certain number of moves
    #used for alpha beta so copies of resources are passed in too
    def shrink_gameboard(size,o_pieces,e_pieces,corners,board):
        if size == "medium":
            for i in range(8):
                for j in range(8):
                    if i == 0 or i == 7 or j == 0 or j == 7 or (i,j) == (1,1) or (i,j) == (1,6) or (i,j) == (6,1) or (i,j) == (6,6):
                        if (i,j) in o_pieces: o_pieces.remove((i,j))
                        if (i,j) in e_pieces: e_pieces.remove((i,j))
                        board[i][j] = 'O'
            board[1][1] = 'x'
            board[1][6] = 'x'
            board[6][1] = 'x'
            board[6][6] = 'x'
            #adds new corners to corner array
            corners.clear()
            corners.append((1,1))
            corners.append((6,1))
            corners.append((6,6))
            corners.append((1,6))
            #checks for any new captures from corners now that gameboard has shrunk
            Player.check_corners_after_shrink(o_pieces,e_pieces,corners,board)
        elif size == "small": 
            for i in range(1,7):
                for j in range(1,7):
                    if i == 1 or i == 6 or j == 1 or j == 6 or (i,j) == (2,2) or (i,j) == (2,5) or (i,j) == (5,2) or (i,j) == (5,5):
                        if (i,j) in o_pieces: o_pieces.remove((i,j))
                        if (i,j) in e_pieces: e_pieces.remove((i,j))
                        board[i][j] = 'O'
            board[2][2] = 'x'
            board[2][5] = 'x'
            board[5][2] = 'x'
            board[5][5] = 'x'
            corners.clear()
            corners.append((2,2))
            corners.append((5,2))
            corners.append((5,5))
            corners.append((2,5))
            Player.check_corners_after_shrink(o_pieces,e_pieces,corners,board)

    #checks if any new captures occur at te corners after the gameboard shrinks
    def check_corners_after_shrink(o_pieces,e_pieces,corners,board):
        #at each corner will check if there are two adjacent opposite coloured pieces in a row
        #in a certain direction from that corner
        for corner in corners:
            if (corner[0]+1,corner[1]) in o_pieces and (corner[0]+2,corner[1]) in e_pieces:
                Player.capture_piece((corner[0]+1,corner[1]),o_pieces,board)
            if (corner[0]+1,corner[1]) in e_pieces and (corner[0]+2,corner[1]) in o_pieces:
                Player.capture_piece((corner[0]+1,corner[1]),e_pieces,board)
            if (corner[0]-1,corner[1]) in o_pieces and (corner[0]-2,corner[1]) in e_pieces:
                Player.capture_piece((corner[0]-1,corner[1]),o_pieces,board)
            if (corner[0]-1,corner[1]) in e_pieces and (corner[0]-2,corner[1]) in o_pieces:
                Player.capture_piece((corner[0]-1,corner[1]),e_pieces,board)
            if (corner[0],corner[1]+1) in o_pieces and (corner[0],corner[1]+2) in e_pieces:
                Player.capture_piece((corner[0],corner[1]+1),o_pieces,board)
            if (corner[0],corner[1]+1) in e_pieces and (corner[0],corner[1]+2) in o_pieces:
                Player.capture_piece((corner[0],corner[1]+1),e_pieces,board)
            if (corner[0],corner[1]-1) in o_pieces and (corner[0],corner[1]-2) in e_pieces:
                Player.capture_piece((corner[0],corner[1]-1),o_pieces,board)
            if (corner[0],corner[1]-1) in e_pieces and (corner[0],corner[1]-2) in o_pieces:
                Player.capture_piece((corner[0],corner[1]-1),e_pieces,board)

    #removes piece from board and piece array passed in
    #used for alpha beta so copies of resources passed in too
    def capture_piece(loc, pieces, board):
        pieces.remove(loc)
        board[loc[0]][loc[1]] = '-'

    #after an action(placement or movement), must check if any pieces are captured
    #used for alpha beta so copies of resources passed in too
    def check_capture_after_action(action,o_pieces,e_pieces,corners,board):
        #checks for adjacent opposite colour pieces and then checks if 
        #same colour is on other side in the same direction 
        if (action[0],action[1]+1) in e_pieces and (action[0],action[1]+2) in o_pieces:
            Player.capture_piece((action[0],action[1]+1),e_pieces,board)
        if (action[0],action[1]-1) in e_pieces and (action[0],action[1]-2) in o_pieces:
            Player.capture_piece((action[0],action[1]-1),e_pieces,board)
        if (action[0]+1,action[1]) in e_pieces and (action[0]+2,action[1]) in o_pieces:
            Player.capture_piece((action[0]+1,action[1]),e_pieces,board)
        if (action[0]-1,action[1]) in e_pieces and (action[0]-2,action[1]) in o_pieces:
            Player.capture_piece((action[0]-1,action[1]),e_pieces,board)

        #checks against corners too
        if (action[0],action[1]+1) in e_pieces and (action[0],action[1]+2) in corners:
            Player.capture_piece((action[0],action[1]+1),e_pieces,board)
        if (action[0],action[1]-1) in e_pieces and (action[0],action[1]-2) in corners:
            Player.capture_piece((action[0],action[1]-1),e_pieces,board)
        if (action[0]+1,action[1]) in e_pieces and (action[0]+2,action[1]) in corners:
            Player.capture_piece((action[0]+1,action[1]),e_pieces,board)
        if (action[0]-1,action[1]) in e_pieces and (action[0]-2,action[1]) in corners:
            Player.capture_piece((action[0]-1,action[1]),e_pieces,board)

        #check for stupid move(piece moves to where itself is captured)
        if (action[0]-1,action[1]) in e_pieces and (action[0]+1,action[1]) in e_pieces:
            Player.capture_piece(action,o_pieces,board)
        elif (action[0],action[1]-1) in e_pieces and (action[0],action[1]+1) in e_pieces:
            Player.capture_piece(action,o_pieces,board)
        elif (action[0]-1,action[1]) in e_pieces and (action[0]+1,action[1]) in corners:
            Player.capture_piece(action,o_pieces,board)
        elif (action[0]-1,action[1]) in corners and (action[0]+1,action[1]) in e_pieces:
            Player.capture_piece(action,o_pieces,board)
        elif (action[0],action[1]-1) in e_pieces and (action[0],action[1]+1) in corners:
            Player.capture_piece(action,o_pieces,board)
        elif (action[0],action[1]-1) in corners and (action[0],action[1]+1) in e_pieces:
            Player.capture_piece(action,o_pieces,board)

    #completes a certain move in the piece array and board passed in
    #used for alpha beta so copies of resources passed in too
    def complete_move(move,player,o_pieces,e_pieces,corners,board):
        
        move_index = o_pieces.index(move[0])
        o_pieces[move_index] = move[1]
        board[move[0][0]][move[0][1]] = '-'
        if player == 'black':
            board[move[1][0]][move[1][1]] = 'B'
        else:
            board[move[1][0]][move[1][1]] = 'W'
       
        #checks whether its move caused a capture
        Player.check_capture_after_action(move[1],o_pieces,e_pieces,corners,board)

    #completes the placement of a certain piece
    #used for alpha beta so copies of resources passed in too
    def complete_place(action,player,o_pieces,e_pieces,corners,board):
        
        if action not in o_pieces:
                o_pieces.append(action)

        if player == 'black':
            board[action[0]][action[1]] = 'B'
        else:
            board[action[0]][action[1]] = 'W'

        Player.check_capture_after_action(action,o_pieces,e_pieces,corners,board)
    
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
    def can_jump(x,y,mid_x,mid_y,o_pieces,e_pieces,board):
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            #only if theres a piece between dest and a piece's current loc
            #will it possibly be allowed to jump
            if (mid_x,mid_y) in o_pieces:
                if board[x][y] == '-':
                    return True
                else: 
                    return False
            elif (mid_x,mid_y) in e_pieces:
                if board[x][y] == '-':
                    return True
                else: 
                    return False
            else: 
                return False
        else:
            return False

    #finds all possible legal moves capable by a certain player
    ##used for alpha beta so copies of resources passed in too
    def legal_moves(o_pieces,e_pieces,board):
        moves = []
        for piece in o_pieces:
            if Player.can_move(piece[0]+1,piece[1],board): moves.append((piece,(piece[0]+1,piece[1])))
            if Player.can_move(piece[0]-1,piece[1],board): moves.append((piece,(piece[0]-1,piece[1])))
            if Player.can_move(piece[0],piece[1]+1,board): moves.append((piece,(piece[0],piece[1]+1)))
            if Player.can_move(piece[0],piece[1]-1,board): moves.append((piece,(piece[0],piece[1]-1)))
            if Player.can_jump(piece[0]+2,piece[1],piece[0]+1,piece[1],o_pieces,e_pieces,board): moves.append((piece,(piece[0]+2,piece[1])))
            if Player.can_jump(piece[0]-2,piece[1],piece[0]-1,piece[1],o_pieces,e_pieces,board): moves.append((piece,(piece[0]-2,piece[1])))
            if Player.can_jump(piece[0],piece[1]+2,piece[0],piece[1]+1,o_pieces,e_pieces,board): moves.append((piece,(piece[0],piece[1]+2)))
            if Player.can_jump(piece[0],piece[1]-2,piece[0],piece[1]-1,o_pieces,e_pieces,board): moves.append((piece,(piece[0],piece[1]-2)))

        return moves
    
    #checks whether the game has ended (no more pieces of a colour)
    #used for alpha beta so copies of resources passed in too
    #EXPAND FOR OTHER SCNARIOS OF GAME ENDING
    def check_game_end(o_pieces,e_pieces):
        #check if either piece array is empty 
        if len(o_pieces) < 2 or len(e_pieces) < 2:
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
    def num_diff_pieces(self,o_pieces, e_pieces):

        return (len(self.enemy_pieces)-len(e_pieces)) - (len(self.our_pieces)-len(o_pieces))

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

    def chk_shrink_edan(self,total_num_moves,o_pieces,e_pieces,corners,board):
        edan_pieces = 0
        #endangered pieces in current player gameboard state, not from alpha beta
        curr_edan_pieces = 0
        risk = 0

        if total_num_moves > 128 and total_num_moves < 152:
            move_diff = 152 - total_num_moves
            for piece in o_pieces:
                if piece[0] == 0 or piece[1] == 0 or piece[0] == 7 or piece[1] == 7 or piece in corners:
                    edan_pieces += 1
            for piece in self.our_pieces:
                if piece[0] == 0 or piece[1] == 0 or piece[0] == 7 or piece[1] == 7 or piece in corners:
                    curr_edan_pieces += 1
            panic_weight = Player.get_panic_weight(move_diff,len(o_pieces)-len(e_pieces))
            risk = panic_weight*(curr_edan_pieces-edan_pieces)
            #if risk > 20:
                #print("panic: ",panic_weight, "move diff: ",move_diff,"piece diff: ",len(o_pieces)-len(e_pieces))
                #print("risk: ",risk,"curr_edan: ",curr_edan_pieces,"edan: ",edan_pieces)
        else:
            move_diff = 216 - total_num_moves
            for piece in o_pieces:
                if piece[0] == 1 or piece[1] == 1 or piece[0] == 6 or piece[1] == 6 or piece in corners:
                    edan_pieces += 1
            for piece in self.our_pieces:
                if piece[0] == 1 or piece[1] == 1 or piece[0] == 6 or piece[1] == 6 or piece in corners:
                    curr_edan_pieces += 1
            panic_weight = Player.get_panic_weight(move_diff,len(o_pieces)-len(e_pieces))
            risk = panic_weight*(curr_edan_pieces-edan_pieces)

        
        #Player.print_gameboard(board)

        return risk

    # Returns the score of a given board state based on placement features.
    def eval_placement(o_pieces, e_pieces, board):
        num_diff_pieces = Player.num_diff_pieces(o_pieces, e_pieces)
        edan_o_pieces = Player.chk_edan_placement(o_pieces, 'B', board)
        edan_e_pieces = Player.chk_edan_placement(e_pieces, 'W', board)

        return 2*num_diff_pieces - edan_o_pieces + edan_e_pieces

    # Returns the score of a given board state based on movement features.
    def eval_movement(self,total_num_moves,o_pieces,e_pieces,corners,board):
        num_diff_pieces = Player.num_diff_pieces(self,o_pieces, e_pieces)
        edan_o_pieces = Player.chk_edan_movement(o_pieces, 'B', board)
        edan_e_pieces = Player.chk_edan_movement(e_pieces, 'W', board)
        shrink_eval = 0
        if (total_num_moves > 128 and total_num_moves < 152) or (total_num_moves > 192 and total_num_moves < 216):
            shrink_eval = Player.chk_shrink_edan(self,total_num_moves,o_pieces,e_pieces,corners,board)

        return 50*num_diff_pieces - edan_o_pieces + edan_e_pieces + shrink_eval

    #COMPLETE EVALUATION FUNCTION FOR ALPHA BETA
    def evaluate(self,total_num_moves,curr_depth,board,o_pieces,e_pieces,corners):

        # Placement stage.
        if total_num_moves < 24:
            return Player.eval_placement(o_pieces, e_pieces, board)

        # Movement stage.
        else:
            return Player.eval_movement(self,total_num_moves,o_pieces, e_pieces, corners,board)

    def alpha_beta(self,o_pieces,e_pieces,corners,board):
        best_val = -10000
        beta = 10000

        corners_copy = corners

        poss_moves = Player.legal_moves(o_pieces,e_pieces,board)
        
        for move in poss_moves:
            #must make copies of all resources before evaluating and furthering search
            board_copy = copy.deepcopy(board)
            o_p_copy = copy.deepcopy(o_pieces)
            e_p_copy = copy.deepcopy(e_pieces)

            #makes move in copied resources 
            Player.complete_move(move,self.curr_turn,o_p_copy,e_p_copy,corners_copy,board_copy)

            value = Player.min_value(self,best_val,beta,board_copy,o_p_copy,e_p_copy,corners_copy,0)

            if value > best_val:
                best_val = value
                self.best_move = move

    def max_value(self,alpha, beta, board, o_pieces, e_pieces, corners, curr_depth):
        #depth limit has been reached or game has ended will cause state to be evaluated 
        if curr_depth >= self.p_depth or Player.check_game_end(o_pieces,e_pieces):
            score = Player.evaluate(self,self.total_moves,curr_depth,board,o_pieces,e_pieces,corners)
            return score
        
        corners_copy = corners

        #ensures board is right size before finding all possible moves
        if self.total_moves + curr_depth == 152:
            corners_copy = copy.deepcopy(corners)
            Player.shrink_gameboard("medium",o_pieces,e_pieces,corners_copy,board)
        elif self.total_moves + curr_depth == 216:
            corners_copy = copy.deepcopy(corners)
            Player.shrink_gameboard("small",o_pieces,e_pieces,corners_copy,board)

        value = -10000
        #gets all possible moves capable by the specific player
        poss_moves = Player.legal_moves(o_pieces,e_pieces,board)

        for move in poss_moves:
            #must make copies of all resources before evaluating and furthering search
            board_copy = copy.deepcopy(board)
            o_p_copy = copy.deepcopy(o_pieces)
            e_p_copy = copy.deepcopy(e_pieces)

            #makes move in copied resources 
            Player.complete_move(move,self.curr_turn,o_p_copy,e_p_copy,corners_copy,board_copy)

            value = max(value, Player.min_value(self,alpha,beta,board_copy,o_p_copy,e_p_copy,corners_copy,curr_depth+1))

            if value >= beta:
                return value

            alpha = max(alpha, value)

        return value

    def min_value(self,alpha, beta, board, o_pieces, e_pieces, corners, curr_depth):
        #depth limit has been reached or game has ended will cause state to be evaluated 
        if curr_depth >= self.p_depth or Player.check_game_end(o_pieces,e_pieces):
            score = Player.evaluate(self,self.total_moves,curr_depth,board,o_pieces,e_pieces,corners)
            return score
        
        corners_copy = corners

        #ensures board is right size before finding all possible moves
        if self.total_moves + curr_depth == 152:
            corners_copy = copy.deepcopy(corners)
            Player.shrink_gameboard("medium",o_pieces,e_pieces,corners_copy,board)
        elif self.total_moves + curr_depth == 216:
            corners_copy = copy.deepcopy(corners)
            Player.shrink_gameboard("small",o_pieces,e_pieces,corners_copy,board)

        value = 10000
        #gets all possible moves capable by the specific player
        poss_moves = Player.legal_moves(o_pieces,e_pieces,board)

        for move in poss_moves:
            board_copy = copy.deepcopy(board)
            o_p_copy = copy.deepcopy(o_pieces)
            e_p_copy = copy.deepcopy(e_pieces)

            #makes move in copied resources 
            Player.complete_move(move,self.curr_turn,o_p_copy,e_p_copy,corners_copy,board_copy)

            value = min(value, Player.max_value(self,alpha,beta,board_copy,o_p_copy,e_p_copy,corners_copy,curr_depth+1))
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
        #depth of alpha beta
        self.p_depth = 2
        self.total_moves = 0
        #tracks who's turn it is
        self.curr_turn = 'white'
        self.our_pieces = []
        self.enemy_pieces = []
        self.corners = []
        self.colour = colour
        self.gameboard = Player.init_gameboard(self)

    #used for testing to see the current state of our gameboard in a formatted way
    def print_gameboard(board):
        for row in board:
            print(row)

    def action(self,turns):

        #shrinks gameboard at start of turn 128 and 192 for white player (first player to move)
        if (turns == 128 and self.colour == "white"):
            Player.shrink_gameboard("medium",self.enemy_pieces,self.our_pieces,self.corners,self.gameboard)
        elif (turns == 192 and self.colour == "white"):
            Player.shrink_gameboard("small",self.enemy_pieces,self.our_pieces,self.corners,self.gameboard)

        if self.total_moves < 24:
            rand_place = Player.random_place(self)
            Player.complete_place(rand_place,self.curr_turn,self.our_pieces,self.enemy_pieces,self.corners,self.gameboard)
            
            if self.curr_turn == 'black':
                self.curr_turn = 'white'
            else:
                self.curr_turn = 'black'

            self.total_moves += 1

            return Player.reverse_move(rand_place)
        else:
            Player.alpha_beta(self,self.our_pieces,self.enemy_pieces,self.corners,self.gameboard)

            # Added here.
            #print("selected move: ",self.best_move, "curr_turn: ",self.curr_turn, " turns: ", turns)
            # Added here.

            Player.complete_move(self.best_move,self.curr_turn,self.our_pieces,self.enemy_pieces,self.corners,self.gameboard)

            if self.curr_turn == 'black':
                self.curr_turn = 'white'
            else:
                self.curr_turn = 'black'

            self.total_moves += 1

            #shrinks gameboard for black player at the end of their 127 or 191 turn to avoid any corner capture errors
            if (turns == 127 and self.colour == "black"):
                Player.shrink_gameboard("medium",self.enemy_pieces,self.our_pieces,self.corners,self.gameboard)
            elif (turns == 191 and self.colour == "black"):
                Player.shrink_gameboard("small",self.enemy_pieces,self.our_pieces,self.corners,self.gameboard)
            
            #print(self.our_pieces)
            #print(self.enemy_pieces)
            #Player.print_gameboard(self)
            return Player.reverse_move(self.best_move)

    def update(self, action):
        
        if action is not None:
            #checks if action is movement(tuple inside tuple) or placement(single tuple)
            if isinstance(action[0], tuple):
                Player.complete_move(Player.reverse_move(action),self.curr_turn,self.enemy_pieces,self.our_pieces,self.corners,self.gameboard)
            else:
                Player.complete_place(Player.reverse_move(action),self.curr_turn,self.enemy_pieces,self.our_pieces,self.corners,self.gameboard)

        if self.curr_turn == 'black':
            self.curr_turn = 'white'
        else:
            self.curr_turn = 'black'
        self.total_moves += 1