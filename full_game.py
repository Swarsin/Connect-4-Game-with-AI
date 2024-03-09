import random, sys, copy, math, time, sqlite3, pygame, pygame_menu

pygame.init()

info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h))
font = pygame.font.SysFont("arial", 75)

played_ai = False
played_2p = False

EMPTY = 0
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 - 10)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

def merge_sort(arr, wins=lambda x: x[1]):
    if len(arr) < 2:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    merge_sort(left, wins)
    merge_sort(right, wins)

    i = 0 #index for the left array 
    j = 0 #index for the right array
    k = 0 #index for the main array
    
    while i < len(left) and j < len(right): #while there are elements in the left and right arrays
        if wins(left[i]) > wins(right[j]): #if the current element in the left array is greater than the corresponding in the right array, add it to the main array
            arr[k] = left[i]
            i += 1 
        else:
            arr[k] = right[j] #else (bigger in right array) add it to the main array
            j += 1
        k += 1

    while i < len(left): #copies remaining element from the left array into the main array
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right): #copies any remaining elements from the right array into the main array
        arr[k] = right[j]
        j += 1
        k += 1

    return arr

def GetList():
    try:
        connect = sqlite3.connect("c4db.db")
        cursor = connect.cursor()

        cursor.execute("""
                    SELECT username, wins 
                    FROM users
                    """)

        rows = cursor.fetchall()
        list = [(row[0], row[1]) for row in rows]
        return list
    except Exception as error:
        print(error)
    finally:
        connect.close()

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
        if self.pointer < 0:
            return None  # or raise an exception for an empty stack
        else:
            self.pointer -= 1  # decrement pointer after popping an item
            self.items = self.items[:self.pointer]
            
    def Peek(self):
        if not self.IsEmpty():
            return self.items[-1]
    
    def Fetch(self, index): #to get item at specific index of the stack object
        if 0 <= index < len(self.items):        
            return self.items[index]
        else:
            return 0
        
    def GetSize(self):
        return len(self.items)
    
    # def __str__(self): #for testing/debugging
    #     return str(self.items)
    
    # def __repr__(self): #for testing/debugging
    #     return str(self.items)

class Board:
    def __init__(self):
        self.rows = 6
        self.columns = 7
        self.board = [Stack() for column in range(self.columns)] #uses composition - creating more complex objects (board) by combining simpler ones(stack) - also if the board class is scrapped, the stacks would be destroyed too as the form an integral part of the board. 
        self.full_columns = []
        self.window_length = 4
        self.moves_history = []
    
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
    
    def SimulateMove(self, column, player1, player2):
        if self.IsValidMove(column):
            self.DropPiece(column, player1.GetPiece() if player1.GetTurn() else player2.GetPiece())
            if player1.GetTurn():
                player1.SetTurn(False)
                player2.SetTurn(True)
            else:
                player2.SetTurn(False)
                player1.SetTurn(True)

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
    
    def Store(self, move):
        self.moves_history.append(move)
        
    def Undo(self):
        for _ in range(2):
            last_move = self.moves_history.pop(-1)
            self.board[last_move].Pop()
            # print(f"Length: {self.board[last_move].GetSize()}")
            # print(f"Length: {self.board[last_move+1].GetSize()}")
            # print(f"is valid: {self.IsValidMove(last_move)}")
            # self.PrintBoard()

class Player:
    def __init__(self, piece, turn, colour, username):
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

class AIPlayer(Player): #Inherits from Player class 
    def __init__(self, piece, turn, colour, difficulty):
        super().__init__(piece, turn, colour, username="")
        self.difficulty = difficulty
    
    def GetUsername(self): #MAKE A BETTER EXAMPLE OF OVERRIDING
        return "AI Player"

    def GetPiece(self):
        return self.piece
    
    def GetTurn(self):
        return self.turn
    
    def SetTurn(self, new):
        self.turn = new

    def GetColour(self):
        return self.colour
    
    def GetDifficulty(self):
        return self.difficulty

