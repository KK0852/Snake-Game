import pygame
from pygame.locals import *
import time
import random

SIZE=25
BACKGROUND_COLOR=(110,110,5)

class Apple:
    def __init__(self,parent_screen):
        self.image=pygame.image.load("apple1.jpeg").convert()
        self.parent_screen=parent_screen
        self.x=SIZE*5
        self.y=SIZE*0

    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x=random.randint(0,30)*SIZE
        self.y=random.randint(0,19)*SIZE

class Snake:
    def __init__(self,parent_screen,length):
        self.length=length
        self.parent_screen = parent_screen
        self.block=pygame.image.load("block1.png").convert()
        self.x=[SIZE]*length
        self.y=[SIZE]*length
        self.direction='down'

    def increse_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction ='left'
       
    
    def move_right(self):
        self.direction ='right'

    def move_up(self):
        self.direction ='up'

    def move_down(self):
      self.direction ='down'

    def draw(self):
        self.parent_screen.fill((110,110,5))
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]
        if self.direction=='up':
            self.y[0] -=SIZE
        if self.direction=='down':
            self.y[0] +=SIZE
        if self.direction=='left':
            self.x[0] -=SIZE
        if self.direction=='right':
            self.x[0] +=SIZE
        self.draw()

      

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((800,500))
        self.surface.fill(BACKGROUND_COLOR)
        self.snake=Snake(self.surface,1)
        self.snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()
    def is_collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1<x2+SIZE:
            if y1>=y2 and y1<y2+SIZE:
                return True
        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake collision with apple
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.snake.increse_length()
            self.apple.move()

        #snake collision with snake
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                raise "Game Over"
        #snake collision on wall
        if not(0<=self.snake.x[0] <= 800 and 0<= self.snake.y[0]<=500):
            raise "hit it"

    def display_score(self):
        font =pygame.font.SysFont('arial',30)
        score=font.render(f"score: {self.snake.length}",True,(255,255,255))
        self.surface.blit(score,(500,10))

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font =pygame.font.SysFont('arial',25)
        line1=font.render(f"Game is Over....Score is {self.snake.length}",True,(255,255,255))
        self.surface.blit(line1,(100,100))
        line2=font.render(f"For play again click ENTER , To exit press ESCAPE",True,(255,255,255))
        self.surface.blit(line2,(150,150))
        pygame.display.flip()

    def reset(self):
        self.snake=Snake(self.surface,1)
        self.apple=Apple(self.surface)

    def run(self):
        running = True
        pause=False
        while running:
            for event in pygame.event.get():
                if event.type== KEYDOWN:
                    if event.key==K_ESCAPE:
                        running=False

                    if event.key==K_RETURN:
                        pause=False
                    if not pause:        
                        if event.key==K_UP:
                            self.snake.move_up()
                            
                        if event.key==K_DOWN:
                            self.snake.move_down()

                        if event.key==K_LEFT:
                            self.snake.move_left()

                        if event.key==K_RIGHT:
                            self.snake.move_right()

                elif event.type==QUIT:
                    running=False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True
                self.reset()
            if(self.snake.length<3):
                time.sleep(0.4)
            else:
                time.sleep(0.1)


   

if __name__ == "__main__":
    game=Game()
    game.run()


  