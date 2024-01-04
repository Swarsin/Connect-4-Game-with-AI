#trying to make login screen

# import pygame as pg

# pg.init()
# FONT = pg.font.Font(None, 42)

# def main():
#     screen = pg.display.set_mode((640, 480))
#     clock = pg.time.Clock()
#     username = ''
#     password = ''
#     done = False
#     while not done:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 done = True
#             elif event.type == pg.KEYDOWN:
#                 if event.key == pg.K_RETURN:
#                     # Do something with the username and password and reset them.
#                     print(f'Username: {username}, Password: {password}')
#                     # I just print it to see if it works.
#                     username = ''
#                     password = ''
#                 elif event.unicode.isalpha() or event.unicode.isdigit():
#                     # Add the character to the appropriate string.
#                     if len(username) < 10:
#                         username += event.unicode
#                     elif len(password) < 10:
#                         password += event.unicode
#         screen.fill((30, 30, 30))
#         # Render the username and password boxes and blit them.
#         username_surface = FONT.render(username, True, (70, 200, 150))
#         password_surface = FONT.render('*' * len(password), True, (70, 200, 150))
#         screen.blit(username_surface, (30, 30))
#         screen.blit(password_surface, (30, 80))
#         pg.display.flip()
#         clock.tick(30)

# if __name__ == '__main__':
#     main()
#     pg.quit()

# import pygame as pg

# pg.init()
# FONT = pg.font.Font(None, 32)

# class InputBox:
#     def __init__(self, x, y, w, h):
#         self.rect = pg.Rect(x, y, w, h)
#         self.color = pg.Color('lightskyblue3')
#         self.text = ''
#         self.txt_surface = FONT.render(self.text, True, self.color)
#         self.active = False

#     def handle_event(self, event):
#         if event.type == pg.MOUSEBUTTONDOWN:
#             # Toggle the active variable.
#             if self.rect.collidepoint(event.pos):
#                 self.active = not self.active
#             else:
#                 self.active = False
#             self.color = self.color_active if self.active else self.color_inactive
#         if event.type == pg.KEYDOWN:
#             if self.active:
#                 if event.key == pg.K_RETURN:
#                     print(self.text)
#                     self.text = ''
#                 elif event.key == pg.K_BACKSPACE:
#                     self.text = self.text[:-1]
#                 else:
#                     self.text += event.unicode
#                 # Re-render the text.
#                 self.txt_surface = FONT.render(self.text, True, self.color)

#     def update(self):
#         # Resize the box if the text is too long.
#         width = max(200, self.txt_surface.get_width() + 10)
#         self.rect.w = width

#     def draw(self, screen):
#         # Blit the text.
#         screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
#         # Blit the rect.
#         pg.draw.rect(screen, self.color, self.rect, 2)

# def main():
#     screen = pg.display.set_mode((640, 480))
#     clock = pg.time.Clock()
#     username_box = InputBox(100, 100, 140, 32)
#     password_box = InputBox(100, 200, 140, 32)
#     username_box.color_inactive = pg.Color('red')
#     password_box.color_inactive = pg.Color('red')
#     username_box.color_active = pg.Color('green')
#     password_box.color_active = pg.Color('green')
#     done = False
#     while not done:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 done = True
#             username_box.handle_event(event)
#             password_box.handle_event(event)
#         # Update the text boxes.
#         username_box.update()
#         password_box.update()
#         screen.fill((30, 30, 30))
#         username_box.draw(screen)
#         password_box.draw(screen)
#         pg.display.flip()
#         clock.tick(30)

# if __name__ == '__main__':
#     main()
#     pg.quit()



#First iteration: (highlight boxes when selected for some reason)
# import pygame as pg

# pg.init()
# FONT = pg.font.Font(None, 32)

# class InputBox:
#     def __init__(self, x, y, w, h):
#         self.rect = pg.Rect(x, y, w, h)
#         self.color = pg.Color('lightskyblue3')
#         self.text = ''
#         self.txt_surface = FONT.render(self.text, True, self.color)
#         self.active = False

#     def handle_event(self, event):
#         if event.type == pg.MOUSEBUTTONDOWN:
#             # Toggle the active variable.
#             if self.rect.collidepoint(event.pos):
#                 self.active = not self.active
#             else:
#                 self.active = False
#             self.color = self.color_active if self.active else self.color_inactive
#         if event.type == pg.KEYDOWN:
#             if self.active:
#                 if event.key == pg.K_RETURN:
#                     print(self.text)
#                     self.text = ''
#                 elif event.key == pg.K_BACKSPACE:
#                     self.text = self.text[:-1]
#                 else:
#                     self.text += event.unicode
#                 # Re-render the text.
#                 self.txt_surface = FONT.render(self.text, True, self.color)

