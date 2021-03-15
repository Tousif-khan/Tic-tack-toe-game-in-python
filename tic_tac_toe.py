#-------------Global variables-------------
#game board
board = ["-","-","-",
         "-","-","-",
         "-","-","-" ]
#if game is still going op
game_is_still_going = True

#who won or tie?
winner = None

#whose turn is it
current_player = "X"

def display_board():
  print(board[0]+" | "+board[1]+" | "+board[2])
  print(board[3]+" | "+board[4]+" | "+board[5])
  print(board[6]+" | "+board[7]+" | "+board[8])

#play tic tac toe
def play_game():

  #iniital game board
  display_board()

  #while the game is still going
  while game_is_still_going:
    #handle a single turn for of an arbitrary player
    handle_turn(current_player)

    #check if game is ended
    check_if_game_over()

    #flip to neext player
    flip_player()
  #the game is ended
  if winner == "X" or winner == "O":
    print(winner +" won")
  elif winner == None:
    print("Tie")

def handle_turn(player): 
  print(player+"'s turn")
  position = int(input("Choose a number between 1-9: "))-1
  #check for validity of input
  valid = False
  while not valid:
    while position not in [0,1,2,3,4,5,6,7,8] :
        position = int(input("Invalid input. Choose a number between 1-9: "))-1
    if board[position] == "-":
      valid = True
    else: 
      print("Already taken. Go to another place")
      position = int(input("Choose a number between 1-9: "))-1
  
  board[position] = player
  display_board()

def check_if_game_over():
  check_for_winner()
  check_if_tie()

def check_for_winner():
  #set for global variable
  global winner
  #check_row
  row_winner = check_row()

  #check_column
  column_winner = check_column()

  #check_diagonal
  diagonal_winner = check_diagonal()

  #get the winner
  if row_winner:
    print("row win")
    winner = row_winner
  elif column_winner:
    print("column win")
    winner = column_winner
  elif diagonal_winner:
    print("diagonal win")
    winner = diagonal_winner
  else:
    winner = None
  return

def check_row():
  #set up global variable
  global game_is_still_going
  #check if any row have same value but not empty
  row_1 = board[0] == board[1] == board[2] !="-"
  row_2 = board[3] == board[4] == board[5] !="-"
  row_3 = board[6] == board[7] == board[8] !="-"
  #if any row does have a match, flag that there is a win
  if row_1 or row_2 or row_3:
    game_is_still_going = False
  #return the winner (X or O)
  if row_1:
    return board[0]
  elif row_2:
    return board[3]
  elif row_3:
    return board[6]
  return

def check_column():
  #set up global variable
  global game_is_still_going
  #check if any row have same value but not empty
  col_1 = board[0] == board[3] == board[6] !="-"
  col_2 = board[1] == board[4] == board[7] !="-"
  col_3 = board[2] == board[5] == board[8] !="-"
  #if any row does have a match, flag that there is a win
  if col_1 or col_2 or col_3:
    game_is_still_going = False
  #return the winner (X or O)
  if col_1:
    return board[0]
  elif col_2:
    return board[1]
  elif col_3:
    return board[2]
  return

def check_diagonal():
  #set up global variable
  global game_is_still_going
  #check if any row have same value but not empty
  diagonal_1 = board[0] == board[4] == board[8] !="-"
  diagonal_2 = board[2] == board[4] == board[6] !="-"
  #if any row does have a match, flag that there is a win
  if diagonal_1 or diagonal_2:
    game_is_still_going = False
  #return the winner (X or O)
  if diagonal_1:
    return board[0]
  elif diagonal_2:
    return board[2]
  return

def check_if_tie():
  global game_is_still_going
  if "-" not in board:
     game_is_still_going = False
  return

def flip_player():
  global current_player
  if current_player == "X":
    current_player = "O"
  elif current_player  == "O":
    current_player = "X"
  return

play_game()