class Node:
    def __init__(self, move, parent):
        self.move = move #what move this node represents
        self.parent = parent #parents of this node
        self.wins = 0 #total games won after this move
        self.total_games = 0 #total games played using this move
        self.children = [] #children of this node

    def SetChildren(self, children):
        self.children = children

    def GetUCTValue(self):
        explore = math.sqrt(2)
        if self.total_games == 0:
            if explore == 0:
                return 0
            else:
                return math.inf
        else:
            expolitation_term =  self.wins / self.total_games
            exploration_term = explore * math.sqrt(math.log(self.parent.total_games) / self.total_games)
            uct = expolitation_term + exploration_term
            return uct

class MCTS:
    def __init__(self, current_board, player1, player2):
        self.root_state = copy.deepcopy(current_board)
        self.player1 = copy.deepcopy(player1)
        self.player2 = copy.deepcopy(player2)
        self.root = Node(None, None)
        self.node_count = 0
        self.simulations = 0
        self.run_time = 0

    def Select(self):
        node, state = self.root, copy.deepcopy(self.root_state)

        while len(node.children) != 0:
            children = node.children
            values = [child.GetUCTValue() for child in children]
            max_value = max(values)
            best_children = [children[i] for i in range(len(children)) if values[i] == max_value]

            node = random.choice(best_children)
            state.SimulateMove(node.move, self.player1, self.player2)

            if node.total_games == 0:
                return node, state
            
        if self.Expand(node, state):
            node = random.choice(list(node.children))
            state.SimulateMove(node.move, self.player1, self.player2)
        return node, state
    
    def Expand(self, parent, state):
        if state.is_terminal_node():
            return False
        
        children = [Node(move, parent) for move in state.GetValidMoves()]
        parent.SetChildren(children)

        return True
    
    def Simulate(self, state):
        while not state.is_terminal_node():
            state.SimulateMove(random.choice(state.GetValidMoves()), self.player1, self.player2)
        #print(f"Player Who Won: {player1.GetPiece() if state.CheckForWin(player1.GetPiece()) else player2.GetPiece() if state.CheckForWin(player2.GetPiece()) else None}")
        return (self.player1.GetPiece() if state.CheckForWin(self.player1.GetPiece()) else self.player2.GetPiece() if state.CheckForWin(self.player2.GetPiece()) else None)
    
    def Backpropagate(self, node, turn, outcome):
        if outcome == turn:
            score = 0
        else:
            score = 1

        if node is not None:
            node.total_games += 1
            node.wins += score

            if outcome is None:
                score += 0
            else:
                score = 1 - score

            self.Backpropagate(node.parent, turn, outcome)

    def Search(self, time_limit):
        start_time = time.process_time()

        simulations = 0

        while time.process_time() - start_time < time_limit:
            node, state = self.Select()
            outcome = self.Simulate(state)
            self.Backpropagate(node, self.player1.GetPiece() if self.player1.GetTurn() else self.player2.GetPiece(), outcome)
            simulations += 1

        run_time = time.process_time() - start_time
        self.run_time = run_time
        self.simulations = simulations

    def GetBestMove(self):
        if self.root_state.is_terminal_node():
            return -1
        else:
            max_value = max(self.root.children, key=lambda x: x.total_games).total_games
            max_nodes = [x for x in self.root.children if x.total_games == max_value]
            best_child = random.choice(max_nodes)
            print(best_child.move)
            return best_child.move
    
    def UpdateMove(self, move):
        if move in self.root.children:
            self.root_state.SimulateMove(move, self.player1, self.player2)
            self.root = self.root.children[move]
        
        self.root_state.SimulateMove(move, self.player1, self.player2)
        self.root = Node(None, None)

