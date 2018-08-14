import itertools
import random


class Player(object):
  """A Player which has Human and Computer subclasses
    
      Attributes
        piece_label: A label of each player's pieces shown on the board
        selected_piece: The selected piece by a player
        moved_piece: The piece which is moved by a player after selected
        lost_pieces_count: The number of the pieces a playser has lost
  """
  def __init__(self):
    self.piece_label
    self.pieces = [[0,0]*9]
    self.selected_piece = []
    self.moved_piece = []
    self.lost_pieces_count = 0
  

  
class Computer(Player):
  def __init__(self):
    self.pieces = [[0,i] for i in range(9)]
    self.piece_label = "X"
    super().__init__()

class Human(Player):
  def __init__(self):
    self.pieces = [[8,i] for i in range(9)]
    self.piece_label = "Y"
    super().__init__()

class Board:
  """
  A board represents the locations of pieces
    
  Attributes
      computer: The opponent of the user
      human: The user
      reachable_places: The reachable places on the board if a player pick an own piece.
      data: 9x9 array which shows where are the pieces on the board
  """
  def __init__(self,computer,human):

    self.computer = computer
    self.human = human
    self.reachable_places = []   
    data = []

    for i, j in itertools.product(range(9),range(9)):
      if j == 0:
        data.append([])
      if i == 0:
        data[i].append(computer.piece_label)
      elif i == 8:
        data[i].append(human.piece_label)
      else:
        data[i].append(" ")
    
    self.data = data
    

    
  def ask_user_select_point(self,symbol):
    # Prompt user to input x,y point
    x,y = -1,-1

    # When a user has finished input, input_flag is going to be True        
    input_flag = False
    while not input_flag:
      position = input("enter the position ( x and y separated by a comma):").split(',')
      if len(position)==2 and position[0] and position[1]:
        x,y = int(position[0]), int(position[1])
        print("You've typed...[x,y] : ",[x,y])
        if self.data[x][y] == symbol:
          input_flag = True  
    return [x,y]
      
  def ask_computer_select_point(self,symbol):
    # Computer pick a point from the available points randomly
    computer_pieces = []
    for i in range(9):
      for j in range(9):
        if self.data[i][j] == symbol:
          computer_pieces.append([i,j])

    [x,y] = random.choice(computer_pieces)
    print("Computer has chosen...[x,y] : ",[x,y])
    return [x,y]


        

  def select_piece(self,player,*point):
    # "player" selects a piece to move
    # if you have "point"(x,y) parameters, user doesn't prompt to input 
    if len(point) == 2 and point[0] and point[1]:
      [x,y] = point
    else:      
      if type(player) == Human:
        [x,y] = self.ask_user_select_point(player.piece_label)
      else:
        [x,y] = self.ask_computer_select_point(player.piece_label)

    
    if self.data[x][y] != player.piece_label:
      print("wrong place")
      return False
    player.selected_piece = [x,y]
    self.calc_reachable_places(x,y)
    
  
  def move_selected_piece(self,player,*point):
    # "player" select a point where they move the peice being selected already.
    # If you have "point"(x,y) parameters, the user doesn't prompt to input
    if len(point) == 2 and point[0] and point[1]:
        [x,y] = point
    else:      
      if type(player) == Human:
        [x,y] = self.ask_user_select_point("+")
      else:
        [x,y] = self.ask_computer_select_point("+")
    

    data = self.data
    
    if player.selected_piece == []:
      print("nothing is selected")
      return False
    if [x,y] not in self.reachable_places:
      print("you cannot move to there")
      return False

    # Clear all "+" in the reachable places
    for r in self.reachable_places:
      [rx,ry] = r
      data[rx][ry] = " "

    # Clear the previous position of the selected peice
    [prev_x,prev_y] = player.selected_piece
    data[prev_x][prev_y] = " "

    # Move the selected piece
    data[x][y] = player.piece_label
    player.moved_piece = [x,y]
    
    # Reset reaachable_places
    self.reachable_places = []
    
    
    
  
  def calc_reachable_places(self,x,y):
  #Calculate the rechable places where a given piece can move
  
    reachable = self.reachable_places
    #vertical directions
    for i in range(x,9):
      if [i,y] == [x,y] :
        continue
      elif self.data[i][y] == " ":
        reachable.append([i,y])
      else:
        break   

    for i in range(x,-1,-1):
      if[i,y] == [x,y] :
        continue
      elif self.data[i][y] == " ":
        reachable.append([i,y])
      else:
        break

    #horizontal directions
    for i in range(y,9):
      if [x,i] == [x,y]:
        continue
      elif self.data[x][i] == " ":
        reachable.append([x,i])
      else:
        break

    for i in range(y,-1,-1):
      if [x,i] == [x,y]:
        continue
      elif self.data[x][i] == " ":
        reachable.append([x,i])
      else:
        break

    for p in reachable:
      [x,y] = p
      self.data[x][y] = "+"
  
  
  def check_captured_pieces(self, offense,defense):
  # After moving a piece, remove the sandwitched opponent's pieces by the moved piece.  
    removed_pieces = []
    tmp = []
    moved_piece = offense.moved_piece
    capture_flag = False
    [x,y] = moved_piece
    # search to downside
    for i in range(x,9):
      if [i,y] == [x,y] :
        continue
      elif self.data[i][y] == defense.piece_label:
        tmp.append([i,y])
      elif self.data[i][y] == offense.piece_label:
        capture_flag = True
        break
      else:
        break
    
    if capture_flag:
      removed_pieces.extend(tmp)
    capture_flag = False
    tmp = []
    # search to upside
    for i in range(x,-1,-1):
      if[i,y] == [x,y] :
        continue
      elif self.data[i][y] == defense.piece_label:
        tmp.append([i,y])
      elif self.data[i][y] == offense.piece_label:
        capture_flag = True
        break
      else:
        break
    if capture_flag:
      removed_pieces.extend(tmp)
    capture_flag = False
    tmp = []
    
    #search to rightside
    for i in range(y,9):
      if [x,i] == [x,y]:
        continue
      elif self.data[x][i] == defense.piece_label:
        tmp.append([x,i])
      elif self.data[x][i] == offense.piece_label:
        capture_flag = True
      else:
        break
    if capture_flag:
      removed_pieces.extend(tmp)
    capture_flag = False
    tmp = []

    #search to lefttside
    for i in range(y,-1,-1):
      if [x,i] == [x,y]:
        continue
      elif self.data[x][i] == defense.piece_label:
        tmp.append([x,i])
      elif self.data[x][i] == offense.piece_label:
        capture_flag = True
      else:
        break
    if capture_flag:
      removed_pieces.extend(tmp)
    capture_flag = False
    tmp = []
    
    # fill " " in the cells where the pieces has been removed
    defense.lost_pieces_count += len(removed_pieces)
    for p in removed_pieces:
      [x,y] = p
      self.data[x][y] = " "
    
    # Reset the moving destination
    offense.moved_piece = []




  
  def show(self):
  # Draw the board with the elements  
    
    for i in range(9):
      print("  |0|1|2|3|4|5|6|7|8|") if i == 0 else 0
      print(i,"|", end = "")
      for j in range(9):
        print(self.data[i][j], end = "")
        print("|", end = "")
      print("")
  


