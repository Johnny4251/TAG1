import pygame
from MenuButton import MenuButton

class MainMenu:
    def __init__(self,name):
        self.name = name
        self.state_machine = None
        self.active_button_idx = 0
        self.buttons = []
    
    def enter(self):
        print(f"Entering: {self.name}")
    
    def leave(self):
        print(f"Leaving: {self.name}")
    
    # User has selected the play button
    def play_pressed(self):
        self.state_machine.transition("game")
        print("PLAY GAME")
    
    # User has selected the credits button
    def credits_pressed(self):
        self.state_machine.transition("credits")
        print("CREDITS")
    
    # User has selected the quit button
    def quit_pressed(self):
        # Send signal to state machine to close window
        self.state_machine.window_should_close = True
        print("QUIT GAME")


    def render(self,window=None):
        color = (0, 0, 0)
        window.fill(color)

        # Add the logo to the window
        window.blit(self.create_logo("TAG"), (200,50))
        
        # Add each button to the window
        play_button = MenuButton("Play", "", self.play_pressed)
        credits_button = MenuButton("Credits", "", self.credits_pressed)
        quit_button = MenuButton("Quit", "", self.quit_pressed)

        # Keep track of all the buttons publically using a list
        self.buttons = [play_button, credits_button, quit_button]

        # Draw each button to the window
        # If the button is active(active_button_idx) then set active=True
        button_x,button_y = 200,200
        for i,button in enumerate(self.buttons):
            if i == self.active_button_idx:
                window.blit(button.create_button(active=True), (button_x,button_y))
            else: 
                window.blit(button.create_button(), (button_x,button_y))
            button_y+=50 # Just so they all don't place on top of each other

    # Creates and returns a title logo
    def create_logo(self, text):
        font = pygame.font.SysFont("Arial", 32)

        logo = font.render(text, True, (255, 0, 0))
        return logo

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state_machine.window_should_close = True
            
            # Handle key events
            # Up & Down keys change the active button index
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_UP:
                    if self.active_button_idx > 0:
                        self.active_button_idx -= 1
                    else:
                        self.active_button_idx = len(self.buttons) -1
                elif key == pygame.K_DOWN:
                    if len(self.buttons) - 1 > self.active_button_idx:
                        self.active_button_idx += 1
                    else:
                        self.active_button_idx = 0
                # On enter key pressed -> press the active button
                elif key == pygame.K_RETURN:
                    self.buttons[self.active_button_idx].pressed()
                elif key == pygame.K_ESCAPE:
                    self.state_machine.window_should_close = True