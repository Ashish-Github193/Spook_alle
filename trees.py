import pygame, random
from particles import Dynamic_leaves
trees = []
for i in range(7):
    trees.append(pygame.image.load('assets/trees/tree' + str(i+10) + '.png'))

class Tree(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = random.choice(trees)
        self.rect = self.image.get_rect(topleft = [position[0], position[1]-192])
        self.leaf_list = []
        self.leaf_time = 10


    def leaves(self):
        self.leaf_list.append(Dynamic_leaves([self.rect.x, self.rect.y+64]))
 

    def update(self, x_shift, surface):

        if self.leaf_time == 0: 
            self.leaves()
            self.leaf_time = 50
        else:
            self.leaf_time -= 1

        for leaf in self.leaf_list:
                if leaf.rect.y > 704 or leaf.life<=0:
                    self.leaf_list.remove(leaf)
                else:
                    leaf.update(x_shift)
                    surface.blit(leaf.image, [leaf.rect.x, leaf.rect.y])

        self.rect.x += x_shift
        