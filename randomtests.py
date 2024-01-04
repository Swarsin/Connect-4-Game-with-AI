# import pygame
# import numpy as np
from leaderboard import sorted_tuples

# # Define the array
# arr = np.array(sorted_tuples)

# # Initialize Pygame
# pygame.init()

# # Set the dimensions of the screen
# screen_width = 500
# screen_height = 500
# screen = pygame.display.set_mode((screen_width, screen_height))

# # Set the font and font size
# font = pygame.font.SysFont('Arial', 20)

# # Loop through the array and render each element as text
# for i in range(arr.shape[0]):
#     for j in range(arr.shape[1]):
#         text = font.render(str(arr[i][j]), True, (255, 255, 255))
#         text_rect = text.get_rect()
#         text_rect.center = (j * 100 + 50, i * 100 + 50)
#         screen.blit(text, text_rect)

# # Update the display
# pygame.display.update()

# # Wait for the user to close the window
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()


import pygame

# Define the array of tuples

# Initialize Pygame
pygame.init()

# Set the dimensions of the screen
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the font and font size
font = pygame.font.SysFont('Arial', 20)

# Set the background color

# Set the text color
text_color = (255, 255, 255) 

# Loop through the array and render each element as text in a table
for i in range(len(sorted_tuples)):
    for j in range(len(sorted_tuples[i])):
        if j == 0:
            text = font.render(str(sorted_tuples[i][j]), True, text_color)
        else:
            text = font.render(str(sorted_tuples[i][j]), True, text_color)
            text = font.render('Wins: ' + str(sorted_tuples[i][j]), True, text_color)
        text_rect = text.get_rect()
        text_rect.center = (j * 100 + 50, i * 50 + 50)
        screen.blit(text, text_rect)

# Update the display
pygame.display.update()

# Wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
