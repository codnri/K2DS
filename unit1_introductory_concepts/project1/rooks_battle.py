
import random


class Player(object):
  def __init__(self):
    self.piece_label
    self.pieces=[[0,0]*9]
    self.selected_piece=[]
    self.moved_piece=[]
    self.lost_pieces_count = 0
  
    
  def move_piece(self,x,y):
    selected = [ piece for piece in self.pieces if piece == self.selected_piece ][0]
    print("selected:",selected)
    # selected = [x,y]
    selected[0] = x
    selected[1] = y
    print("self.pieces",self.pieces)
    self.selected_piece = []
    self.moved_piece = [x,y]
    pass
  pass

  # def remove_piece(self,removed_pieces):
  #   pieces = self.pieces
  #   for removed_piece in removed_pieces:
  #     pieces.remove(removed_piece) if removed_piece in pieces else print("fail to remove",removed_piece)
    
  
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
  def __init__(self,computer,human):
    self.computer = computer
    self.human = human
    self.reachable_places = []   
    data= []
    for i in range(9):
      data.append([])
      for j in range(9):
        # data[i].append(" ")
        if i == 0:
          data[i].append(computer.piece_label)
        elif i == 8:
          data[i].append(human.piece_label)
        else:
          data[i].append(" ")
    self.data = data
    
    # for i in range(9):
    #   for j in range(9):
    #     if i == 0:
    #       self.data[i][j] = computer.piece_label
    #     elif i == 8:
    #       self.data[i][j] = human.piece_label
    #     else:
    #       self.data[i][j] = " "
    
  def ask_user_select_point(self,symbol):
    x,y = -1,-1
    
      # x,y = self.getPositionInput()
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
    computer_pieces = []
    for i in range(9):
      for j in range(9):
        if self.data[i][j] == symbol:
          computer_pieces.append([i,j])
    # print("computer_pieces:",computer_pieces)
    [x,y] = random.choice(computer_pieces)
    print("Computer has chosen...[x,y] : ",[x,y])
    return [x,y]


        

  def select_piece(self,player,*point):
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
    # self.calc()
  
  def move_selected_piece(self,player,*point):
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

    # clear all "+" in the reachable places
    for r in self.reachable_places:
      [rx,ry] = r
      data[rx][ry] = " "

    # clear the previous position of the selected peice
    [prev_x,prev_y] = player.selected_piece
    data[prev_x][prev_y] = " "

    # move the selected piece
    # player.move_piece(x,y)
    data[x][y] = player.piece_label
    print("selected_piece",player.selected_piece)
    player.moved_piece = [x,y]
    
    # reset reaachable_places
    self.reachable_places = []
    
    # self.calc()
    
    
  #Calculate the rechable places where a given piece can move
  def calc_reachable_places(self,x,y):
    reachable = self.reachable_places
    #vertical directions
    for i in range(x,9):
      if [i,y] == [x,y] :
        continue
      elif self.data[i][y]==" ":
        reachable.append([i,y])
      else:
        break   

    for i in range(x,-1,-1):
      if[i,y] == [x,y] :
        continue
      elif self.data[i][y]==" ":
        reachable.append([i,y])
      else:
        break

    #horizontal directions
    for i in range(y,9):
      if [x,i] == [x,y]:
        continue
      elif self.data[x][i]==" ":
        reachable.append([x,i])
      else:
        break

    for i in range(y,-1,-1):
      if [x,i] == [x,y]:
        continue
      elif self.data[x][i]==" ":
        reachable.append([x,i])
      else:
        break
    print(reachable)
    for p in reachable:
      [x,y] = p
      self.data[x][y] = "+"
  
  # after moving a piece, remove the sandwitched opponent's pieces by the moved piece.
  def check_captured_pieces(self, offense,defense):
    
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
      elif self.data[x][i]==defense.piece_label:
        tmp.append([x,i])
      elif self.data[x][i]==offense.piece_label:
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
      elif self.data[x][i]==defense.piece_label:
        tmp.append([x,i])
      elif self.data[x][i]==offense.piece_label:
        capture_flag = True
      else:
        break
    if capture_flag:
      removed_pieces.extend(tmp)
    capture_flag = False
    tmp = []
    print("removed_pieces",removed_pieces) 
    # defense.remove_piece(removed_pieces)
    defense.lost_pieces_count += len(removed_pieces)
    for p in removed_pieces:
      [x,y] = p
      self.data[x][y] = " "
    
    # reset the moving destination
    offense.moved_piece = []


  # layout the all elements on the board
  """
  def calc(self):
    data = self.data
    computer = self.computer
    human = self.human
    # print(computer.pieces)
    for i in range(9):
      for j in range(9):
        if [i,j] in computer.pieces:
          data[i][j]="X"
        elif [i,j] in human.pieces:
          data[i][j]="Y"
        elif [i,j] in self.reachable_places:
          data[i][j]="+"
        else:
          data[i][j]=" "
  """  
    # print(data)
  
  # draw the board with elements
  def show(self):
    # self.calc()
    
    for i in range(9):
      print("  |0|1|2|3|4|5|6|7|8|") if i == 0 else 0
      print(i,"|", end="")
      for j in range(9):
        print(self.data[i][j], end="")
        print("|", end="")
      print("")
  