#     def update(self):
#         # Resize the box if the text is too long.
#         width = max(200, self.txt_surface.get_width() + 10)
#         self.rect.w = width

#     def draw(self, screen):
#         # Blit the text.
#         screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
#         # Blit the rect.
#         pg.draw.rect(screen, self.color, self.rect, 2)

# def main():
#     screen = pg.display.set_mode((640, 480))
#     clock = pg.time.Clock()
#     username_box = InputBox(100, 100, 140, 32)
#     password_box = InputBox(100, 200, 140, 32)
#     username_box.color_inactive = pg.Color('red')
#     password_box.color_inactive = pg.Color('red')
#     username_box.color_active = pg.Color('green')
#     password_box.color_active = pg.Color('green')
#     done = False
#     while not done:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 done = True
#             username_box.handle_event(event)
#             password_box.handle_event(event)

#         # Update the text box.
#         username_box.update()
#         password_box.update()

#         # Draw everything.
#         screen.fill((30, 30, 30))
#         username_box.draw(screen)
#         password_box.draw(screen)

#         pg.display.flip()
#         clock.tick(30)

# if __name__ == '__main__':
#     main()

#Second Iteration - no highlighting boxes and text
# import pygame as pg

# pg.init()
# FONT = pg.font.Font(None, 32)

# class InputBox:
#     def __init__(self, x, y, w, h):
#         self.rect = pg.Rect(x, y, w, h)
#         self.color = pg.Color('lightskyblue3')
#         self.text = ''
#         self.txt_surface = FONT.render(self.text, True, self.color)
#         self.active = False

#     def handle_event(self, event):
#         if event.type == pg.MOUSEBUTTONDOWN:
#             # Toggle the active variable.
#             if self.rect.collidepoint(event.pos):
#                 self.active = not self.active
#             else:
#                 self.active = False
#             self.color = self.color_active if self.active else self.color_inactive
#         if event.type == pg.KEYDOWN:
#             if self.active:
#                 if event.key == pg.K_RETURN:
#                     print(self.text)
#                     self.text = ''
#                 elif event.key == pg.K_BACKSPACE:
#                     self.text = self.text[:-1]
#                 else:
#                     self.text += event.unicode
#                 # Re-render the text.
#                 self.txt_surface = FONT.render(self.text, True, self.color)

#     def update(self):
#         # Resize the box if the text is too long.
#         width = max(200, self.txt_surface.get_width() + 10)
#         self.rect.w = width

#     def draw(self, screen):
#         pg.draw.rect(screen, self.color, self.rect, 2)
#         screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

# def main():
#     screen = pg.display.set_mode((640, 480))
#     clock = pg.time.Clock()
#     username_box = InputBox(100, 100, 140, 32)
#     password_box = InputBox(100, 200, 140, 32)
#     username_box.color_inactive = pg.Color('white')
#     password_box.color_inactive = pg.Color('white')
#     username_box.color_active = pg.Color('white')
#     password_box.color_active = pg.Color('white')
#     done = False
#     while not done:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 done = True
#             username_box.handle_event(event)
#             password_box.handle_event(event)
#         # Update the text boxes.
#         username_box.update()
#         password_box.update()
#         screen.fill((30, 30, 30))
#         username_box.draw(screen)
#         password_box.draw(screen)
#         pg.display.flip()
#         clock.tick(30)

# if __name__ == '__main__':
#     main()
#     pg.quit()

#Third iterarion - added submit button
# import pygame as pg

# pg.init()
# FONT = pg.font.Font(None, 32)

# class InputBox:
#     def __init__(self, x, y, w, h):
#         self.rect = pg.Rect(x, y, w, h)
#         self.color = pg.Color('lightskyblue3')
#         self.text = ''
#         self.txt_surface = FONT.render(self.text, True, self.color)
#         self.active = False

