import pygame, pygame_menu, sys, psycopg2
from leaderboard import sorted_tuples
from ai_mode_adjusted import *
from main import Main_2p
pygame.init()

info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h))

password_error_displayed = False
user_not_found_displayed = False
incorrect_combo_error_displayed = False

ai_value_error_displayed = False
ai_repeated_error_displayed = False
played_ai = False

value_error_displayed_2p = False
repeated_error_displayed_2p = False
played_2p = False

hostname = 'localhost'
database = 'c4db'
db_username = 'postgres'
db_pwd = 'admin'
port_id = 5432
conn = None

def secure_password(password):
    min_length = 8
    has_uppercase = False
    has_lowercase = False
    has_digit = False

    # Check each character in the password
    for char in password:
        if 'A' <= char <= 'Z':
            has_uppercase = True
        elif 'a' <= char <= 'z':
            has_lowercase = True
        elif '0' <= char <= '9':
            has_digit = True

    # Check if the password meets the criteria
    if len(password) >= min_length and has_uppercase and has_lowercase and has_digit:
        return True
    else:
        return False

def play_game():
    # code for play with friend
    print("Playing game...")

def search_user(user_id):
    try:
        with psycopg2.connect(
            host = hostname,
            dbname = database,
            user = db_username,
            password = db_pwd,
            port = port_id) as conn:

            with conn.cursor() as cur:
                query = "SELECT * FROM USERS WHERE id = %s"
                cur.execute(query, (user_id,))
                result = [cur.fetchall()]
                return result
    except Exception as error:
        print(error)
    finally:
        # if cur is not None: #don't need to close cursor when using the with clause
        #     cur.close()
        if conn is not None:
            conn.close()

def add_user(username, password, id):
    try:
        with psycopg2.connect(
            host = hostname,
            dbname = database,
            user = db_username,
            password = db_pwd,
            port = port_id) as conn:
        
            with conn.cursor() as cur:
                
                insert_script = '''INSERT INTO users (id, username, password, wins) VALUES (%s, %s, %s, %s)'''
                record = (id, username, password, 0)
                cur.execute(insert_script, record)

    except Exception as error:
        print(error)

    finally:
        # if cur is not None: #don't need to close cursor when using the with clause
        #     cur.close()
        if conn is not None:
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
    global user_not_found_displayed
    global incorrect_combo_error_displayed

    user = username_input.get_value()
    pwd = password_input.get_value()
    id = hash_function(user)
    print(id)
    result = search_user(id)[0]
    print(result)
    if result == []:
        if not user_not_found_displayed:
            login_menu.add.label(("User not found!"))
            user_not_found_displayed = True
    else:
        #CHECK PASSWORD AND IF CORRECT GO TO NEXT SCREEN
        if pwd == result[0][2]:
            #go to next screen
            print("Go to next screen")
            main_menu._open(customise_2p)
        else:
            if not incorrect_combo_error_displayed:
                login_menu.add.label(("Incorrect username or password!"))
                incorrect_combo_error_displayed = True


def register():
    global password_error_displayed

    user = username_input.get_value()
    pwd = password_input.get_value()
    id = hash_function(user)
    if secure_password(pwd):
        add_user(user, pwd, id)
        #AND GO TO NEXT MENU SCREEN
    else:
        if not password_error_displayed:
            login_menu.add.label(("Password must have number, capitals, and lowercase letters!"))
            password_error_displayed = True

# Function to be called when the user clicks on the "Play" button
def start_ai_game():
    global ai_value_error_displayed
    global ai_repeated_error_displayed
    global played_ai
    try:
        selected_value1 = drop_down1.get_value()  # get_value() returns the user choice as a tuple (since that's how it's defined in the code) with the index of the selected choice in the corresponding choices array
        selected_value2 = drop_down2.get_value()  # example: (('Hard', 4), 3), (('Green', (0, 255, 0)), 1), (('Blue', (0, 0, 255)), 2), (('Player 1', 1), 0)
        selected_value3 = drop_down3.get_value()
        selected_value4 = drop_down4.get_value()
        if selected_value2 == selected_value3:
            raise NameError
        played_ai = False
        pygame.time.set_timer(open_ai_game, 1)
        return (selected_value1, selected_value2, selected_value3, selected_value4)
    except ValueError:
        if not ai_value_error_displayed:
            #print("You must choose an option from all dropdown lists") #for testing
            customise_menu.add.label(("You must choose an option from all dropdown lists!"))
            ai_value_error_displayed = True
    except NameError:
        if not ai_repeated_error_displayed:
            #print("You must choose an option from all dropdown lists") #for testing
            customise_menu.add.label(("Both players can't choose the same colour!"))
            ai_repeated_error_displayed = True

