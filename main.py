class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []
    
    def push(self, item):
        self.items.append(item)

    def pop(self, item):
        if not self.is_empty():
            return self.items.pop()
        
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
    
    def fetch(self, index): #to get item at specific index of the stack object
        if 0 <= index < len(self.items):        
            return self.items[index]
        else:
            return None
        
    def fetch_all(self): #returns copy of entire stack object - doesn't affect original
        return self.items.copy
        
    def size(self):
        return len(self.items)
    
    def __str__(self): #for testing/debugging
        return str(self.items)
    
    def __repr__(self): #for testing/debugging
        return str(self.items)

# board = [Stack() for i in range(6)]
# board[0].push('piece')

# print(board)
# print(board[0].fetch(7))

class Board:
    def __init__(self):
        self.board = [Stack() for i in range(7)]

    def output(self):
        print(self.board)

    