#     def handle_event(self, event):
#         if event.type == pg.MOUSEBUTTONDOWN:
#             # Toggle the active variable.
#             if self.rect.collidepoint(event.pos):
#                 self.active = not self.active
#             else:
#                 self.active = False
#             self.color = self.color_active if self.active else self.color_inactive
#         if event.type == pg.KEYDOWN:
#             if self.active:
#                 if event.key == pg.K_RETURN:
#                     print(self.text)
#                     self.text = ''
#                 elif event.key == pg.K_BACKSPACE:
#                     self.text = self.text[:-1]
#                 else:
#                     self.text += event.unicode
#                 # Re-render the text.
#                 self.txt_surface = FONT.render(self.text, True, self.color)

#     def update(self):
#         # Resize the box if the text is too long.
#         width = max(200, self.txt_surface.get_width() + 10)
#         self.rect.w = width

#     def draw(self, screen):
#         # Blit the text.
#         screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
#         # Blit the rect.
#         pg.draw.rect(screen, self.color, self.rect, 2)

# class Button(pg.sprite.Sprite):
#     def __init__(self, x, y, w, h, color, text, callback):
#         super().__init__()
#         self.rect = pg.Rect(x, y, w, h)
#         self.color = color
#         self.text = text
#         self.callback = callback
#         self.font = pg.font.Font(None, 32)
#         self.image = self.font.render(self.text, True, self.color)
#         self.rect = self.image.get_rect(center=self.rect.center)

#     def update(self, events):
#         for event in events:
#             if event.type == pg.MOUSEBUTTONDOWN:
#                 if self.rect.collidepoint(event.pos):
#                     self.callback()

#     def draw(self, screen):
#         screen.blit(self.image, self.rect)

# def main():
#     screen = pg.display.set_mode((640, 480))
#     clock = pg.time.Clock()
#     username_box = InputBox(100, 100, 140, 32)
#     password_box = InputBox(100, 200, 140, 32)
#     submit_button = Button(100, 300, 140, 32, pg.Color('green'), 'Submit', lambda: print(f'Username: {username_box.text}, Password: {password_box.text}'))
#     username_box.color_inactive = pg.Color('white')
#     password_box.color_inactive = pg.Color('white')
#     username_box.color_active = pg.Color('white')
#     password_box.color_active = pg.Color('white')
#     done = False
#     while not done:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 done = True
#             username_box.handle_event(event)
#             password_box.handle_event(event)
#             submit_button.update([event])
#         # Update the text boxes.
#         username_box.update()
#         password_box.update()
#         screen.fill((30, 30, 30))
#         username_box.draw(screen)
#         password_box.draw(screen)
#         submit_button.draw(screen)
#         pg.display.flip()
#         clock.tick(30)

# if __name__ == '__main__':
#     main()
#     pg.quit()

import pygame as pg

pg.init()
FONT = pg.font.Font(None, 32)

class InputBox:
    def __init__(self, x, y, w, h, label):
        self.rect = pg.Rect(x, y, w, h)
        self.color = pg.Color('white')
        self.text = ''
        self.txt_surface = FONT.render(self.text, True, self.color)
        self.active = False
        self.label = label

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # Toggle the active variable.
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(f'{self.label}: {self.text}')
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the label.
        label_surface = FONT.render(self.label, True, pg.Color('white'))
        screen.blit(label_surface, (self.rect.x + 5, self.rect.y - 25))
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

class Button(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, color, text, callback):
        super().__init__()
        self.rect = pg.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.callback = callback
        self.font = pg.font.Font(None, 32)
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.callback()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

#def validate(): 

#def secure(password):
#    if len(password) >= 8 and 



def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    username_box = InputBox(100, 100, 140, 32, 'Username')
    password_box = InputBox(100, 200, 140, 32, 'Password')
    login_button = Button(60, 300, 140, 32, pg.Color('green'), 'Login', lambda: print(f'Username: {username_box.text}, Password: {password_box.text}'))
    register_button = Button(75, 350, 140, 32, pg.Color('red'), 'Register', lambda: print(f'Register - Username: {username_box.text}, Password: {password_box.text}'))
    username_box.color_inactive = pg.Color('white')
    password_box.color_inactive = pg.Color('white')
    username_box.color_active = pg.Color('white')
    password_box.color_active = pg.Color('white')
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            username_box.handle_event(event)
            password_box.handle_event(event)
            login_button.update([event])
            register_button.update([event])
        # Update the text boxes.
        username_box.update()
        password_box.update()
        screen.fill((30, 30, 30))
        username_box.draw(screen)
        password_box.draw(screen)
        login_button.draw(screen)
        register_button.draw(screen)
        pg.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
    pg.quit()
