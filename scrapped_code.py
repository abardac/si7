

#print(loc)
#print(pieces)
#Player.print_gameboard(board)



#must make copies of all resources before evaluating and furthering search
#board_copy = deepcopy(state.board)
#o_p_copy = deepcopy(state.o_pieces)
#e_p_copy = deepcopy(state.e_pieces)
#colour_copy = deepcopy(state.colour)
#corners_copy = deepcopy(state.corners)

#state_copy = State(colour_copy,o_p_copy,e_p_copy,corners_copy,board_copy,0)



'''
*** Not sure what this does...
'''
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

#rand_place = Player.random_place(self)
#Player.complete_place(rand_place,self.curr_turn,self.our_pieces,self.enemy_pieces,self.corners,self.gameboard)




'''
Used for testing to see the current state of our gameboard in a formatted way.
'''
def print_gameboard(board):
    for row in board:
        print(row)

