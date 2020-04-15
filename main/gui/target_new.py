#Variable 0: WIN_Width
def WIN_Width():
	file = open("variable", ).readlines()
	try:
		return int(file[0])
	except:
		return 570

#Variable 1: WIN_Height
def WIN_Height():
	file = open("variable", ).readlines()
	try:
		return int(file[1])
	except:
		return 800

#Variable 2: MAX_ROTATION
def MAX_ROTATION():
	file = open("variable", ).readlines()
	try:
		return int(file[2])
	except:
		return 25

#Variable 3: ROT_VEL
def ROT_VEL():
	file = open("variable", ).readlines()
	try:
		return int(file[3])
	except:
		return 20

#Variable 4: ANIMATION_TIME
def ANIMATION_TIME():
	file = open("variable", ).readlines()
	try:
		return int(file[4])
	except:
		return 5

#Variable 5: GAP
def GAP():
	file = open("variable", ).readlines()
	try:
		return int(file[5])
	except:
		return 200

#Variable 6: PVEL
def PVEL():
	file = open("variable", ).readlines()
	try:
		return int(file[6])
	except:
		return 5

#Variable 7: BVEL
def BVEL():
	file = open("variable", ).readlines()
	try:
		return int(file[7])
	except:
		return 5

import pygame
import neat
import time
import os
import random
import pickle
pygame.font.init()

WIN_Width_c = WIN_Width()
WIN_Height_c = WIN_Height()

GEN = 0

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("../images","ship_norm.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("../images","ship_up.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("../images","ship_down.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("../images","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("../images","border.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("../images","background.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)



class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION_c = MAX_ROTATION()
    ROT_VEL_c = ROT_VEL()
    ANIMATION_TIME_c = ANIMATION_TIME()

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.vel = 0
        self.tick_count = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d>= 16:
            d = 16
        
        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < MAX_ROTATION():
                self.tilt = MAX_ROTATION()
        else:
            if self.tilt > -90:
                self.tilt -= ROT_VEL()
        
    def draw(self, win):
        self.img_count += 1
        self.img = self.IMGS[0]
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP_c = GAP()
    PVEL_c = PVEL()

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + GAP()

    def move(self):
        self.x -= PVEL()
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False
        

class Base:
    BVEL_c = BVEL()
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= BVEL()
        self.x2 -= BVEL()

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score, gen):
    
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_Width() - 10 - text.get_width(), 10))
    
    text = STAT_FONT.render("Gen: " + str(gen), 1, (255,255,255))
    win.blit(text, (10, 10))


    base.draw(win)

    for bird in birds:
        bird.draw(win)

    pygame.display.update()

def main(genomes, config):
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_Width(),WIN_Height()))
    clock = pygame.time.Clock()
    score = 0
    
    run = True
    while run:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break
        
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
        
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        # bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
                
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            

            pipe.move()


        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))
        
        for r in rem:
            pipes.remove(r)
        
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)


        base.move()
        draw_window(win, birds, pipes, base, score, GEN)

        if score > 5:
            pickle.dump(nets[0],open("best.pickle", "wb"))
            run = False
            break



def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,1)

    # print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)