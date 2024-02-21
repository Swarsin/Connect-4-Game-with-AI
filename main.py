import pygame, sys

pygame.init()

SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 - 10)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h))
font = pygame.font.SysFont("arial", 75)

class Stack:
    def __init__(self):
        self.items = []
        self.pointer = 0

    def IsEmpty(self):
        return self.pointer == 0
    
    def Push(self, item):
        if len(self.items) <= self.pointer:
            self.items += [0] * (self.pointer - len(self.items) + 1)
        self.items[self.pointer] = item
        self.pointer += 1

    def Pop(self): #change this so it uses pointers - wouldn't get marks as it is right now
        # if not self.IsEmpty():
        #     return self.items.pop(item)
        if self.pointer < 0:
            return None  # or raise an exception for an empty stack
        else:
            self.pointer -= 1  # decrement pointer after popping an item
            self.items[self.pointer] = 0
            
        
    def Peek(self):
        if not self.IsEmpty():
            return self.items[-1]
    
    def Fetch(self, index): #to get item at specific index of the stack object
        if 0 <= index < len(self.items):        
            return self.items[index]
        else:
            return 0
        
    def FetchAll(self): #returns copy of entire stack object - doesn't affect original
        return self.items.copy
        
    def GetSize(self):
        return len(self.items)
    
    def __str__(self): #for testing/debugging
        return str(self.items)
    
    def __repr__(self): #for testing/debugging
        return str(self.items)

