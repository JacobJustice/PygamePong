import pygame

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600

class RectangleEntity():
    x = 0
    y = 0
    width = 10
    height = 10
    color = (255,255)
    v_x = 0
    v_y = 0
    
    def __init__(self, x, y, width, height, color, v_x=0, v_y=0):
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
        self.color = color
        self.v_x = v_x
        self.v_y = v_y
    
    def __str__(self):
        return 'x: ' + str(self.x) + ' y: ' + str(self.y) + ' width: ' + str(self.width) + ' height: ' + str(self.height) + ' color: ' + str(self.color)
    
    def update(self, dt):
        self.x += self.v_x
        self.y += self.v_y

    def display(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Puck(RectangleEntity):
    def __init__(self, x, y, width, height, color, v_x=0, v_y=0):
        super().__init__(x, y, width, height, color, v_x, v_y)
    
    def middle(self):
        self.x=(SCREEN_WIDTH-self.width)/2
        self.y=(SCREEN_HEIGHT-self.height)/2
        self.v_x*=-1
    
    def update(self, dt):
        if self.y+self.height > SCREEN_HEIGHT or self.y < 0:
            self.v_y *= -1
        self.x += self.v_x
        self.y += self.v_y


class Paddle(RectangleEntity):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)

    def check_collision(self, puck):
        paddle_right = self.x + self.width
        paddle_bottom = self.y + self.height
        puck_right = puck.x + puck.width
        puck_bottom = puck.y + puck.height

        if paddle_right >= puck.x and self.x <= puck_right and paddle_bottom >= puck.y and self.y <= puck_bottom:
            return True
        else:
            return False

class Model:
    screen_width = SCREEN_WIDTH
    screen_height = SCREEN_HEIGHT
    FPS = 60
    running = True
    clock = pygame.time.Clock()
    score = [0,0]

    def __init__(self):
        self.puck = Puck(x=(self.screen_width-10)/2, y=(self.screen_height-10)/2, width=10, height=10, color=(255,255,255), v_x=3, v_y=3)
        self.paddle1 = Paddle(x=5, y=(self.screen_height-90)/2, width=10, height=90, color=(255,255,0))
        self.paddle2 = Paddle(x=(self.screen_width-15), y=(self.screen_height-90)/2, width=10, height=90, color=(0,255,255))
        self.entities = [self.paddle1, self.paddle2, self.puck]

    def __str__(self):
        return 'puck ' + str(self.puck) + '\npaddle1 ' + str(self.paddle1) + '\npaddle2 ' + str(self.paddle2)
    
    def update(self, controller):
        if controller.quit:
            self.running = False
            return

        # Player controls
        if controller.player_up:
            self.paddle1.v_y = -2
        elif controller.player_down:
            self.paddle1.v_y = 2
        else:
            self.paddle1.v_y = 0
        
        # Paddle 2 AI
        if (self.puck.y+self.puck.height/2) > (self.paddle2.y+self.paddle2.height/2):
            self.paddle2.v_y = 2
        else:
            self.paddle2.v_y = -2

        # should a point be given?
        if self.puck.x+self.puck.width > SCREEN_WIDTH:
            #give point to AI
            self.score[0] += 1
            self.puck.middle()
            print('+1 point for Paddle 1, score is now', self.score[0], '-', self.score[1])

        if self.puck.x < 0:
            #give point to player
            self.score[1] += 1
            self.puck.middle()
            print('+1 point for Paddle 2, score is now', self.score[0], '-', self.score[1])

        if self.paddle1.check_collision(self.puck) or self.paddle2.check_collision(self.puck):
            self.puck.v_x *= -1
        #calculate dt
        dt = self.clock.tick(self.FPS) / 1000
        for entity in self.entities:
            entity.update(dt)

class View:
    screen = None
    background_color = (64, 0, 64)
    def __init__(self, screen):
        self.screen = screen

    def display(self, model):
        self.screen.fill(self.background_color)
        for entity in model.entities:
            entity.display(self.screen)
        pygame.display.update()

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    KEYDOWN,
    QUIT,
)

class Controller:
    quit = False
    player_up = False
    player_down = False
    
    def update(self):
        self.player_down = False
        self.player_up = False
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit = True

        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self.player_up = True
        if keys[K_DOWN]:
            self.player_down = True
                
if __name__ == '__main__':
    import main