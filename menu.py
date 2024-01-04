#Libraries used: 
#pygame for making the main menu 
#sys to exit the program when the user wants to quit

import pygame, sys

class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("NEA Folder/Background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("NEA Folder/font.otf", size)


def play(): #code that is run when play button is pressed
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("Work under progress", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(
            image=None,
            pos=(640, 460),
            text_input="BACK",
            font=get_font(75),
            base_color="White",
            hovering_color="Green",
        )

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def leaderboard():#code that is run when the LEADERBOARD button is pressed
    from leaderboard import sorted_tuples
    while True:
        LEADERBOARD_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        #LEADERBOARD_TEXT = get_font(45).render("Work under progress", True, "white")

        # font = pygame.font.SysFont('Arial', 20)

        # # Set the background color
        # background_color = (50, 50, 50)

        # # Set the text color
        # text_color = (255, 255, 255) 

        # # Loop through the array and render each element as text in a table
        # for i in range(len(sorted_tuples)):
        #     for j in range(len(sorted_tuples[i])):
        #         if j == 0:
        #             text = font.render(str(sorted_tuples[i][j]), True, text_color, background_color)
        #         else:
        #             text = font.render(str(sorted_tuples[i][j]), True, text_color, background_color)
        #             text = font.render('Wins: ' + str(sorted_tuples[i][j]), True, text_color, background_color)
        #         text_rect = text.get_rect()
        #         text_rect.center = (j * 100 + 50, i * 50 + 50)
        #         SCREEN.blit(text, text_rect)

        

        LEADERBOARD_BACK = Button(
            image=None,
            pos=(640, 460),
            text_input="BACK",
            font=get_font(75),
            base_color="White",
            hovering_color="Green",
        )

        LEADERBOARD_BACK.changeColor(LEADERBOARD_MOUSE_POS)
        LEADERBOARD_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEADERBOARD_BACK.checkForInput(LEADERBOARD_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu(): #code that is run to display the main menu
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Connect 4 Game", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(
            image=pygame.image.load("NEA Folder/Play Rect.png"),
            pos=(640, 250),
            text_input="PLAY",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )
        LEADERBOARD_BUTTON = Button(
            image=pygame.image.load("NEA Folder/Options Rect.png"),
            pos=(640, 400),
            text_input="LEADERBOARD",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )
        QUIT_BUTTON = Button(
            image=pygame.image.load("NEA Folder/Quit Rect.png"),
            pos=(640, 550),
            text_input="QUIT",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, LEADERBOARD_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if LEADERBOARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    leaderboard()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()