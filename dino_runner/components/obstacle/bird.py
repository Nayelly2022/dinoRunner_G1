from dino_runner.components.obstacle.obstacle import Obstacle
from dino_runner.utils.constants import BIRD
import random

class Bird(Obstacle):
    def __init__(self, imagen):
        self.type = 0
        super().__init__(imagen, self.type)
        self.rect.y = random.randint(1,205)
        self.step_index = 0
        

    def draw(self, screen):
        if self.step_index >= 10:
            self.step_index = 0
        screen.blit(self.image[self.step_index //5],self.rect)
        self.step_index += 1