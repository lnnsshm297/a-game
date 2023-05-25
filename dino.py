import pygame
import random


pygame.init()


width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dinosaur Game")

clock = pygame.time.Clock()


dinosaur_img = pygame.Surface((40, 40))  
dinosaur_img.fill((255, 0, 0))  


dinosaur_x = width // 2 - dinosaur_img.get_width() // 2
dinosaur_y = height - dinosaur_img.get_height() - 10


cactus_img = pygame.Surface((20, 40))  
cactus_img.fill((0, 255, 0))  


cacti = []

def generate_cactus():
    cactus_height = random.randint(50, 150)
    cactus_x = width
    cactus_y = height - cactus_height - 10
    cacti.append((cactus_x, cactus_y))

ground_y = height - 10

def draw_ground():
    pygame.draw.line(screen, (0, 0, 0), (0, ground_y), (width, ground_y))

score = 0
high_score = 0

def update_score():
    global score, high_score
    score += 1
    if score > high_score:
        high_score = score

def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    high_score_text = font.render("High Score: " + str(high_score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))


game_over = False
end_time = 0

jumping = False
jump_count = 10

while not game_over:
    screen.fill((255, 255, 255))  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not jumping:
                    jumping = True

    
    if jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            dinosaur_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            jumping = False
            jump_count = 10

    
    for i in range(len(cacti)):
        cacti[i] = (cacti[i][0] - 2, cacti[i][1])

    
    if random.randint(0, 100) < 1:
        generate_cactus()

    
    for cactus in cacti:
        cactus_rect = pygame.Rect(cactus[0], cactus[1], cactus_img.get_width(), cactus_img.get_height())

        dinosaur_rect = pygame.Rect(dinosaur_x, dinosaur_y, dinosaur_img.get_width(), dinosaur_img.get_height())

        if dinosaur_rect.colliderect(cactus_rect):
            game_over = True
            end_time = pygame.time.get_ticks()

    
    screen.blit(dinosaur_img, (dinosaur_x, dinosaur_y))
    for cactus in cacti:
        screen.blit(cactus_img, cactus)
    draw_ground()
    draw_score()

    pygame.display.flip()
    clock.tick(30)  


while pygame.time.get_ticks() - end_time <= 60000:
    screen.fill((255, 255, 255))  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    font = pygame.font.Font(None, 48)
    game_over_text = font.render("Game Over", True, (0, 0, 0))
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 48))
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 + 48))

    pygame.display.flip()

pygame.quit()
