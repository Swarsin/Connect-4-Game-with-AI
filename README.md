# Connect-4-Game-with-AI
(My ongoing project)


Through Harvard CS50's Artificial Intelligence with Python course and further research into AlphaGo, I learned about adversarial search, Monte Carlo Tree Search and Minimax algorithm and their applications in board games. 
Intrigued, I set out to make an AI player for Connect 4, using a minimax algorithm.

I have used an array of 7 stacks objects to represent the game board, which isn't ideal, and makes things a bit more complicated. 

Done:
- made a somewhat functioning menu system
- made a functional connect 4 game (NEEDS TO BE FIXED*)
- made a functional connect 4 ai bot using minimax algorithm with alpha beta pruning to allow for a more advanced bot that can see farther into the future (can branch up to a depth of 6, with minor delays between moves at the start of the game)


To do:
- Need to change DisplayBoard method so that it creates a board that is centred on the display - currently the board is only centred for 1080p displays and running the game on any other sized displays messes up the game. !!!
- I aim to incorporate the "Play against friend" and "Play against AI/bot" mode into the menu system of the game soon.
- I'll also add functionality to allow the user to customise their game
