
import random


class Player:
  def __init__(self):
    self.piece_label
    self.pieces=[[0,0]*9]
    self.selected_piece=[]
    self.moved_piece=[]
  # def select_piece(self,x):
  #   # print(self.pieces[x])
    
  def getPositionInput(self):
    flag = False
    while not flag:
      position = input("enter the position ( x and y separated by a comma):").split(',')
      if len(position)==2 and position[0] and position[1]:
        x,y = int(position[0]), int(position[1])
        flag =True
    print("x,y : ",[x,y])
    return [x,y]
  #   pass
  
  def askUserToSelectPiece(self):
    x,y = -1,-1
    while [x,y] not in self.pieces:
      x,y = self.getPositionInput()
      print("in askUserToSelectPiece() x,y : ",[x,y])
      print("self pieces ",self.pieces)
    print([x,y],"is selected successfully")
    self.selected_piece = [x,y]
  
  def askUserMovingPosition(self,reachable_places):
    x,y = -1,-1
    while [x,y] not in reachable_places:
      x,y = self.getPositionInput()
      print("in askUserMovingPosition() x,y : ",[x,y])
      print("reachable_places ",reachable_places)
    print("The selected piece is moved to ",[x,y]," successfully")
    pass

  def delete_piece(self,x):
    self.pieces.pop(x)
    pass
    
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

  def remove_piece(self,removed_pieces):
    pieces = self.pieces
    for removed_piece in removed_pieces:
      pieces.remove(removed_piece) if removed_piece in pieces else print("fail to remove",removed_piece)
    
  
class Computer(Player):
  def __init__(self):
    self.pieces = [[0,i] for i in range(9)]
    self.piece_label = "X"

class Human(Player):
  def __init__(self):
    self.pieces = [[8,i] for i in range(9)]
    self.piece_label = "Y"
  pass

class Board:
  def __init__(self,computer,human):
    self.computer = computer
    self.human = human
    self.data = [[" " for i in range(9)] for j in range(9)]
    self.reachable_places = []
    
  
  def select_piece(self,player,x,y):
    if [x,y] not in player.pieces:
      print("wrong place")
      return False
    player.selected_piece = [x,y]
    self.calc_reachable_places(x,y)
    self.calc()
  
  def move_selected_piece(self,player,x,y):
    if player.selected_piece == []:
      print("nothing is selected")
      return False
    if [x,y] not in self.reachable_places:
      print("you cannot move to there")
      return False
    player.move_piece(x,y)
    self.reachable_places = []
    self.calc()
    
    
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
    defense.remove_piece(removed_pieces)


  # layout the all elements on the board
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
    
    # print(data)
  
  # draw the board with elements
  def show(self):
    self.calc()
    for i in range(9):
      for j in range(9):
        print(self.data[i][j], end="")
        print("|", end="")
      print("")
  


class Match():
  def __init__(self,board):
    self.board = board
    self.isHumansTurn = False
    self.isEnd = False
  def start_match():
    # while !isEnd:
      
    #   pass
    player
    self.isHumansTurn = bool(random.getrandbits(1))
    if self.isHumansTurn:
      print("You start first")
      player = board.human
    else:
      print("Computer starts first")
      player = board.computer
    x,y = player.getPositionInput()
    board.select_piece(player,2,3)
    board.move_selected_piece(player,2,3)
    print("")


    
  
  

computer = Computer()
human = Human()
board = Board(computer,human)
# board.data[4][7] = "L"
# board.show()
# board.human.delete_piece(4)

# print(board.human.pieces)
# board.calc_reachable_places(4,4)

board.select_piece(computer,0,6)
board.move_selected_piece(computer,6,6)

board.select_piece(computer,0,7)
board.move_selected_piece(computer,6,7)


board.select_piece(human,8,5)
# board.show()

board.move_selected_piece(human,6,5)
# print("before",computer.pieces)
board.show()

board.select_piece(human,8,8)
board.move_selected_piece(human,6,8)
board.check_captured_pieces(human,computer)

board.human.askUserToSelectPiece()
board.show()
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