class Match():
  """
  A match of Rook

  Attributes
        board: A array representing the Rook board
        is_humans_turn: A boolean tracking if it is the users turn
        is_end: A boolean tracking if the game is over
        winner: A string for the name of the winner
  """
  def __init__(self,board):
    self.board = board
    self.is_humans_turn = False
    self.is_end = False
    self.winner = ""

  def start_match(self):
    #Start a match    
    self.is_humans_turn = bool(random.getrandbits(1))

    # Decide the first offense randomly
    if self.is_humans_turn:
      print("You start first")
      offense = board.human
      defense = board.computer
    else:
      print("Computer starts first")
      offense = board.computer
      defense = board.human
    
    # Loop until deciding the winner
    while not self.is_end:
      print("Select a moving piece")
      board.show()
      board.select_piece(offense)
      print("Choose a destination")
      board.show()
      board.move_selected_piece(offense)
      board.check_captured_pieces(offense,defense)
      board.show()

      # Judge the game
      # if defense.lost_pieces_count >= 5 or defense.lost_pieces_count - offense.lost_pieces_count >= 3:
      if defense.lost_pieces_count >= 2:
        self.is_end = True
        self.winner = offense
        break

      #Change the turn
      if type(offense) == Human:
        offense, defense = computer, human
      else:
        offense, defense = human, computer
    

    # Show the match result
    if type(self.winner) == Human:
      print("You won!!")
    else:
      print("You lost")
    

computer = Computer()
human = Human()
board = Board(computer,human)
match = Match(board)
match.start_match()
