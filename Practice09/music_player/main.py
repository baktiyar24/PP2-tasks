import pygame
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800,600))
font = pygame.font.Font(None, 30)
text = font.render("P = Play | S = Stop | N = Next track | B = Previous (Back) | Q = Quit", True, (0,0,0))
pygame.display.set_caption("Player Pygame")



playlist = [
    "Practice09/music_player/music/song1.mp3",
    "Practice09/music_player/music/song2.mp3",
    "Practice09/music_player/music/song3.mp3"
]
current_track = 0

running = True

while running:

    screen.fill((255,255,255))
    screen.blit(text, (70,250))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
                pygame.quit()
            elif event.key == pygame.K_p:
                pygame.mixer.music.load(playlist[current_track])
                pygame.mixer.music.play()
            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
            elif event.key == pygame.K_n:
                current_track += 1
                if current_track >= len(playlist):
                    current_track = 0
                pygame.mixer.music.load(playlist[current_track])
                pygame.mixer.music.play()
            elif event.key == pygame.K_b:
                current_track -= 1
                if current_track >= len(playlist):
                    current_track = 0
                pygame.mixer.music.load(playlist[current_track])
                pygame.mixer.music.play()
                
                

                



        