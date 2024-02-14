import pygame, sys, random, copy, math
#Libraries used:
#Pygame - GUI for the game, displays board and allows the user to drop pieces onto the board
#sys - sys.exit() upon user quitting window
#random - to randomly choose who gets first turn
#copy - to create a deepcopy of the game board class - used to evaluate simulated game states and decide best move in Minimax algorithm
#math - math.inf for best and -math.inf for worst possibe move in minimax

#Band A:
#Recursive Merge sort - has recursion and merge sort (implemented in leaderboard)
#Optimisation for Minimax algorithm - aplha beta pruning which stops exploring for further moves if a bad enough score is found for a move
#Stack and Stack operations - each column in the game board is a stack, and pieces are pushed onto the stack/column
#Complex user-define use of OOP model e.g. classes, inheritance, composition, polymorphism, interfaces
#To Do:
#Hashing in login screen
#Possible Aggregate SQL Functions to display (in leaderboard screen) total games played, average wins, other details 
#If really needed could implement MCTS as another AI Player algorithm

pygame.init()

SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 - 10)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
font = pygame.font.SysFont("arial", 75)
clock = pygame.time.Clock()
PLAYER_TURN = 0
AI_TURN = 1

EMPTY = 0

class Stack:
    def __init__(self):
        self.items = []
        self.pointer = 0

    def IsEmpty(self):
        return self.pointer == 0
    
    def Push(self, item):
        if len(self.items) <= self.pointer:
            self.items += [None] * (self.pointer - len(self.items) + 1)
        self.items[self.pointer] = item
        self.pointer += 1

    def Pop(self, item): #change this so it uses pointers - wouldn't get marks as it is right now
        if not self.IsEmpty():
            return self.items.pop(item)
        
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
        self.window_length = 4
    
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
    
    def GetValidMoves(self):
        valid_moves = [column for column in range(self.columns) if self.IsValidMove(column)]
        return valid_moves
    
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
    
    def EvaluateWindow(self, window, player_piece):
        score = 0 
        opponent_piece = 1 #PLAYER_PIECE
        #evaluating player move:
        if player_piece == 1:
            opponent_piece = 2 #AI_PIECE
        if window.count(player_piece) == 4:
            score += 100   
        elif window.count(player_piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(player_piece) == 2 and window.count(EMPTY) == 2:
            score += 2
        return score
        
    def ScorePosition(self, player_piece):
        score = 0

        #score centre column
        centre_array = [self.board[self.columns//2].Fetch(row) for row in range(self.rows)]
        centre_count = centre_array.count(player_piece)
        score += centre_count * 3

        #score horizontally
        for row in range(self.rows):
            row_array = [self.board[column].Fetch(row) for column in range(self.columns)] #creatint an array of the entire row
            for column in range(4):#(self.column - 3):
                window = row_array[column:column + self.window_length]
                score += self.EvaluateWindow(window, player_piece)

        #score vertically
        for column in range(self.columns):
            column_array = [self.board[column].Fetch(row) for row in range(self.rows)]
            for row in range(self.rows - 3):
                window = column_array[row:row + self.window_length]
                score += self.EvaluateWindow(window, player_piece)

        #score in a positively sloped diagonal
        for row in range(self.rows - 3):
            for column in range(self.columns - 3):
                window = [self.board[column + i].Fetch(row + i) for i in range(self.window_length)]
                score += self.EvaluateWindow(window, player_piece)

        #score in a negatively sloped diagonal
        for row in range(self.rows - 3):
            for column in range(self.columns - 3):
                window = [self.board[column + 3 - i].Fetch(row + i) for i in range(self.window_length)]
                score += self.EvaluateWindow(window, player_piece)

        return score

    def GetBestMove(self, player_piece):
        valid_moves = self.GetValidMoves()#self.board.GetValidMoves()
        highest_score = -10000
        best_move = random.choice(valid_moves)
        for move in valid_moves: #for each valid column
            temp_board = copy.deepcopy(board1)
            temp_board.DropPiece(move, player_piece)
            score = temp_board.ScorePosition(player_piece)
            if score > highest_score:
                highest_score = score
                best_move = move
        return best_move
    
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

    def DisplayBoard(self):
        rect = pygame.Rect(0, 0, 100, 100)
        for column in range(self.columns):
            for row in range(self.rows):
                rect.center = ((info.current_w//2) - 300 + column*(SQUARE_SIZE), (info.current_h/2) - 250 + row*(SQUARE_SIZE))
                pygame.draw.rect(screen, BLUE, rect)
                pygame.draw.circle(screen, BLACK, ((info.current_w//2) - 300 + column*(SQUARE_SIZE), (info.current_h/2) - 250 + row*(SQUARE_SIZE)), RADIUS)
        for column in range(self.columns):
            for row in range(self.rows):        
                if self.board[column].Fetch(row) == 1:
                    pygame.draw.circle(screen, RED, ((info.current_w//2) - 300 + column*(SQUARE_SIZE), (info.current_h - ((info.current_h/2) - 250 + row*(SQUARE_SIZE)))), RADIUS) #I don't understand why +280 here, maybe the board isn't actually centred?
                elif self.board[column].Fetch(row) == 2:
                    pygame.draw.circle(screen, YELLOW, ((info.current_w//2) - 300 + column*(SQUARE_SIZE), (info.current_h - ((info.current_h/2) - 250 + row*(SQUARE_SIZE)))), RADIUS) #I don't understand why +280 here, maybe the board isn't actually centred?
        pygame.display.update()

    def is_terminal_node(self):
        return self.CheckForWin(1) or self.CheckForWin(2) or self.CheckForDraw()
    
    def minimax(self, board, depth, alpha, beta, max_player):
        valid_moves = board.GetValidMoves()
        is_terminal = board.is_terminal_node()
        if depth == 0 or is_terminal:
            if is_terminal:
                if board.CheckForWin(2):
                    return (None, 1000000000)
                elif board.CheckForWin(1):
                    return (None, -1000000000)
                else: #game over, so no more valid moves
                    return (None, 0)
            else: #depth = zero
                return (None, board.ScorePosition(2))
        if max_player:
            value = -math.inf
            column = random.choice(valid_moves)
            for move in valid_moves: #for column in valid columns
                temp_board = copy.deepcopy(board)
                temp_board.DropPiece(move, 2)
                #new_score = max(value, minimax(temp_board, depth-1, False))
                new_score = board.minimax(temp_board, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value
            
        else: #for minimising player
            value = math.inf
            column = random.choice(valid_moves)
            for move in valid_moves:
                temp_board = copy.deepcopy(board)
                temp_board.DropPiece(move, 1)
                new_score = board.minimax(temp_board, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = move
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

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

class AIPlayer(Player): #Inherits from Player class but still need to implement into the actual game
    def __init__(self, username, piece, turn, colour):
        super().__init__(username, piece, turn, colour)
    
    def GetUsername(self):
        return "AI Player"

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

board1 = Board()
player1 = Player("One", 1, True, RED)
player2 = Player("Two", 2, False, YELLOW)

turn = random.randint(PLAYER_TURN, AI_TURN) # change depending on the user input from the customisation menu
#board1.PrintBoard()
board1.DisplayBoard()
pygame.display.update()
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, info.current_w, ((info.current_h-600)/2)))
            x_pos = event.pos[0]
            if player1.GetTurn():
                pygame.draw.circle(screen, RED, (x_pos, (((info.current_h-600)/2)-RADIUS)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (x_pos, (((info.current_h-600)/2)-RADIUS)), RADIUS)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_pos = event.pos[0]
            current_column = (x_pos - ((info.current_w - 700)//2)) // SQUARE_SIZE #floor division to get whole number value of column, -600 to offset the 600 pixels i added to centre the board 
            if not board1.IsValidMove(current_column): #doesn't allow user to drop piece outside the board
                continue
            if player1.GetTurn():
                board1.DropPiece(current_column, 1)
                if board1.CheckForWin(1):
                    text = font.render("Player One wins!", 1, RED)
                    text_rect = text.get_rect(center=(info.current_w/2, 76//2))
                    screen.blit(text, text_rect)
                    game_over = True
                elif board1.CheckForDraw():
                    text = font.render("DRAW!", 1, BLUE)
                    text_rect = text.get_rect(center=(info.current_w/2, 76//2))
                    screen.blit(text, text_rect)
                    game_over = True
                player1.SetTurn(False)
                player2.SetTurn(True)
                board1.PrintBoard()
                board1.DisplayBoard()

    if player2.GetTurn() and not game_over:
        board1.DropPiece(board1.minimax(board1, 6, -math.inf, math.inf, True)[0], 2)#board1.DropPiece(random.randint(0, 6), 2)
        if board1.CheckForWin(2):
            text = font.render("AI Player wins!", 1, YELLOW)
            text_rect = text.get_rect(center=(info.current_w/2, 75//2))
            screen.blit(text, text_rect)
            game_over = True
        elif board1.CheckForDraw():
            text = font.render("DRAW!", 1, BLUE)
            text_rect = text.get_rect(center=(info.current_w/2, 75//2))
            screen.blit(text, text_rect)
            game_over = True   
        player2.SetTurn(False)
        player1.SetTurn(True)
        board1.PrintBoard()
        board1.DisplayBoard()
    if game_over:
        pygame.time.wait(3000)
