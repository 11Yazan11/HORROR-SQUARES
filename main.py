import pygame
import math
import random
import time
import ast


pygame.init()

class Game:
    def __init__(self):
        self.wnx = 600
        self.wny = 600
        self.run = True
        self.screen = pygame.display.set_mode((self.wnx, self.wny))

        self.fps = 10
        self.score = 0
        self.level = 4
        self.level1time = None
        self.level2time = None
        self.level3time = None
        self.level4time = None

        self.bg_start = True
        self.max_time = 200
        self.time = 0
        self.clock = pygame.time.Clock()

        self.direction = ""
        self.levelsgrids()
        self.original_grid = self.allgrids[self.level - 1]
        self.grid = self.allgrids[self.level - 1]
        self.grid[1] = 2

        self.coin_sound = pygame.mixer.Sound("coin.mp3")
        self.coin_sound.set_volume(1)
        self.win_sound = pygame.mixer.Sound("win.mp3")
        self.win_sound.set_volume(1)
        self.game_over_sound = pygame.mixer.Sound("gameover.mp3")
        self.jumpscare_sound = pygame.mixer.Sound("jusound.mp3")
        self.jumpscare2_sound = pygame.mixer.Sound("jusound2.mp3")
        self.letsgosound = pygame.mixer.Sound("letsgo.mp3")
        self.oui = pygame.mixer.Sound("ouioui.mp3")
        self.chinese = pygame.mixer.Sound("chinese.mp3")

        self.mrbeast = pygame.mixer.Sound("mrbeast.mp3")
        self.mrbeast.set_volume(0.4)

        self.ahh = pygame.mixer.Sound("ahh.mp3")
        self.ahh.set_volume(1.5)

        self.ban = pygame.mixer.Sound("ban.mp3")
        self.ban.set_volume(0.4)

        self.bruh = pygame.mixer.Sound("bruh.mp3")
        self.bruh.set_volume(1)

        self.lvl4song = pygame.mixer.Sound("song.mp3")
        self.lvl4song.set_volume(1)
        

    

        self.jumpscare_img = pygame.image.load("ju.png").convert_alpha()
        self.jumpscare_img = pygame.transform.scale(self.jumpscare_img, (self.wnx/2, self.wny/2))

        self.mario = pygame.image.load("mario.jpeg").convert_alpha()
        self.mario = pygame.transform.scale(self.mario, (self.wnx, self.wny))

        self.check = pygame.image.load("check.png").convert_alpha()
        self.check = pygame.transform.scale(self.check, (self.wnx/2, self.wny/2))

        

        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break
            # Call functions
            self.mouse_handling()
            self.move()
            self.update_grid()
            self.window(self.grid)
            self.levelsgrids()
            # ..............
            pygame.display.flip()
            self.clock.tick(self.fps)

            if self.direction != "":
                self.time += 0.5

            if self.direction != "" and self.bg_start:
                if self.level == 1:
                    self.mrbeast.play(loops=-1)
                if self.level == 2:
                    self.ahh.play(loops=-1)
                if self.level == 3:
                    self.ban.play(loops=-1) 
                self.bg_start = False
                if self.level == 4:
                    self.lvl4song.play(loops=-1)

            if self.level == 1:
                self.max_time = 200

            if self.level == 2:
                self.max_time = 230 

            if self.level == 3:
                self.max_time = 300 

            if self.level == 4:
                self.max_time = 210       

            if self.time >= self.max_time:
                self.loose()   

    def window(self, grid):
        pressed = pygame.key.get_pressed()
        self.screen.fill((100, 30, 60))
        pygame.display.set_caption(f"HORROR SQUARES || FPS = {self.fps} || SCORE = {self.score} || LEVEL = {self.level} || TIME = {self.time} / {self.max_time} ||")

        grid_size = int(math.sqrt(len(grid)))
        cell_width = self.wnx / grid_size
        cell_height = self.wny / grid_size

        for i in range(len(grid)):
            x = (i % grid_size) * cell_width
            y = (i // grid_size) * cell_height
            rect_zone = pygame.Rect(x, y, cell_width, cell_height)

            # FOR EDITING...

            #if self.mouse_rect.colliderect(rect_zone) and pygame.mouse.get_pressed()[0] == 1:
            #    grid[i] = 1
            #if self.mouse_rect.colliderect(rect_zone) and pygame.mouse.get_pressed()[2] == 1:
            #    grid[i] = 0
            #if self.mouse_rect.colliderect(rect_zone) and pressed[pygame.K_SPACE]:
            #    grid[i] = 3  

            #.....................      
            
            color = "black" if grid[i] == 0 else "white" if grid[i] == 1 else "red" if grid[i] == 2 else "yellow" if grid[i] == 3 else "blue"
            pygame.draw.rect(self.screen, color, rect_zone)

    def update_grid(self):
        
        grid_size = int(math.sqrt(len(self.grid)))
        red_pos = self.grid.index(2)

        if self.direction == "UP" and red_pos >= grid_size:
            dest_pos = red_pos - grid_size
            if self.grid[dest_pos] == 3:
                self.grid[red_pos] = 0
                self.grid[dest_pos] = 2
                self.coin_sound.play()
                self.score += 1 
            if self.grid[dest_pos] == 0:  # Check if destination cell is not white
                self.grid[red_pos] = 0  # Leave black cell behind
                self.grid[dest_pos] = 2  # Move red square to the destination

            if self.grid[dest_pos] == 4 and 3 not in self.grid:
                self.grid[red_pos] = 0
                self.grid[dest_pos] = 4
                self.win()    
   
        elif self.direction == "DOWN" and red_pos < len(self.grid) - grid_size:
            dest_pos = red_pos + grid_size
            if self.grid[dest_pos] == 3:
                self.grid[red_pos] = 0
                self.grid[dest_pos] = 2
                self.coin_sound.play()
                self.score += 1  
            if self.grid[dest_pos] == 0:  # Check if destination cell is not white
                self.grid[red_pos] = 0  # Leave black cell behind
                self.grid[dest_pos] = 2  # Move red square to the destination

            if self.grid[dest_pos] == 4 and 3 not in self.grid:
                self.grid[red_pos] = 0
                self.grid[dest_pos] = 4
                self.win()    
 
        elif self.direction == "LEFT" and red_pos % grid_size != 0:
            dest_pos = red_pos - 1
            if self.grid[dest_pos] == 3:
                self.grid[red_pos] = 0
                self.grid[dest_pos] = 2
                self.score += 1  
                self.coin_sound.play()
            if self.grid[dest_pos] == 0:  # Check if destination cell is not white
                self.grid[red_pos] = 0  # Leave black cell behind
                self.grid[dest_pos] = 2

            if self.grid[dest_pos] == 4 and 3 not in self.grid:
                self.grid[red_pos] = 0
                self.grid[dest_pos] = 4
                self.win()    
   
        elif self.direction == "RIGHT" and (red_pos + 1) % grid_size != 0:
            dest_pos = red_pos + 1
            if self.grid[dest_pos] == 3:
                self.grid[red_pos] = 0
                self.grid[dest_pos] = 2
                self.score += 1
                self.coin_sound.play()
            if self.grid[dest_pos] == 0:  # Check if destination cell is not white
                self.grid[red_pos] = 0  # Leave black cell behind
                self.grid[dest_pos] = 2  # Move red square to the destination

            if self.grid[dest_pos] == 4 and 3 not in self.grid:
                self.grid[red_pos] = 0
                self.grid[dest_pos] = 4
                self.win()    


    

    # Reset direction after move


    def mouse_handling(self):
        self.mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)

    def move(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.direction = "UP"  
        elif pressed[pygame.K_DOWN]:
            self.direction = "DOWN"
        elif pressed[pygame.K_LEFT]:
            self.direction = "LEFT"
        elif pressed[pygame.K_RIGHT]:
            self.direction = "RIGHT"
    def loose(self):
        self.mrbeast.stop()
        self.ahh.stop()
        self.ban.stop()
        self.screen.fill((0, 0, 0))
        pygame.display.set_caption(f"HORROR SQUARES || FPS = {self.fps} || SCORE = {self.score} || LEVEL = {self.level} || TIME = {self.time} / {self.max_time}")
        self.bruh.play()
        self.game_over_sound.play()
        self.screen.blit(self.mario, (0, 0))
        pygame.display.flip()
        time.sleep(0.9)
        self.screen.blit(self.jumpscare_img, (0, 0))
        self.jumpscare_sound.play(loops=-1)
        self.jumpscare2_sound.play(loops=-1)
        for i in range(1000 * 7):
            rand_color = random.randint(0, 1)*255
            self.screen.fill((rand_color, rand_color, rand_color))
            self.screen.blit(self.jumpscare_img, (self.wnx / 4 + random.randint(0, 10), self.wny / 4 + random.randint(0, 10)))
            pygame.display.flip()
        pygame.display.flip()
        self.run = False

    def levelsgrids(self):

        self.grid1 = [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 3,
                     1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
                     1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0,
                     1, 0, 1, 0, 1, 3, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0,
                     1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0,
                     1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0,
                     1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0,
                     1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                     1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0,
                     1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0,
                     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0,
                     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0,
                     1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0,
                     1, 1, 1, 0, 1, 3, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0,
                     1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 3,
                     3, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 3, 1, 1, 0, 1, 0,
                     1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0,
                     3, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0,
                     1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4]
        
        self.grid2 = [1, 2, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                      1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
                      1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 3, 1, 1, 0, 1, 1, 0, 1, 0,
                      1, 1, 1, 0, 1, 3, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0,
                      1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0,
                      1, 3, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0,
                      1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0,
                      1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0,
                      1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0,
                      1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0,
                      1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0,
                      1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0,
                      1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0,
                      1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0,
                      1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3,
                      3, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0,
                      0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 3, 1, 0, 0, 1, 0,
                      0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0,
                      0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0,
                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4]
        
        
        self.grid3 = [0, 2, 1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                      0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1,
                      0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                      1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0,
                      1, 0, 0, 0, 1, 0, 0, 3, 1, 3, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0,
                      1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 3, 0, 1, 0, 0,
                      0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
                      0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0,
                      1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0,
                      0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0,
                      0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,
                      0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0,
                      0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                      0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1,
                      0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0,
                      1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0,
                      0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0,
                      0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 3, 1, 1, 1, 0, 1, 1, 1,
                      0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,
                      3, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 4]
        
        self.grid4 = [0, 2, 1, 1, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 3, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 3, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 3, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 3, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 3, 1, 1, 0, 1, 1, 0, 1, 1, 4, 4, 4, 1]

        # THE GRID FOR LEVEL 4 IS THE ONE WRITTEN IN THE TEXT FILE, WHEN THE CODE WAS LAST RUN.
        with open("grids\grids.txt", "r") as file:
            content = (file.read().strip())
            self.grid4 = eval(content)
        #................................    

        self.allgrids = [self.grid1, self.grid2, self.grid3, self.grid4]
        

    def win(self):
        pygame.display.flip()
        self.mrbeast.stop()
        self.ahh.stop()
        self.ban.stop()
        self.lvl4song.stop()
        self.win_sound.play()
        self.direction = ""
        if self.level == 4:
            self.level4time = self.time  
            pygame.display.set_caption(f' YOUR SKIBIDI TIMES : LEVEL 1 = {self.level1time} // LEVEL 2 = {self.level2time} // LEVEL 3 = {self.level3time}')
            pygame.display.flip()
            self.time = 0  
            self.screen.fill('green')
            self.screen.blit(self.check, (self.wnx / 4, self.wny / 4))
            pygame.display.flip()
            self.letsgosound.play()
            time.sleep(3.2)
            self.chinese.play()
            time.sleep(4)
            pygame.display.set_caption(f' YOUR SKIBIDI TIMES : LEVEL 2 = {self.level2time} // LEVEL 3 = {self.level3time} // LEVEL 4 = {self.level4time}')
            pygame.display.flip()
            time.sleep(3)
            self.oui.play()
            time.sleep(7)
            self.run = False 
        else:   
            if self.level == 1:
                self.level1time = self.time
            if self.level == 2:
                self.level2time = self.time
            if self.level == 3:
                self.level3time = self.time    
            self.level += 1
            self.time = 0    
            self.bg_start = True      
            self.original_grid = self.allgrids[self.level - 1]
            self.grid = self.allgrids[self.level - 1]
            self.grid[1] = 2                   

game = Game()

# ADD THE CURRENT GRID TO A TEXT FILE
with open("grids\grids.txt",'w') as file:
   file.write(str(game.grid))
#.................   

pygame.quit()