def Main_2p(player1, player2, board1):
    winner = None
    game_over = False
    board1.PrintBoard()
    board1.DisplayBoard(player1, player2)
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
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        try:
                            board1.Undo()
                            board1.PrintBoard()
                            board1.DisplayBoard(player1, player2)
                        except Exception:
                            continue
            pygame.display.update()
            pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
            #print("Clicks allowed")
            #print(f"after allowed, mouse clicks blocked: {pygame.event.get_blocked(pygame.MOUSEBUTTONDOWN)}")
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = event.pos[0]
                current_column = (x_pos - ((info.current_w - 700)//2)) // SQUARE_SIZE #floor division to get whole number value of column, -600 to offset the 600 pixels i added to centre the board 
                if not board1.IsValidMove(current_column): #doesn't allow user to drop piece outside the board
                    continue
                if player1.GetTurn():
                    #print("Mouse Clicked")
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    #print(f"after mouse clicked, mouse clicks blocked: {pygame.event.get_blocked(pygame.MOUSEBUTTONDOWN)}")
                    board1.DropPiece(current_column, player1.GetPiece())
                    board1.Store(current_column)
                    if board1.CheckForWin(player1.GetPiece()):
                        pygame.draw.rect(screen, BLACK, (0, 0, info.current_w, ((info.current_h-600)/2)))
                        text = font.render(f"{player1.GetUsername()} won!", 1, player1.GetColour())
                        text_rect = text.get_rect(center=(info.current_w/2, 76//2))
                        screen.blit(text, text_rect)
                        game_over = True
                        winner = player1.GetUsername()
                    elif board1.CheckForDraw():
                        pygame.draw.rect(screen, BLACK, (0, 0, info.current_w, ((info.current_h-600)/2)))
                        text = font.render("DRAW!", 1, (255, 255, 255))
                        text_rect = text.get_rect(center=(info.current_w/2, 76//2))
                        screen.blit(text, text_rect)
                        game_over = True
                    player1.SetTurn(False)
                    player2.SetTurn(True)
                else:
                    #print("Mouse Clicked")
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    #print(f"after mouse clicked, mouse clicks blocked: {pygame.event.get_blocked(pygame.MOUSEBUTTONDOWN)}")
                    board1.DropPiece(current_column, player2.GetPiece())
                    board1.Store(current_column)
                    if board1.CheckForWin(player2.GetPiece()):
                        pygame.draw.rect(screen, BLACK, (0, 0, info.current_w, ((info.current_h-600)/2)))
                        text = font.render(f"{player2.GetUsername()} won!", 1, player2.GetColour())
                        text_rect = text.get_rect(center=(info.current_w/2, 75//2))
                        screen.blit(text, text_rect)
                        game_over = True
                        winner = player2.GetUsername()
                    elif board1.CheckForDraw():
                        pygame.draw.rect(screen, BLACK, (0, 0, info.current_w, ((info.current_h-600)/2)))
                        text = font.render("DRAW!", 1, (255, 255, 255))
                        text_rect = text.get_rect(center=(info.current_w/2, 75//2))
                        screen.blit(text, text_rect)
                        game_over = True
                    player2.SetTurn(False)
                    player1.SetTurn(True)    
                board1.PrintBoard()
                board1.DisplayBoard(player1, player2)
                if game_over:
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN) 
                    pygame.time.wait(3000)
                    return winner

def Main(player1, player2, board1):
    game_over = False
    board1.PrintBoard()
    board1.DisplayBoard(player1, player2)
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        try:
                            board1.Undo()
                            board1.PrintBoard()
                            board1.DisplayBoard(player1, player2)
                        except Exception:
                            continue
                pygame.display.update()
                pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                #print("Clicks allowed")
                #print(f"after allowed, mouse clicks blocked: {pygame.event.get_blocked(pygame.MOUSEBUTTONDOWN)}")
                if event.type == pygame.MOUSEBUTTONDOWN and not pygame.event.get_blocked(pygame.MOUSEBUTTONDOWN):
                    #print("Mouse Clicked")
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    #print(f"after mouse clicked, mouse clicks blocked: {pygame.event.get_blocked(pygame.MOUSEBUTTONDOWN)}")
                    x_pos = event.pos[0]
                    current_column = (x_pos - ((info.current_w - 700)//2)) // SQUARE_SIZE #floor division to get whole number value of column, -600 to offset the 600 pixels i added to centre the board 
                    if not board1.IsValidMove(current_column): #doesn't allow user to drop piece outside the board
                        continue
                    if player1.GetTurn():
                        board1.DropPiece(current_column, player1.GetPiece())
                        board1.Store(current_column)
                        if board1.CheckForWin(player1.GetPiece()):
                            pygame.draw.rect(screen, BLACK, (0, 0, info.current_w, ((info.current_h-600)/2)))
                            text = font.render("Player One won!", 1, player1.GetColour())
                            text_rect = text.get_rect(center=(info.current_w/2, 76//2))
                            screen.blit(text, text_rect)
                            game_over = True
                        elif board1.CheckForDraw():
                            pygame.draw.rect(screen, BLACK, (0, 0, info.current_w, ((info.current_h-600)/2)))
                            text = font.render("DRAW!", 1, (255, 255, 255))
                            text_rect = text.get_rect(center=(info.current_w/2, 76//2))
                            screen.blit(text, text_rect)
                            game_over = True
                        player1.SetTurn(False)
                        player2.SetTurn(True)
                        board1.PrintBoard()
                        board1.DisplayBoard(player1, player2)

                if player2.GetTurn() and not game_over:
                    #print("AI Move")
                    #print(f"after ai move, mouse clicks blocked: {pygame.event.get_blocked(pygame.MOUSEBUTTONDOWN)}")
                    ai_move = board1.minimax(board1, player2.GetDifficulty(), -math.inf, math.inf, True)[0]
                    board1.DropPiece(ai_move, 2)#board1.DropPiece(random.randint(0, 6), 2)
                    board1.Store(ai_move)
                    if board1.CheckForWin(player2.GetPiece()):
                        pygame.draw.rect(screen, BLACK, (0, 0, info.current_w, ((info.current_h-600)/2)))
                        text = font.render("AI Player won!", 1, player2.GetColour())
                        text_rect = text.get_rect(center=(info.current_w/2, 75//2))
                        screen.blit(text, text_rect)
                        game_over = True
                    elif board1.CheckForDraw():
                        pygame.draw.rect(screen, BLACK, (0, 0, info.current_w, ((info.current_h-600)/2)))
                        text = font.render("DRAW!", 1, (255, 255, 255))
                        text_rect = text.get_rect(center=(info.current_w/2, 75//2))
                        screen.blit(text, text_rect)
                        game_over = True 
                    player2.SetTurn(False)
                    player1.SetTurn(True)
                    board1.PrintBoard()
                    board1.DisplayBoard(player1, player2)
                if game_over:
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)  
                    pygame.time.wait(3000)

def MainMCTS(player1, player2, board1, mcts_obj):
    game_over = False
    board1.PrintBoard()
    board1.DisplayBoard(player1, player2)
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        try:
                            board1.Undo()
                            board1.PrintBoard()
                            board1.DisplayBoard(player1, player2)
                        except Exception:
                            continue
                pygame.display.update()
                pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                #print("Clicks allowed")
                #print(f"after allowed, mouse clicks blocked: {pygame.event.get_blocked(pygame.MOUSEBUTTONDOWN)}")
                if event.type == pygame.MOUSEBUTTONDOWN and not pygame.event.get_blocked(pygame.MOUSEBUTTONDOWN):
                    #print("Mouse Clicked")
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    #print(f"after mouse clicked, mouse clicks blocked: {pygame.event.get_blocked(pygame.MOUSEBUTTONDOWN)}")
                    x_pos = event.pos[0]
                    current_column = (x_pos - ((info.current_w - 700)//2)) // SQUARE_SIZE #floor division to get whole number value of column, -600 to offset the 600 pixels i added to centre the board 
                    if not board1.IsValidMove(current_column): #doesn't allow user to drop piece outside the board
                        continue
                    if player1.GetTurn():
                        board1.DropPiece(current_column, player1.GetPiece())
                        mcts_obj.UpdateMove(current_column)
                        board1.Store(current_column)
                        if board1.CheckForWin(player1.GetPiece()):
                            pygame.draw.rect(screen, BLACK, (0, 0, info.current_w, ((info.current_h-600)/2)))
                            text = font.render("Player One wins!", 1, player1.GetColour())
                            text_rect = text.get_rect(center=(info.current_w/2, 76//2))
                            screen.blit(text, text_rect)
                            game_over = True
                        elif board1.CheckForDraw():
                            pygame.draw.rect(screen, BLACK, (0, 0, info.current_w, ((info.current_h-600)/2)))
                            text = font.render("DRAW!", 1, (255, 255, 255))
                            text_rect = text.get_rect(center=(info.current_w/2, 76//2))
                            screen.blit(text, text_rect)
                            game_over = True
                        player1.SetTurn(False)
                        player2.SetTurn(True)
                        board1.PrintBoard()
                        board1.DisplayBoard(player1, player2)

                if player2.GetTurn() and not game_over:
                    #print("AI Move")
                    #print(f"after ai move, mouse clicks blocked: {pygame.event.get_blocked(pygame.MOUSEBUTTONDOWN)}")
                    mcts_obj.Search(player2.GetDifficulty())
                    ai_move = mcts_obj.GetBestMove()
                    board1.DropPiece(ai_move, 2)
                    mcts_obj.UpdateMove(ai_move)
                    board1.Store(ai_move)
                    if board1.CheckForWin(player2.GetPiece()):
                        pygame.draw.rect(screen, BLACK, (0, 0, info.current_w, ((info.current_h-600)/2)))
                        text = font.render("AI Player wins!", 1, player2.GetColour())
                        text_rect = text.get_rect(center=(info.current_w/2, 75//2))
                        screen.blit(text, text_rect)
                        game_over = True
                    elif board1.CheckForDraw():
                        pygame.draw.rect(screen, BLACK, (0, 0, info.current_w, ((info.current_h-600)/2)))
                        text = font.render("DRAW!", 1, (255, 255, 255))
                        text_rect = text.get_rect(center=(info.current_w/2, 75//2))
                        screen.blit(text, text_rect)
                        game_over = True   
                    player2.SetTurn(False)
                    player1.SetTurn(True)
                    board1.PrintBoard()
                    board1.DisplayBoard(player1, player2)
                if game_over:
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN) 
                    pygame.time.wait(3000)


#FROM HERE, CODE FOR MENU
def secure_password(password):
    min_length = 8
    uppercase = 0
    lowercase = 0
    digit = 0

    # Check each character in the password
    for char in password:
        if 'A' <= char <= 'Z':
            uppercase += 1
        elif 'a' <= char <= 'z':
            lowercase += 1
        elif '0' <= char <= '9':
            digit += 1

    # Check if the password meets the criteria
    if len(password) >= min_length and (uppercase + lowercase + digit >= 8 and (uppercase >= 1 and lowercase >= 1 and digit >= 1)):
        return True
    else:
        return False

def play_game():
    # code for play with friend
    print("Playing game...")

def search_user(user_id):
    try:
        conn = sqlite3.connect("c4db.db")
        cursor = conn.cursor()
        with conn:
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchall()
        return result
    except Exception as error:
        print(error)
    finally:
        conn.close()

def add_user(username, password, user_id):
    try:
        conn = sqlite3.connect("c4db.db")
        cursor = conn.cursor()
        with conn:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?, 0)", (user_id, username, password))
    except Exception as error:
        print(error)
    finally:
        conn.close()

def update_score(username):
    try:
        conn = sqlite3.connect("c4db.db")
        cursor = conn.cursor()
        with conn:
            cursor.execute("UPDATE users SET wins = wins + 1 WHERE username = ?", (username,))
    except Exception as error:
        print(error)
    finally:
        conn.close()

def go_to_leaderboard():
    # code for play with bot
    main_menu._open(leaderboard)

def quit_game():
    # code for back
    print("Quitting...")
    exit()

def open_options_menu():
    main_menu._open(options_menu)

def play_with_friend():
    # code for play with friend
    print("Playing with friend...")
    main_menu._open(login_menu)

def play_with_bot():
    # code for play with bot
    print("Playing with bot...")
    main_menu._open(customise_menu)

def hash_function(input):
    value = 0
    [value := value + ord(i) for i in input] #calculates ascii value of a string input
    return value % 200

def login():
    user = username_input.get_value()
    pwd = password_input.get_value()
    id = hash_function(user)
    result = search_user(id)

    user_not_found = "User not found!"
    wrong_combo = "Incorrect username or password!"
    widget_titles = [widget.get_title() for widget in login_menu.get_widgets()]

    if result == []:
        if user_not_found not in widget_titles:
            login_menu.add.label(user_not_found)
    else:
        #CHECK PASSWORD AND IF CORRECT GO TO NEXT SCREEN
        if pwd == result[0][2]:
            #go to next screen
            #print("Go to next screen")
            for widget in login_menu.get_widgets():
                if widget.get_title() == user_not_found or widget.get_title() == wrong_combo:
                    login_menu.remove_widget(widget)
            main_menu._open(login_menu_p2)
            return (user, pwd)
        else:
            if wrong_combo not in widget_titles:
                login_menu.add.label(wrong_combo)

def login_p2():
    user = username_input_p2.get_value()
    pwd = password_input_p2.get_value()
    id = hash_function(user)
    result = search_user(id)
    previous_user_details = login()

    double_login = "User already logged in!"
    user_not_found = "User not found!"
    wrong_combo = "Incorrect username or password!"
    widget_titles = [widget.get_title() for widget in login_menu_p2.get_widgets()]

    if previous_user_details[0] == user:
        if double_login not in widget_titles:
            login_menu_p2.add.label(double_login)
    elif result == []:
        if user_not_found not in widget_titles:
            login_menu_p2.add.label(user_not_found)
    else:
        #CHECK PASSWORD AND IF CORRECT GO TO NEXT SCREEN
        if pwd == result[0][2]:
            #go to next screen
            #print("Go to next screen")
            for widget in login_menu_p2.get_widgets():
                if widget.get_title() == user_not_found or widget.get_title() == wrong_combo or widget.get_title() == double_login:
                    login_menu_p2.remove_widget(widget)
            main_menu._open(customise_2p)
            return (user, pwd)
        else:
            if wrong_combo not in widget_titles:
                login_menu_p2.add.label(wrong_combo)

def register():
    user = username_input.get_value()
    pwd = password_input.get_value()
    id = hash_function(user)
    result = search_user(id)
    
    registered_successfully = "User successfully registered!"
    already_registered = "User has already been registered, please log-in instead!"
    weak_password = "Password must be at least 8 characters, and have number, capital, and lowercase letters!"
    widget_titles = [widget.get_title() for widget in login_menu.get_widgets()]

    if result != []:
        if already_registered not in widget_titles:#not already_registered:
            login_menu.add.label(already_registered)
    elif secure_password(pwd):
        if registered_successfully not in widget_titles:
            add_user(user, pwd, id)
            login_menu.add.label(registered_successfully)
    else:
        if weak_password not in widget_titles:
            login_menu.add.label(weak_password)

def register_p2():
    user = username_input_p2.get_value()
    pwd = password_input_p2.get_value()
    id = hash_function(user)
    result = search_user(id)
    
    registered_successfully = "User successfully registered!"
    already_registered = "User has already been registered, please log-in instead!"
    weak_password = "Password must be at least 8 characters, and have number, capital, and lowercase letters!"
    widget_titles = [widget.get_title() for widget in login_menu_p2.get_widgets()]

    if result != []:
        if already_registered not in widget_titles:#not already_registered:
            login_menu_p2.add.label(already_registered)
    elif secure_password(pwd):
        if registered_successfully not in widget_titles:
            add_user(user, pwd, id)
            login_menu_p2.add.label(registered_successfully)
    else:
        if weak_password not in widget_titles:
            login_menu_p2.add.label(weak_password)

# Function to be called when the user clicks on the "Play" button
def start_ai_game():
    global played_ai

    missing_options = "You must choose an option from all dropdown lists!"
    same_colour = "Both players can't choose the same colour!"
    widget_titles = [widget.get_title() for widget in customise_menu.get_widgets()]

    try:
        selected_value1 = drop_down1.get_value()  # get_value() returns the user choice as a tuple (since that's how it's defined in the code) with the index of the selected choice in the corresponding choices array
        selected_value2 = drop_down2.get_value()  # example: (('Hard', 4), 3), (('Green', (0, 255, 0)), 1), (('Blue', (0, 0, 255)), 2), (('Player 1', 1), 0)
        selected_value3 = drop_down3.get_value()
        selected_value4 = drop_down4.get_value()
        if selected_value2 == selected_value3:
            raise NameError
        played_ai = False
        board = Board()
        human_player = Player(1, True if selected_value4[0][1] == 1 else False, selected_value2[0][1], "You")
        ai_player = AIPlayer(2, False if selected_value4[0][1] == 1 else True, selected_value3[0][1], selected_value1[0][1])
        for widget in customise_menu.get_widgets():
            if widget.get_title() == missing_options or widget.get_title() == same_colour:
                customise_menu.remove_widget(widget)
        main_menu.disable()
        screen.fill((0, 0, 0))
        if selected_value1[1] == 0:
            mcts = MCTS(board, human_player, ai_player)
            MainMCTS(human_player, ai_player, board, mcts)
        else:
            Main(human_player, ai_player, board)
        main_menu.enable()
    except ValueError:
        if missing_options not in widget_titles:
            customise_menu.add.label(missing_options)
    except NameError:
        if same_colour not in widget_titles:
            customise_menu.add.label(same_colour)

def start_2p_game():
    global played_2p

    missing_options = "You must choose an option from all dropdown lists!"
    same_colour = "Both players can't choose the same colour!"
    widget_titles = [widget.get_title() for widget in customise_2p.get_widgets()]

    try:
        selected_value1 = dropdown1_2p.get_value()  # get_value() returns the user choice as a tuple (since that's how it's defined in the code) with the index of the selected choice in the corresponding choices array
        selected_value2 = dropdown2_2p.get_value()  # example: (('Hard', 4), 3), (('Green', (0, 255, 0)), 1), (('Blue', (0, 0, 255)), 2), (('Player 1', 1), 0)
        selected_value3 = dropdown3_2p.get_value()
        if selected_value1 == selected_value2:
            raise NameError
        played_2p = False
        p1_details = login()
        p2_details = login_p2()
        board = Board()
        player_one = Player(1, True if selected_value3[0][1] == 1 else False, selected_value1[0][1], p1_details[0])
        player_two = Player(2, False if selected_value3[0][1] == 1 else True, selected_value2[0][1], p2_details[0])
        for widget in customise_2p.get_widgets():
            if widget.get_title() == missing_options or widget.get_title() == same_colour:
                customise_2p.remove_widget(widget)
        main_menu.disable()
        screen.fill((0, 0, 0))
        winner = Main_2p(player_one, player_two, board)
        if winner != None:
            update_score(winner)
        main_menu.enable()
    except ValueError:
        if missing_options not in widget_titles:
            missing_options_widget = customise_2p.add.label(missing_options)
    except NameError:
        if same_colour not in widget_titles:
            same_colour_widget = customise_2p.add.label(same_colour)

def remove_all_widgets(menu):
    for widget in menu.get_widgets():
        menu.remove_widget(widget)

def update_leaderboard():
    remove_all_widgets(leaderboard)
    # main_menu._open(leaderboard)
    leaderboard.add.button("Update", update_leaderboard)
    i = 0
    for user in merge_sort(GetList(), wins=lambda x: x[1]):
        i += 1
        leaderboard.add.label(str(i) + ". " + str(user[0]) + "\t\t\t\t\t\twins: " + str(user[1]))

# create main menu
main_menu = pygame_menu.Menu("Connect Four Game", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_SOLARIZED)

main_menu.add.button("Play game", open_options_menu)
main_menu.add.button("Leaderboard", go_to_leaderboard)
main_menu.add.button("Quit", quit_game)

# create game options menu
options_menu = pygame_menu.Menu("Connect Four Game Options", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_SOLARIZED)

options_menu.add.button("Login & Play with Friend", play_with_friend)
options_menu.add.button("Play with Bot (No login)", play_with_bot)

# Create leaderboard screen
leaderboard = pygame_menu.Menu("Leaderboard", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_SOLARIZED)

leaderboard.add.button("Update", update_leaderboard)
update_leaderboard()

# Create login menu
login_menu = pygame_menu.Menu("Login for Player 1", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_SOLARIZED)
username_input = login_menu.add.text_input("Username: ", maxchar=20)  # Add text input for username
password_input = login_menu.add.text_input("Password: ", maxchar=20, password=True)  # Add password input
login_menu.add.button("Login", login)  # add login button
login_menu.add.button("Register", register)  # add register button


login_menu_p2 = pygame_menu.Menu("Login for Player 2", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_SOLARIZED)
username_input_p2 = login_menu_p2.add.text_input("Username: ", maxchar=20)  # Add text input for username
password_input_p2 = login_menu_p2.add.text_input("Password: ", maxchar=20, password=True)  # Add password input
login_menu_p2.add.button("Login", login_p2)  # add login button
login_menu_p2.add.button("Register", register_p2)  # add register button
login_menu_p2.add.label("Player 1 logged in successfully!")


# Create a Pygame Menu
customise_menu = pygame_menu.Menu("Customise Game", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_SOLARIZED)

# Add four drop-down lists
drop_down1_choices = [
    ("Easiest (MCTS)", 5),
    ("Easier (Minimax)", 1),
    ("Easy (Minimax)", 2),
    ("Medium (Minimax)", 4),
    ("Hard (Minimax)", 6),
    ("Hardest (Minimax)", 7),
]

drop_down1 = customise_menu.add.dropselect("Difficulty: ", drop_down1_choices, onchange=None)

drop_down2_choices = [
    ("Red", (255, 0, 0)),
    ("Green", (0, 255, 0)),
    ("Yellow", (255, 255, 0)),
    ("Purple", (160, 32, 240)),
]

drop_down2 = customise_menu.add.dropselect("1st Player Colour: ", drop_down2_choices, onchange=None)

drop_down3_choices = [
    ("Red", (255, 0, 0)),
    ("Green", (0, 255, 0)),
    ("Yellow", (255, 255, 0)),
    ("Purple", (160, 32, 240)),
]

drop_down3 = customise_menu.add.dropselect("2nd Player Colour: ", drop_down3_choices, onchange=None)

drop_down4_choices = [("Player 1", 1), ("Player 2", 2), ("Random", int(random.randint(1,2)))]

drop_down4 = customise_menu.add.dropselect("First Move: ", drop_down4_choices, onchange=None)

# Add a "Play" button to trigger the start_ai_game function
play = customise_menu.add.button("Play", start_ai_game)

customise_2p = pygame_menu.Menu("2P Customise", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_SOLARIZED)

customise_2p.add.label("Both players logged in successfully!")

dropdown1_2p = customise_2p.add.dropselect("1st Player Colour: ", drop_down2_choices, onchange=None)

dropdown2_2p = customise_2p.add.dropselect("2nd Player Colour: ", drop_down3_choices, onchange=None)

dropdown3_2p = customise_2p.add.dropselect("First Move: ", drop_down4_choices, onchange=None)

play_2p = customise_2p.add.button("Play", start_2p_game)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if main_menu.is_enabled():
        main_menu.update(events)
        main_menu.draw(screen)
    pygame.display.update()