def start_2p_game():
    global value_error_displayed_2p
    global repeated_error_displayed_2p
    global played_2p
    try:
        selected_value1 = dropdown1_2p.get_value()  # get_value() returns the user choice as a tuple (since that's how it's defined in the code) with the index of the selected choice in the corresponding choices array
        selected_value2 = dropdown2_2p.get_value()  # example: (('Hard', 4), 3), (('Green', (0, 255, 0)), 1), (('Blue', (0, 0, 255)), 2), (('Player 1', 1), 0)
        selected_value3 = dropdown3_2p.get_value()
        if selected_value1 == selected_value2:
            raise NameError
        played_2p = False
        pygame.time.set_timer(open_2p_game, 1)
        print((selected_value1, selected_value2, selected_value3))
        return (selected_value1, selected_value2, selected_value3)
    except ValueError:
        if not value_error_displayed_2p:
            #print("You must choose an option from all dropdown lists") #for testing
            customise_2p.add.label(("You must choose an option from all dropdown lists!"))
            value_error_displayed_2p = True
    except NameError:
        if not repeated_error_displayed_2p:
            #print("You must choose an option from all dropdown lists") #for testing
            customise_2p.add.label(("Both players can't choose the same colour!"))
            repeated_error_displayed_2p = True

# create main menu
main_menu = pygame_menu.Menu("Connect Four Game", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_BLUE)

main_menu.add.button("Play game", open_options_menu)
main_menu.add.button("Leaderboard", go_to_leaderboard)
main_menu.add.button("Quit", quit_game)

# create game options menu
options_menu = pygame_menu.Menu("Connect Four Game Options", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_BLUE)

options_menu.add.button("Login & Play with Friend", play_with_friend)
options_menu.add.button("Play with Bot (No login)", play_with_bot)

# Create leaderboard screen
leaderboard = pygame_menu.Menu("Leaderboard", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_BLUE)

i = 0
for user in sorted_tuples:
    i += 1
    leaderboard.add.label(str(i) + "." + str(user[0]) + "\t\t\t\t\t\twins: " + str(user[1]))

# Create login menu
login_menu = pygame_menu.Menu("Login", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_BLUE)

username_input = login_menu.add.text_input("Username: ", maxchar=20)  # Add text input for username

password_input = login_menu.add.text_input("Password: ", maxchar=20, password=True)  # Add password input

login_menu.add.button("Login", login)  # add login button
login_menu.add.button("Register", register)  # add register button

# Create a Pygame Menu
customise_menu = pygame_menu.Menu("Customise Game", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_BLUE)

# Add four drop-down lists
drop_down1_choices = [
    ("Very easy", 1),
    ("Easy", 2),
    ("Medium", 4),
    ("Hard", 6),
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

customise_2p = pygame_menu.Menu("2P Customise", info.current_w, info.current_h, theme=pygame_menu.themes.THEME_BLUE)

dropdown1_2p = customise_2p.add.dropselect("1st Player Colour: ", drop_down2_choices, onchange=None)

dropdown2_2p = customise_2p.add.dropselect("2nd Player Colour: ", drop_down3_choices, onchange=None)

dropdown3_2p = customise_2p.add.dropselect("First Move: ", drop_down4_choices, onchange=None)

play_2p = customise_2p.add.button("Play", start_2p_game)

open_ai_game = pygame.USEREVENT + 0

open_2p_game = pygame.USEREVENT + 1 

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == open_ai_game:
            if not played_ai:
                pygame.time.set_timer(open_ai_game, 1)
                main_menu.disable()
                main_menu.full_reset() 
                screen.fill((0, 0, 0))
                choices = start_ai_game()
                board = Board()
                human_player = Player("Player 1", 1, (True if choices[3][0][1] == 1 else False), choices[1][0][1])
                ai_player = AIPlayer(2, (True if choices[3][0][1] == 2 else False), choices[2][0][1], choices[0][0][1])
                board.PrintBoard()
                board.DisplayBoard(human_player, ai_player)
                pygame.display.update()
                Main(human_player, ai_player, board)
                played_ai = True
            else:
                main_menu.enable()
        elif event.type == open_2p_game:
            if not played_2p:
                pygame.time.set_timer(open_2p_game, 1)
                main_menu.disable()
                main_menu.full_reset()
                screen.fill((0, 0, 0))
                choices = start_2p_game()
                board = Board()
                player_one = Player("Player 1", 1, (True if choices[2][0][1] == 1 else False), choices[0][0][1])
                player_two = Player("Player 2", 2, (True if choices[2][0][1] == 2 else False), choices[1][0][1])
                board.PrintBoard()
                board.DisplayBoard(player_one, player_two)
                Main_2p(player_one, player_two, board)
                played_2p = True
            else:
                main_menu.enable()
    if main_menu.is_enabled():
        main_menu.update(events)
        main_menu.draw(screen)
    pygame.display.update()