class Match():
  def __init__(self,board):
    self.board = board
    self.is_humans_turn = False
    self.is_end = False
    self.winner = ""
  def start_match(self):
    # while !isEnd:
      
    #   pass
    
    self.is_humans_turn = bool(random.getrandbits(1))
    if self.is_humans_turn:
      print("You start first")
      offense = board.human
      defense = board.computer
    else:
      print("Computer starts first")
      offense = board.computer
      defense = board.human
    
    while not self.is_end:
      print("Select a moving piece")
      board.show()
      board.select_piece(offense)
      print("Choose a destination")
      board.show()
      board.move_selected_piece(offense)
      board.check_captured_pieces(offense,defense)
      board.show()

      # judge the game
      # if defense.lost_pieces_count >= 5 or defense.lost_pieces_count - offense.lost_pieces_count >= 3:
      if defense.lost_pieces_count >= 2:
        self.is_end = True
        self.winner = offense
        break
      #change the turn
      if type(offense) == Human:
        offense, defense= computer, human
      else:
        offense, defense= human, computer
    


    if type(self.winner) == Human:
      print("You won!!")
    else:
      print("You lost")
    


    
  
  

computer = Computer()
human = Human()
board = Board(computer,human)
match = Match(board)
match.start_match()
# board.data[4][7] = "L"
# board.show()
# board.human.delete_piece(4)

# board.select_piece(human,8,6)
# board.show()
# print("-----",human.selected_piece)
# board.move_selected_piece(human,6,6)
# board.show()

# print(board.human.pieces)
# board.calc_reachable_places(4,4)

# board.select_piece(computer,0,6)
# board.move_selected_piece(computer,6,6)

# board.select_piece(computer,0,7)
# board.move_selected_piece(computer,6,7)


# board.select_piece(human,8,5)
# # board.show()

# board.move_selected_piece(human,6,5)
# # print("before",computer.pieces)
# board.show()

# board.select_piece(human,8,8)
# board.move_selected_piece(human,6,8)
# board.check_captured_pieces(human,computer)

# board.human.askUserToSelectPiece()
# board.human.askUserMovingPosition()
# board.show()
# print("after",computer.pieces)
# board.calc_reachable_places(8,2)
# print(board.data)


# print(human.pieces)
# for i in range(0,5):
#   print(i)

# arr = [[8, 0], [8, 1], [8, 2], [8, 4], [8, 5], [8, 6], [8, 7], [8, 8]]
# for [i,j] in arr:
#   print("i: ",i," j:",j)

# print([1,2] == [1,2] and 1 == 12 )

# arr = [[8, 0], [8, 1], [8, 2], [8, 4], [8, 5], [8, 6], [8, 7], [8, 8]]
# [x,y] = [8,8]
# arr.remove([x,y]) if [x,y] in arr else 0
# print(arr)

# a = None
# if a:
#   print ("empty")
# else:
#   print("else")

#input component
"""
flag = False
while not flag:
  position = input("enter the position ( x and y separated by a comma):").split(',')
  if len(position)==2 and position[0] and position[1]:
    x,y = position[0], position[1]
    flag =True
print("x,y : ",[x,y])
"""

# arr = [[1,2,3],[4,5,6],[7,8,9]]
# # arr[1][2] = "★"
# for i in range(3):
#   arr[0][i] = "*"
# print(arr)

# arr #= [[" "] * 3] * 3

# for i in range(3):
#   arr[0][i] = "P"
#   print(arr[0][i])
#   # self.data[8][i] = human.piece_label
# # print(arr[0])
# print(arr)
