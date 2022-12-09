import pygame
from dino_runner.utils.constants import RUNNING,RUNNING_SHIELD ,DUCKING, DUCKING_SHIELD,JUMPING,SHIELD_TYPE, DEFAULT_TYPE,JUMPING_SHIELD,JUMP_SOUND
from pygame.sprite import Sprite

RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD}
DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD}

class Dinosaur():
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.type = DEFAULT_TYPE    
        self.image = RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.step_index = 0
        self.dino_run = True
        self.dino_duck= False
        self.dino_jump = False

        self.jump_vel = self.JUMP_VEL

        self.setup_state_booleans()

    def setup_state_booleans(self):
        self.has_powerup=False
        self.shield = False
        self.show_text = False
        self.shield_time_up = 0

    def update(self, user_input):
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        
        if user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
        
        elif user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
            JUMP_SOUND.play(0)      

        
        elif not self.dino_jump:
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False
        
        if self.step_index >=9:
            self.step_index = 0


    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.dino_rect.y = self.dino_rect.y - (self.jump_vel * 4)
            self.jump_vel = self.jump_vel - 0.8
        
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_rect.y = self.Y_POS
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
        
    def duck(self):
        self.image = DUCK_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS   
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index +=1

    def run(self):
        self.image = RUN_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS   
        self.dino_rect.y = self.Y_POS
        self.step_index +=1




    def draw(self,screen):
        screen.blit(self.image,(self.dino_rect.x,self.dino_rect.y))
    

    def check_invisivility(self,screen):
        if self.shield:
            time_to_show = round((self.shield_time_up - pygame.time.get_ticks())/100,2)
            if time_to_show >=0:
                if self.show_text:
                    fond = pygame.font.Font('freesansbold.ttf',18)
                    text = fond.render(f'Shield enable for {time_to_show}',True,(0,0,0))
                    textRect = text.get_rect()
                    textRect.center = (500,40)
                    screen.blit(text,textRect)
            
            else:
                self.shield = False
                self.update_to_default(SHIELD_TYPE)
    
    def update_to_default(self,current_type):
        if self.type == current_type:
            self.type = DEFAULT_TYPE

