import pygame
pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((800,600))
running = True
clock = pygame.time.Clock()

# Car
car = pygame.image.load("Practice10/Racer/images/car.png").convert_alpha()
car = pygame.transform.scale(car, (120,150))
car_x = 335
car_y = 400
car_speed = 4

# Background
bg = pygame.image.load("Practice10/Racer/images/background.png").convert_alpha()
bg = pygame.transform.scale(bg, screen.get_size())
bg_sound = pygame.mixer.Sound("Practice10/Racer/music,sounds/bg_sound.mp3")
bg_sound.play()
bg_y = 0

# Enemy
enemy = pygame.image.load("Practice10/Racer/images/enemy.png").convert_alpha()
enemy = pygame.transform.scale(enemy, (120,150))



while running:

    screen.blit(bg, (0, bg_y))
    screen.blit(bg, (0, bg_y - 600))
    screen.blit(car, (car_x, car_y))
    screen.blit(enemy, (0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 150:
        car_x -= car_speed
    elif keys[pygame.K_RIGHT] and car_x < 525:
        car_x += car_speed
    elif keys[pygame.K_UP] and car_y > 50:
        car_y -= car_speed
    elif keys[pygame.K_DOWN] and car_y < 450:
        car_y += car_speed
    



    bg_y += 2
    if bg_y == 600:
        bg_y = 0

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    clock.tick(120)
    

pygame.quit()