import pygame
import sys
import random

pygame.init()

pygame.mixer.init()

pygame.mixer.music.load("../Sound/tacorain1.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# -----------------
# PLAYER STATS
# -----------------

playerstats = {
    "health": 30,
    "max_health": 30
}

# -----------------
# TACO IMAGE
# -----------------

taco_img = pygame.image.load(
    "../Images/Attacks/taco1.png"
).convert_alpha()

taco_img = pygame.transform.scale(
    taco_img, (70, 70)
)

# -----------------
# RAT POISON IMAGE
# -----------------

ratpoison_img = pygame.image.load(
    "../Images/Attacks/ratPoison1.png"
).convert_alpha()

ratpoison_img = pygame.transform.scale(
    ratpoison_img, (50, 50)
)

# -----------------
# PLAYER IMAGE
# -----------------

player_idleimg1 = pygame.image.load(
    "../Images/PlayerInBattle/idle1.png"
).convert_alpha()

player_idleimg1 = pygame.transform.scale(
    player_idleimg1, (50, 50)
)

player_rect = player_idleimg1.get_rect(center=(100, 100))

# -----------------
# TACOS
# -----------------

tacos = []

last_taco_spawn = pygame.time.get_ticks()

# -----------------
# RAT POISON
# -----------------

rat_poisons = []

last_ratpoison_spawn = pygame.time.get_ticks()

# -----------------
# MAIN GAME LOOP
# -----------------

while True:

    # -----------------
    # EVENTS
    # -----------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # -----------------
    # PLAYER MOVEMENT
    # -----------------

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player_rect.y -= 5

    if keys[pygame.K_s]:
        player_rect.y += 5

    if keys[pygame.K_a]:
        player_rect.x -= 5

    if keys[pygame.K_d]:
        player_rect.x += 5

    player_rect.clamp_ip(screen.get_rect())

    # -----------------
    # TIME
    # -----------------

    current_time = pygame.time.get_ticks()

    # -----------------
    # SPAWN TACOS
    # -----------------

    if current_time - last_taco_spawn >= 500:

        taco = pygame.Rect(
            random.randint(0, 760),
            random.randint(0, 560),
            40,
            40
        )

        taco_speed_x = random.choice([-4, -3, 3, 4])
        taco_speed_y = random.choice([-4, -3, 3, 4])

        tacos.append([
            taco,
            taco_speed_x,
            taco_speed_y,
            current_time
        ])

        last_taco_spawn = current_time

    # -----------------
    # SPAWN RAT POISON
    # -----------------

    if current_time - last_ratpoison_spawn >= 5000:

        rat_poison = pygame.Rect(
            random.randint(0, 750),
            random.randint(0, 550),
            50,
            50
        )

        # Random movement
        rat_speed_x = random.choice([-4, -3, 3, 4])
        rat_speed_y = random.choice([-4, -3, 3, 4])

        rat_poisons.append([
            rat_poison,
            rat_speed_x,
            rat_speed_y,
            current_time
        ])

        last_ratpoison_spawn = current_time

    # -----------------
    # MOVE TACOS
    # -----------------

    for taco in tacos[:]:

        taco_rect = taco[0]

        taco_rect.x += taco[1]

        if taco_rect.left <= 0:
            taco_rect.left = 0
            taco[1] *= -1

        if taco_rect.right >= 800:
            taco_rect.right = 800
            taco[1] *= -1

        taco_rect.y += taco[2]

        if taco_rect.top <= 0:
            taco_rect.top = 0
            taco[2] *= -1

        if taco_rect.bottom >= 600:
            taco_rect.bottom = 600
            taco[2] *= -1

        # Taco hits player
        if taco_rect.colliderect(player_rect):

            playerstats["health"] -= 5

            tacos.remove(taco)

            print("Health:", playerstats["health"])

        # Taco expires after 5 seconds
        elif current_time - taco[3] >= 5000:

            tacos.remove(taco)

    # -----------------
    # MOVE RAT POISON
    # -----------------

    for rat_poison in rat_poisons[:]:

        rat_rect = rat_poison[0]

        # Random movement
        rat_rect.x += rat_poison[1]
        rat_rect.y += rat_poison[2]

        # Bounce left/right
        if rat_rect.left <= 0:
            rat_rect.left = 0
            rat_poison[1] *= -1

        if rat_rect.right >= 800:
            rat_rect.right = 800
            rat_poison[1] *= -1

        # Bounce top/bottom
        if rat_rect.top <= 0:
            rat_rect.top = 0
            rat_poison[2] *= -1

        if rat_rect.bottom >= 600:
            rat_rect.bottom = 600
            rat_poison[2] *= -1

        # -----------------
        # COLLECT RAT POISON
        # -----------------

        if rat_rect.colliderect(player_rect):

            # Heal all the way to 30
            playerstats["health"] = playerstats["max_health"]

            rat_poisons.remove(rat_poison)

            print("RAT POISON COLLECTED!")
            print("Health:", playerstats["health"])

        # Rat poison expires after 5 seconds
        elif current_time - rat_poison[3] >= 5000:

            rat_poisons.remove(rat_poison)

    # -----------------
    # PLAYER DIED
    # -----------------

    if playerstats["health"] <= 0:

        print("You died. welcome back to life anyways")

        playerstats["health"] = 5

        print("Health:", playerstats["health"])

    # -----------------
    # DRAW
    # -----------------

    screen.fill((0, 0, 0))

    # Draw tacos
    for taco in tacos:
        screen.blit(taco_img, taco[0])

    # Draw rat poison
    for rat_poison in rat_poisons:
        screen.blit(ratpoison_img, rat_poison[0])

    # Draw player
    screen.blit(player_idleimg1, player_rect)

    # -----------------
    # UPDATE SCREEN
    # -----------------

    pygame.display.flip()

    clock.tick(60)