class Board:
    def __init__(self):
        self.rows = 6
        self.columns = 7
        self.board = [Stack() for column in range(self.columns)] #uses composition - creating more complex objects (board) by combining simpler ones(stack) - also if the board class is scrapped, the stacks would be destroyed too as the form an integral part of the board. 
        self.full_columns = []
    
    def GetRows(self):
        return self.rows
    
    def GetColumns(self):
        return self.columns

    def DropPiece(self, column, player_piece):
        self.board[column].Push(player_piece)

    def IsValidMove(self, column):
        if not  0 <= column <= 6:
            return False
        if self.board[column].GetSize() == 6:
            return False
        return True
    
    def CheckForWin(self, player_piece):
        #Check for horizontal win
        for column in range(self.columns-3): #(column_count - 3) since the last 3 columns can't contain 4 pieces in a row horizontally
            for row in range(self.rows):
                if self.board[column].Fetch(row) == player_piece and self.board[column + 1].Fetch(row) == player_piece and self.board[column + 2].Fetch(row) == player_piece and self.board[column + 3].Fetch(row) == player_piece:
                    return True
        #Check for vertical win        
        for column in range(self.columns):
            for row in range(self.rows-3): #(row_count - 3) since the top 3 rows can't contain 4 pieces in a row vertically
                if self.board[column].Fetch(row) == player_piece and self.board[column].Fetch(row + 1) == player_piece and self.board[column].Fetch(row + 2) == player_piece and self.board[column].Fetch(row + 3) == player_piece:
                    return True
        #Check for win where diagonal going up
        for column in range(self.columns-3): #can't have a diagonal going up beyond the middle (4th) column so subtract 3
            for row in range(self.rows-3): #can't have a diagonal going up beyond the 3rd row so subtract 3
                if self.board[column].Fetch(row) == player_piece and self.board[column + 1].Fetch(row + 1) == player_piece and self.board[column + 2].Fetch(row + 2) == player_piece and self.board[column + 3].Fetch(row + 3) == player_piece:
                    return True
        #Check for win where diagonal going down
        for column in range(self.columns-3): #can't have a diagonal going down beyond the 4th row
            for row in range(3, self.columns): #cant have a diagonal going down before the 4th column
                if self.board[column].Fetch(row) == player_piece and self.board[column + 1].Fetch(row - 1) == player_piece and self.board[column + 2].Fetch(row - 2) == player_piece and self.board[column + 3].Fetch(row - 3) == player_piece:
                    return True
        return False
    
    def CheckForDraw(self):
        for column in range(self.columns):
            if self.board[column].GetSize() == 6:
                if column not in self.full_columns:
                    self.full_columns.append(column)
        if len(self.full_columns) == 7:
            return True
        return False
        

    def PrintBoard(self): #displays on terminal - for original testing before GUI
        for row in range(self.rows - 1, -1, -1): #is self.rows - 1 because the row indices is 0 to 5 and this for loops runs from 0 to 5 (matches the row indices of the board)
            for column in range(self.columns):
                print(self.board[column].Fetch(row), end = " ")
            print("")
        print("")

    def DisplayBoard(self, player1, player2):
        rect = pygame.Rect(0, 0, 100, 100)
        for column in range(self.columns):
            for row in range(self.rows):
                rect.center = ((info.current_w//2) - 300 + column*(SQUARE_SIZE), (info.current_h/2) - 250 + row*(SQUARE_SIZE))
                pygame.draw.rect(screen, BLUE, rect)
                pygame.draw.circle(screen, BLACK, ((info.current_w//2) - 300 + column*(SQUARE_SIZE), (info.current_h/2) - 250 + row*(SQUARE_SIZE)), RADIUS)
        for column in range(self.columns):
            for row in range(self.rows):        
                if self.board[column].Fetch(row) == 1:
                    pygame.draw.circle(screen, player1.GetColour(), ((info.current_w//2) - 300 + column*(SQUARE_SIZE), (info.current_h - ((info.current_h/2) - 250 + row*(SQUARE_SIZE)))), RADIUS) #I don't understand why +280 here, maybe the board isn't actually centred?
                elif self.board[column].Fetch(row) == 2:
                    pygame.draw.circle(screen, player2.GetColour(), ((info.current_w//2) - 300 + column*(SQUARE_SIZE), (info.current_h - ((info.current_h/2) - 250 + row*(SQUARE_SIZE)))), RADIUS) #I don't understand why +280 here, maybe the board isn't actually centred?
        pygame.display.update()

    def Store(self, move):
        self.moves_history.append(move)
        
    def Undo(self):
        for i in range(2):
            last_move = self.moves_history.pop(-1)
            self.board[last_move].Pop()

class Player:
    def __init__(self, username, piece, turn, colour):
        self.username = username
        self.piece = piece
        self.turn = turn
        self.colour = colour
    
    def GetUsername(self):
        return self.username
    
    def GetPiece(self):
        return self.piece
    
    def GetTurn(self):
        return self.turn
    
    def SetTurn(self, new):
        self.turn = new

    def GetColour(self):
        return self.colour
    
    # def DropPiece(self, choice): #useless method
    #     #choice = int(input(f"{self.username}, enter the column that you want to drop your piece into>>> ")) (for CLI version of the game)
    #     # while not board1.IsValidMove(choice):
    #     #         print("Invalid")
    #     #     if board1.IsValidMove(choice):
    #     #         board1.DropPiece(choice, self.piece)
    #     board1.DropPiece(choice, self.piece)
            

# class Game: # could code later, but right now I probably don't need this
#     def __init__():


# board_obj = Board()
# player_one = Player("One", 1, True, RED)
# player_two = Player("Two", 2, False, YELLOW)

# turn = 0
#board1.PrintBoard()
    
# board_obj.DisplayBoard(player_one, player_two)
# pygame.display.update()

def Main_2p(player1, player2, board1):
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, info.current_w, ((info.current_h-600)/2)))
                x_pos = event.pos[0]
                if player1.GetTurn():
                    pygame.draw.circle(screen, player1.GetColour(), (x_pos, (((info.current_h-600)/2)-RADIUS)), RADIUS)
                else:
                    pygame.draw.circle(screen, player2.GetColour(), (x_pos, (((info.current_h-600)/2)-RADIUS)), RADIUS)
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = event.pos[0]
                current_column = (x_pos - ((info.current_w - 700)//2)) // SQUARE_SIZE #floor division to get whole number value of column, -600 to offset the 600 pixels i added to centre the board 
                if not board1.IsValidMove(current_column): #doesn't allow user to drop piece outside the board
                    continue
                if player1.GetTurn():
                    board1.DropPiece(current_column, player1.GetPiece())
                    if board1.CheckForWin(player1.GetPiece()):
                        text = font.render(f"{player1.GetUsername()} wins!", 1, player1.GetColour())
                        text_rect = text.get_rect(center=(info.current_w/2, 76//2))
                        screen.blit(text, text_rect)
                        game_over = True
                    elif board1.CheckForDraw():
                        text = font.render("DRAW!", 1, (255, 255, 255))
                        text_rect = text.get_rect(center=(info.current_w/2, 76//2))
                        screen.blit(text, text_rect)
                        game_over = True
                    player1.SetTurn(False)
                    player2.SetTurn(True)
                else:
                    board1.DropPiece(current_column, player2.GetPiece())
                    if board1.CheckForWin(player2.GetPiece()):
                        text = font.render(f"{player2.GetUsername()} wins!", 1, player2.GetColour())
                        text_rect = text.get_rect(center=(info.current_w/2, 75//2))
                        screen.blit(text, text_rect)
                        game_over = True
                    elif board1.CheckForDraw():
                        text = font.render("DRAW!", 1, (255, 255, 255))
                        text_rect = text.get_rect(center=(info.current_w/2, 75//2))
                        screen.blit(text, text_rect)
                        game_over = True
                    player2.SetTurn(False)
                    player1.SetTurn(True)    
                board1.PrintBoard()
                board1.DisplayBoard(player1, player2)
                if game_over:
                    pygame.time.wait(3000)
# Main_2p(player_one, player_two, board_obj)
