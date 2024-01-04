import pygame
import pygame_menu

pygame.init()

# Initialize Pygame display
window_size = (800, 600)
pygame.display.set_mode(window_size)
pygame.display.set_caption("Connect 4")

# Create a Pygame Menu
menu = pygame_menu.Menu("Customise Game", 800, 600, theme=pygame_menu.themes.THEME_BLUE)

# Add four drop-down lists
drop_down1_choices = [("Very easy", 1), ("Easy", 2), ("Medium", 3), ("Hard", 4), ("Hardest", 5)]
drop_down1 = menu.add.dropselect("Difficulty: ", drop_down1_choices, onchange=None)

drop_down2_choices = [("Red", (255, 0, 0)), ("Green", (0, 255, 0)), ("Blue", (0, 0, 255))]
drop_down2 = menu.add.dropselect("1st Player Colour: ", drop_down2_choices, onchange=None)
drop_down3_choices = [("Red", (255, 0, 0)), ("Green", (0, 255, 0)), ("Blue", (0, 0, 255))]
drop_down3 = menu.add.dropselect("2nd Player Colour: ", drop_down3_choices, onchange=None)

drop_down4_choices = [("Player 1", 1), ("Player 2", 2)]
drop_down4 = menu.add.dropselect("First Move: ", drop_down4_choices, onchange=None)

# Function to be called when the user clicks on the "Play" button
def start_game():
    selected_value1 = drop_down1.get_value()
    selected_value2 = drop_down2.get_value()
    selected_value3 = drop_down3.get_value()
    selected_value4 = drop_down4.get_value()
    
    print("Selected values: {}, {}, {}, {}".format(selected_value1, selected_value2, selected_value3, selected_value4))

# Add a "Play" button to trigger the start_game function
menu.add.button("Play", start_game)

# Run the menu
menu.mainloop(pygame.display.set_mode(window_size))
pygame.quit()
