import pygame
import sys

pygame.init()

# ชื่อเกม
game_name = "tiger1"

# window
window = pygame.display.set_mode((999, 335))
pygame.display.set_caption(game_name)
icon = pygame.image.load("game image/t34.png")
pygame.display.set_icon(icon)

# พื้นหลัง
bg = pygame.image.load("game image/new_bg-H.png ")
floor = pygame.image.load("game image/newbg-L.png")

# player
player = pygame.image.load("game image/newtiger1.png")

# FPS
clock = pygame.time.Clock()
FPS = 60

# สี
white = (255, 255, 255)
green = (0, 160, 10)
bright_green = (14, 178, 0)
dark_gray = (169, 169, 169)
bright_gray = (192, 192, 192)

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(window, ic, (x, y, w, h))

    padx = x + (w / 2)
    pady = y + (h / 2)
    print_text(msg, 20, padx, pady)

def print_text(msg, size, x, y):
    font_text = pygame.font.Font("DM Taohu Regular.ttf", size)
    textsurf, textRect = text_objects(msg, font_text)
    textRect.center = (x, y)
    window.blit(textsurf, textRect)

def text_objects(text, font):
    textsurface = font.render(text, True, white)
    return textsurface, textsurface.get_rect()

def Quit_game():
    pygame.quit()
    sys.exit()

def intro():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Quit_game()

        # แบคกราว
        window.blit(bg, (0, 0))
        window.blit(floor, (0, 35))
        # ชื่อเกม
        print_text(game_name, 50, 200, 100)
        # ปุ่ม
        button("START", 800, 80, 150, 50, green, bright_green, mainloop)
        button("EXIT", 800, 160, 150, 50, green, bright_green, Quit_game)

        pygame.display.update()

def mainloop():

    global pause

    # ท้องฟ้า
    bgx = 0
    bgy = 0
    bg_move = 2.5
    # พื้นดิน
    floorx = 0
    floory = 35
    floormove = 5
    # ตัวละคร
    player_rect = player.get_rect(center=(200, 200))
    gravity = 0.25
    jump = 5
    playerjump = 0
    # ระยะทางที่ขับ
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Quit_game()

            if event.type == pygame.KEYDOWN:
                # กดกระโดด
                if event.key == pygame.K_w and player_rect.centery == 270:
                    playerjump = 0
                    playerjump -= jump

                # กดหยุดเกม
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    Paused()

        # เคลื่อนที่หน้า/หลัง
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and player_rect.centerx < 200:
            player_rect.centerx += floormove
        elif keys[pygame.K_d]:
            floorx -= floormove
            bgx -= bg_move
            score += 1

        if keys[pygame.K_a] and bgx < 0:
            floorx += floormove
            bgx += bg_move
            score -= 1
        elif keys[pygame.K_a] and player_rect.centerx > 0:
            player_rect.centerx -= floormove

        # แรงโน้มถ่วง/กระโดด
        playerjump += gravity
        player_rect.centery += playerjump
        if player_rect.centery > 270:
            player_rect.centery = 270

        # แสดงภาพ
        window.blit(bg, (bgx, bgy))
        window.blit(floor, (floorx, floory))
        window.blit(player, (player_rect))

        # ระยะทางที่ขับ
        distance = score / 10
        msg = "range " + str(distance)
        print_text(msg, 20, 100, 20)

        # ฉากจบเกม
        if distance > 979.7:
            endtro()

        clock.tick(FPS)
        pygame.display.update()

def Paused():
    # เรื่มหยุดเกม
    pygame.mixer.music.pause()
    print_text("Paused", 50, 200, 100)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Quit_game()

        button("BACK TO GAME", 800, 40, 150, 50, green, bright_green, unpause)
        button("RE TRY", 800, 120, 150, 50, green, bright_green, mainloop)
        button("EXIT", 800, 200, 150, 50, dark_gray, bright_gray, Quit_game)

        clock.tick(FPS)
        pygame.display.update()

def unpause():
    # เล่นเกมต่อ
    global pause
    pygame.mixer.music.unpause()
    pause = False

def endtro():
    # จบเกม
    print_text("you win", 50, 200, 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Quit_game()

        button("RE TRY", 800, 80, 150, 50, green, bright_green, mainloop)
        button("EXIT", 800, 160, 150, 50, dark_gray, bright_gray, Quit_game)

        clock.tick(FPS)
        pygame.display.update()

intro()
