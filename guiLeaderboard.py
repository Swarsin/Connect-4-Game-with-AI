# import pygame
# import random
# from leaderboard import sorted_tuples
# # Initialize pygame and create a window
# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Leaderboard Example")
# clock = pygame.time.Clock()

# # Create a font object
# font = pygame.font.SysFont("Arial", 32)

# # Create a list of sample names and scores
# names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Harry", "Ivy", "Jack", "Swaraj", "Singh", "Who", "Am", "I", "Talking", "About"]
# scores = [random.randint(0, 100) for _ in range(len(names))]

# # Sort the names and scores by descending order of scores
# names_scores = sorted(zip(names, scores), key=lambda x: x[1], reverse=True)

# # Create a surface to draw the leaderboard on8
# leaderboard = pygame.surface.Surface((8000, 1000))

# # Draw the names and scores on the leaderboard
# y = 50
# for name, score in names_scores:
#     text = font.render(f"{name}: {score}", True, (255, 255, 255))
#     leaderboard.blit(text, (100, y))
#     y += 100

# # Create a variable to store the scroll offset
# scroll_y = 0

# # Main loop
# running = True
# while running:
#     # Handle events
#     for event in pygame.event.get():
#         # Quit the program if the user closes the window
#         if event.type == pygame.QUIT:
#             running = False
#         # Scroll the leaderboard if the user uses the mouse wheel
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 4: scroll_y = min(scroll_y + 15, 0)
#             if event.button == 5: scroll_y = max(scroll_y - 15, -400)

#     # Fill the screen with black
#     screen.fill((0, 0, 0))

#     # Blit the leaderboard on the screen with the scroll offset
#     screen.blit(leaderboard, (0, scroll_y))

#     # Update the display
#     pygame.display.flip()

#     # Limit the frame rate
#     clock.tick(60)

# # Quit pygame
# pygame.quit()


import pygame
import random
from leaderboard import sorted_tuples
# Initialize pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE) # Make the window resizable
pygame.display.set_caption("Leaderboard Example")
clock = pygame.time.Clock()

sorted_tuples.append(("osidfj", 3))
sorted_tuples.append(("uikwefshbdgidfj", 3))
sorted_tuples.append(("owsnfe", 3))
sorted_tuples.append(("weoiur", 3))
sorted_tuples.append(("mlkscd", 3))
sorted_tuples.append(("wpeiuro", 3))
sorted_tuples.append(("posdmf", 3))
sorted_tuples.append(("qwpoei", 3))
sorted_tuples.append(("xddfj", 3))

# Create a font object
font = pygame.font.SysFont("Arial", 32) 

# Calculate the height of the leaderboard surface based on the number of users
leaderboard_height = len(sorted_tuples) * 100

# Create a surface to draw the leaderboard on
leaderboard = pygame.surface.Surface((800, leaderboard_height))

# Draw a plain background on the leaderboard
leaderboard.fill((0, 0, 0))

# Draw the names and scores on the leaderboard
y = 150 #increasing this means that the text is printed lower, decreasing means text will be higher up in the screen 
for tuple in sorted_tuples:
    text = font.render(f"{tuple[0]}: {tuple[1]}", True, (255, 255, 255))
    leaderboard.blit(text, (100, y))
    y += 100
# Create a variable to store the scroll offset
scroll_y = 0

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        # Quit the program if the user closes the window
        if event.type == pygame.QUIT:
            running = False
        # Scroll the leaderboard if the user uses the mouse wheel
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: scroll_y = min(scroll_y + 15, 0)
            if event.button == 5: scroll_y = max(scroll_y - 15, -leaderboard_height + 600) # Adjust the scroll limit based on the leaderboard height
        # Resize the window and the leaderboard if the user changes the window size
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE) # Update the screen size
            leaderboard = pygame.transform.scale(leaderboard, (event.w, event.h)) # Scale the leaderboard to fit the new size

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Blit the leaderboard on the screen with the scroll offset
    screen.blit(leaderboard, (0, scroll_y))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
