import pygame, pygame_menu, sys
from leaderboard import sorted_tuples

pygame.init()

info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h))


def play_game():
    # code for play with friend
    print("Playing game...")


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


def login():
    print(
        f"Login with username: {username_input.get_value()} and password: {password_input.get_value()}"
    )
    # Add verification and stuff for login logic here


def register():
    print(
        f"Register with username: {username_input.get_value()} and password: {password_input.get_value()}"
    )
    # Add verification and stuff for login logic here


# Function to be called when the user clicks on the "Play" button
def start_game():
    try:
        selected_value1 = (
            drop_down1.get_value()
        )  # get_value() returns the user choice as a tuple (since that's how it's defined in the code) with the index of the selected choice in the corresponding choices array
        selected_value2 = (
            drop_down2.get_value()
        )  # example: (('Hard', 4), 3), (('Green', (0, 255, 0)), 1), (('Blue', (0, 0, 255)), 2), (('Player 1', 1), 0)
        selected_value3 = drop_down3.get_value()
        selected_value4 = drop_down4.get_value()

        print(
            "Selected values: {}, {}, {}, {}".format(
                selected_value1, selected_value2, selected_value3, selected_value4
            )
        )

    except ValueError:
        print("You must choose an option from all dropdown lists")


# create main menu
main_menu = pygame_menu.Menu(
    "Connect Four Game",
    info.current_w,
    info.current_h,
    theme=pygame_menu.themes.THEME_BLUE,
)
main_menu.add.button("Play game", open_options_menu)
main_menu.add.button("Leaderboard", go_to_leaderboard)
main_menu.add.button("Quit", quit_game)

# create game options menu
options_menu = pygame_menu.Menu(
    "Connect Four Game Options",
    info.current_w,
    info.current_h,
    theme=pygame_menu.themes.THEME_BLUE,
)
options_menu.add.button("Login & Play with Friend", play_with_friend)
options_menu.add.button("Play with Bot (No login)", play_with_bot)

# Create leaderboard screen
leaderboard = pygame_menu.Menu(
    "Leaderboard", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_BLUE
)

i = 0
for user in sorted_tuples:
    i += 1
    leaderboard.add.label(
        str(i) + "." + str(user[0]) + "\t\t\t\t\t\twins: " + str(user[1])
    )

# Create login menu
login_menu = pygame_menu.Menu(
    "Login", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_BLUE
)
username_input = login_menu.add.text_input(
    "Username: ", maxchar=20
)  # Add text input for username
password_input = login_menu.add.text_input(
    "Password: ", maxchar=20, password=True
)  # Add password input
login_menu.add.button("Login", login)  # add login button
login_menu.add.button("Register", register)  # add register button

# Create a Pygame Menu
customise_menu = pygame_menu.Menu(
    "Customise Game",
    info.current_w,
    info.current_h,
    theme=pygame_menu.themes.THEME_BLUE,
)

# Add four drop-down lists
drop_down1_choices = [
    ("Very easy", 1),
    ("Easy", 2),
    ("Medium", 3),
    ("Hard", 4),
    ("Hardest", 5),
]
drop_down1 = customise_menu.add.dropselect(
    "Difficulty: ", drop_down1_choices, onchange=None
)

drop_down2_choices = [
    ("Red", (255, 0, 0)),
    ("Green", (0, 255, 0)),
    ("Blue", (0, 0, 255)),
]
drop_down2 = customise_menu.add.dropselect(
    "1st Player Colour: ", drop_down2_choices, onchange=None
)
drop_down3_choices = [
    ("Red", (255, 0, 0)),
    ("Green", (0, 255, 0)),
    ("Blue", (0, 0, 255)),
]
drop_down3 = customise_menu.add.dropselect(
    "2nd Player Colour: ", drop_down3_choices, onchange=None
)

drop_down4_choices = [("Player 1", 1), ("Player 2", 2)]
drop_down4 = customise_menu.add.dropselect(
    "First Move: ", drop_down4_choices, onchange=None
)

# Add a "Play" button to trigger the start_game function
customise_menu.add.button("Play", start_game)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
    if main_menu.is_enabled():
        main_menu.update(events)
        main_menu.draw(screen)
    pygame.display.update()
