class Player(object):

	best_move = None
	#depth of alpha beta
	p_depth = 0
	gameboard = []
	total_moves = 0
	#tracks who's turn it is
	curr_turn = 'white'
	whites = []
	blacks = []

	#initialises gameboard with x's in corners
	def init_gameboard():
		row = []
		for i in range(8):
			row.append('-')
		for j in range(8):
			gameboard.append(row)
		gameboard[0][0] = 'x'
		gameboard[0][7] = 'x'
		gameboard[7][0] = 'x'
		gameboard[7][7] = 'x'

	#will shrink gameboard to required size after certain number of moves
	#used for alpha beta so copies of resources are passed in too
	def shrink_gameboard(moves,w_pieces,b_pieces,board):
		if moves == 128:
			for i in range(8):
				for j in range(8):
					if i == 0 || i == 7 || j == 0 || j == 7:
						if (i,j) in w_pieces: w_pieces.remove((i,j))
						if (i,j) in b_pieces: b_pieces.remove((i,j))
						board[i][j] = 'x'
			board[1][1] = 'x'
			board[1][6] = 'x'
			board[6][1] = 'x'
			board[6][6] = 'x'
		else if moves = 192: 
			for i in range(1,7):
				for j in range(1,7):
					if i == 1 || i == 6 || j == 1 || j == 6:
						if (i,j) in w_pieces: w_pieces.remove((i,j))
						if (i,j) in b_pieces: b_pieces.remove((i,j))
						board[i][j] = 'x'
			board[2][2] = 'x'
			board[2][5] = 'x'
			board[5][2] = 'x'
			board[5][5] = 'x'

	#removes piece from board and piece array passed in
	#used for alpha beta so copies of resources passed in too
	def capture_piece(loc, pieces, board):
		pieces.remove(loc)
		board[loc[0]][loc[1]] = '-'

    #checks if a certain piece is surrounded by pieces of opposite colour
    #used for alpha beta so copies of resources passed in too
	def check_for_capture(loc, pieces, board):
		if (loc[0]+1,loc[1]) in pieces and (loc[0]-1,loc[1]) in pieces:
			capture_piece(loc, pieces, board)
		if (loc[0],loc[1]+1) in whites and (loc[0],loc[1]-1) in whites:
			capture_piece(loc, pieces, board)

	#after an action(placement or movement), must check if any pieces are captured
	#used for alpha beta so copies of resources passed in too
	def check_capture_after_action(action,player,w_pieces,b_pieces,board):
		#checks for adjacent opposite colour pieces and then checks if 
		#same colour is on other side in the same direction 
		if player == 'black':
			if (action[0],action[1]+1) in w_pieces:
				check_for_capture((action[0],action[1]+1),w_pieces,board)
			if (action[0],action[1]-1) in w_pieces:
				check_for_capture((action[0],action[1]-1),w_pieces,board)
			if (action[0]+1,action[1]) in w_pieces:
				check_for_capture((action[0]+1,action[1]),w_pieces,board)
			if (action[0]-1,action[1]) in w_pieces:
				check_for_capture((action[0]-1,action[1]),w_pieces,board)
			#check for stupid move(piece moves to where itself is captured)
			check_for_capture(action, b_pieces, board)
		else:
			if (action[0],action[1]+1) in b_pieces:
				check_for_capture((action[0],action[1]+1),b_pieces,board)
			if (action[0],action[1]-1) in b_pieces:
				check_for_capture((action[0],action[1]-1),b_pieces,board)
			if (action[0]+1,action[1]) in b_pieces:
				check_for_capture((action[0]+1,action[1]),b_pieces,board)
			if (action[0]-1,action[1]) in b_pieces:
				check_for_capture((action[0]-1,action[1]),b_pieces,board)
			check_for_capture(action, w_pieces, board)

	#completes a certain move in the piece array and board passed in
	#used for alpha beta so copies of resources passed in too
	def complete_move(move,player,w_pieces,b_pieces,board):
		if player == 'black':
			move_index = b_pieces.index(move[0])
			b_pieces[move_index] = move[1]
			board[move[0][0]][move[0][1]] = '-'
			board[move[1][0]][move[1][1]] = 'B'
		else:
			move_index = w_pieces.index(move[0])
			w_pieces[move_index] = move[1]
			board[move[0][0]][move[0][1]] = '-'
			board[move[1][0]][move[1][1]] = 'W'

		#checks whether its move caused a capture
		check_capture_after_action(move[1],player,w_pieces,b_pieces,board)

	#completes the placement of a certain piece
	#used for alpha beta so copies of resources passed in too
	def complete_place(action,player,w_pieces,b_pieces,board):
		if player == 'black':
			b_pieces.append(action)
			board[action[0]][action[1]] = 'B'
		else:
			w_pieces.append(action)
			board[action[0]][action[1]] = 'W'

		check_capture_after_action(action,player,w_pieces,b_pieces,board)
    
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
	def can_jump(x,y,mid_x,mid_y,w_pieces,b_pieces,board):
		if x >= 0 and x <= 7 and y >= 0 and y <= 7:
			#only if theres a piece between dest and a piece's current loc
			#will it possibly be allowed to jump
			if (mid_x,mid_y) in b_pieces || (mid_x,mid_y) in w_pieces:
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
	def legal_moves(player,w_pieces,b_pieces,board):
		moves = []
		if player = 'white':
			for piece in w_pieces:
				if can_move(piece[0]+1,piece[1]): moves.append((piece,(piece[0]+1,piece[1])))
				if can_move(piece[0]-1,piece[1]): moves.append((piece,(piece[0]-1,piece[1])))
				if can_move(piece[0],piece[1]+1): moves.append((piece,(piece[0],piece[1]+1)))
				if can_move(piece[0],piece[1]-1): moves.append((piece,(piece[0],piece[1]-1)))
				if can_jump(piece[0]+2,piece[1],piece[0]+1,piece[1]): moves.append((piece,(piece[0]+2,piece[1])))
				if can_jump(piece[0]-2,piece[1],piece[0]-1,piece[1]): moves.append((piece,(piece[0]-2,piece[1])))
				if can_jump(piece[0],piece[1]+2,piece[0],piece[1]+1): moves.append((piece,(piece[0],piece[1]+2)))
				if can_jump(piece[0],piece[1]-2,piece[0],piece[1]-1): moves.append((piece,(piece[0],piece[1]-2)))
		if player = 'black':
			for piece in b_pieces:
				if can_move(piece[0]+1,piece[1]): moves.append((piece,(piece[0]+1,piece[1])))
				if can_move(piece[0]-1,piece[1]): moves.append((piece,(piece[0]-1,piece[1])))
				if can_move(piece[0],piece[1]+1): moves.append((piece,(piece[0],piece[1]+1)))
				if can_move(piece[0],piece[1]-1): moves.append((piece,(piece[0],piece[1]-1)))
				if can_jump(piece[0]+2,piece[1],piece[0]+1,piece[1]): moves.append((piece,(piece[0]+2,piece[1])))
				if can_jump(piece[0]-2,piece[1],piece[0]-1,piece[1]): moves.append((piece,(piece[0]-2,piece[1])))
				if can_jump(piece[0],piece[1]+2,piece[0],piece[1]+1): moves.append((piece,(piece[0],piece[1]+2)))
				if can_jump(piece[0],piece[1]-2,piece[0],piece[1]-1): moves.append((piece,(piece[0],piece[1]-2)))

		return moves
    
    #checks whether the game has ended (no more pieces of a colour)
    #used for alpha beta so copies of resources passed in too
    #EXPAND FOR OTHER SCNARIOS OF GAME ENDING
	def check_game_end(w_pieces,b_pieces):
		#check if either piece array is empty 
		if not w_pieces || not b_pieces:
			return True
		else: 
			return False

    #COMPLETE EVALUATION FUNCTION FOR ALPHA BETA
	def evaluate(board,player,w_pieces,b_pieces):
		return 0

	def alpha_beta(alpha, beta, player, board, w_pieces, b_pieces, curr_depth):

        #depth limit has been reached or game has ended will cause state to be evaluated 
		if curr_depth >= p_depth or check_game_end():
			score = evaluate(board,player,w_pieces,b_pieces)
			return score

	    #ensures board is right size before finding all possible moves
		if total_moves + curr_depth == 128 || total_moves + curr_depth == 192:
			shrink_gameboard(total_moves+curr_depth,w_pieces,b_pieces,board)

		#gets all possible moves capable by the specific player
		poss_moves = legal_moves(player,w_pieces,b_pieces,board)

		if player == curr_turn:
			for move in poss_moves:
				#must make copies of all resources before evaluating and furthering search
				board_copy = list(board)
				w_p_copy = list(w_pieces)
				b_p_copy = list(b_pieces)

                #makes move in copied resources 
				complete_move(move,player,w_p_copy,b_p_copy,board_copy)

                if player == 'black':
                	player = 'white'
                else:
                	player = 'black'

                score = alpha_beta(alpha,beta,player,board_copy,w_p_copy,b_p_copy,curr_depth+1)

                if score > alpha:
                	if curr_depth == 0:
                		best_move = move
                	alpha = score

                if score >= beta:
                	return alpha

            return alpha
        else:
        	for move in poss_moves:
				board_copy = list(board)
				w_p_copy = list(w_pieces)
				b_p_copy = list(b_pieces)

				complete_move(move,player,w_p_copy,b_p_copy,board_copy)

                if player == 'black':
                	player = 'white'
                else:
                	player = 'black'

                score = alpha_beta(alpha,beta,player,board_copy,w_p_copy,b_p_copy,curr_depth+1)

                if score < beta:
                	beta = score

                if alpha >= beta:
                	return beta

            return beta

	def __init__(self, colour):
		self.colour = colour
		init_gameboard()
		self.p_depth = 8

	def action(self,turns):
        alpha = alpha_beta(-10000,10000,curr_turn,gameboard,whites,blacks,0)

        if curr_turn == 'black':
        	curr_turn = 'white'
        else:
        	curr_turn = 'black'

        total_moves += 1

        complete_move(best_move,curr_turn,whites,blacks,gameboard)

        return best_move

	def update(self, action):
		total_moves += 1
		if total_moves == 128 || total_moves = 192:
			shrink_gameboard()

		if action is not None:
			#checks if action is movement(tuple inside tuple) or placement(single tuple)
			if isinstance(action[0], tuple):
				complete_move(action)
			else:
				complete_place(action)

        if curr_turn == 'black':
        	curr_turn = 'white'
        else:
        	curr_turn = 'black'