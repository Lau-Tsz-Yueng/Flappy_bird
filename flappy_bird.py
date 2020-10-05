import sys
import pygame
import random


class Bird(object):
    def __init__(self):
        self.birdRect = pygame.Rect(65, 50, 50, 50)
        self.birdStatus = [pygame.image.load("bird0_0.png")
                          ,pygame.image.load("bird0_1.png")
                          ,pygame.image.load("bird0_2.png")]
        self.status = 0
        self.birdX = 120
        self.birdY = 350
        self.jump = False
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False

    def bird_update(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
        else:
            self.gravity += 0.2
            self.birdY += self.gravity
        self.birdRect[1] = self.birdY


class Pipeline(object):
    def __init__(self):
        self.wall_x = random.randint(400, 600)
        self.pineUp = pygame.image.load("pipe_down.png")
        self.pineDown = pygame.image.load("pipe_up.png")

    def update_pipeline(self):
        self.wall_x -= 5
        if self.wall_x < -80:
            global score
            score += 1
            self.wall_x = random.randint(400, 600)


def create_map():
    screen.fill(color)
    screen.blit(background, (0, 0))

    screen.blit(Pipeline.pineUp, (Pipeline.wall_x, -300))
    screen.blit(Pipeline.pineDown, (Pipeline.wall_x, 500))
    Pipeline.update_pipeline()

    if Bird.dead:
        Bird.status = 2
    elif Bird.jump:
        Bird.status = 1
    screen.blit(Bird.birdStatus[Bird.status], (Bird.birdX, Bird.birdY))
    Bird.bird_update()
    screen.blit(font.render(str(score), -1, (255, 255, 255)), (200, 50))
    pygame.display.update()


def check_dead():
    up_rect = pygame.Rect(Pipeline.wall_x , -300, Pipeline.pineUp.get_width() - 10, Pipeline.pineUp.get_height())
    down_rect = pygame.Rect(Pipeline.wall_x, 500, Pipeline.pineUp.get_width() - 10, Pipeline.pineUp.get_height())

    if up_rect.colliderect(Bird.birdRect) or down_rect.colliderect(Bird.birdRect):
        Bird.dead = True

    if not 0 < Bird.birdRect[1] < height:
        Bird.dead = True
        return True
    else:
        return False


def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
            return True


def get_result():
    text1 = "Game Over"
    text2 = "Your final score is:  " + str(score)
    font_1 = pygame.font.SysFont("Arial", 70)
    surf_1 = font.render(text1, 1, (242, 3, 36))
    font_2 = pygame.font.SysFont("Arial", 50)
    surf_2 = font.render(text2, 1, (253, 177, 6))

    screen.blit(surf_1, [screen.get_width()/2 - surf_1.get_width()/2, 100])
    screen.blit(surf_2, [screen.get_width() / 2 - surf_2.get_width() / 2, 200])
    pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont(None, 50)
    size = width, height = 400, 720
    screen = pygame.display.set_mode(size)
    color = (0, 0, 0)
    black = (255, 255, 255)
    speed = [5, 5]
    score = 0

    clock = pygame.time.Clock()
    Pipeline = Pipeline()
    Bird = Bird()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not Bird.dead:
            Bird.jump = True
            Bird.gravity = 5
            Bird.jumpSpeed = 10

    background = pygame.image.load("background.jpg")

    if check_dead():
        get_result()
    else:
        create_map()

pygame.quit()
