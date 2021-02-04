import pygame
import random
import time


pygame.init()

pause = True

flap = pygame.mixer.Sound("swoosh.mp3")
pygame.mixer.Sound.set_volume(flap, 0.2)

# Dimensions
display_width = 1840
display_height = 980
bird_height = 46

# Gravity
gravity = 0.34


#setting up game display
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Flappy Bird")
screen_rect = gameDisplay.get_rect()

icon = pygame.image.load('C:\\Users\\gubai\\pythoncodes\\FlappyBird\\bird.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

#colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)



# loading assets
pipesImg = pygame.image.load('newpipe.png')
birdImg = pygame.image.load('bird.png')
background = pygame.image.load('background.png')
rect = background.get_rect()
pipe_surface = pipesImg


#creating a user event SPAWNPIPE
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 2000)
pipe_height = [400,600,800]

# giving bird image a rect
bird_surface = birdImg
bird_rect = bird_surface.get_rect(center = (200,490))



# Bliting pipes and the bird
def pipes(x,y):
    gameDisplay.blit(pipesImg, (x, y))

def bird(x,y):
    new_bird = pygame.transform.rotozoom(birdImg, -y_change * 1.3, 1)
    gameDisplay.blit(new_bird, bird_rect)


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()



# This block draws the buttons and enables user to click them
def button(msg, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()


    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x +(w/2)), (y + (h/2)) )
    gameDisplay.blit(textSurf, textRect)


# these two functions are directly connected to the paused() function
def quitgame():
    pygame.quit()
    quit()


def unpause():
    global pause
    pause = False
    pygame.mixer.music.unpause()

# pause function
def paused():

    pygame.mixer.music.pause()

    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2.1), (display_height/3))
    gameDisplay.blit(TextSurf, TextRect)


    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        button("Continue",500, 450, 350, 180, green, bright_green, unpause)
        button("QUIT",921, 450, 350, 180, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


# giving our pipe image a rect
def create_pipe():
    x_pipe = 920
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (x_pipe, random_pipe_pos))
    top_pipe =  pipe_surface.get_rect(midbottom = (x_pipe, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

# separating pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 7
    return pipes

# Bliting pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 980:
            gameDisplay.blit(pipe_surface, pipe)
        else:
            fliped_pipe = pygame.transform.flip(pipe_surface, False, True)
            gameDisplay.blit(fliped_pipe, pipe)




# When bird_rect collides with pipe_rect execute crash() function
def collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            game_loop()



def game_intro():

    intro = True


    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Setting up font and positioning buttons that will be displayed at the start
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("Flappy bird", largeText)
        TextRect.center = ((display_width/2.1), (display_height/3.9))
        gameDisplay.blit(background, (0,0))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!",500, 450, 350, 180, green, bright_green, game_loop)
        button("QUIT",921, 450, 350, 180, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)

#______________
best_score = []

# Block responsible for our score
def things_dodged(count):
    font = pygame.font.SysFont(None, 40)
    text = font.render("Score: " + str(int(count)), True, white)
    bestS = font.render("Best: " + str(int(max(best_score))), True, white)
    gameDisplay.blit(text, (0, 0))
    gameDisplay.blit(bestS, (150, 0))



# Main game loop
def game_loop():

    global pause

    gameExit = False

    pipe_list = []

    x = (display_width * 0.1)
    y = (display_height * 0.4)


    dodged = 0

    global y_change
    y_change = 0

    while not gameExit:



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(flap)
                    y_change = -27
                if event.key == pygame.K_p:
                    pause = True
                    paused()


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    y_change = 0

            if event.type == SPAWNPIPE:
                pipe_list.extend(create_pipe())

            # if bird_rect.top <= -100 or bird_rect.bottom >= 1000 - bird_height:
            #     gameExit = True
            #     game_loop()

            bird_rect.clamp_ip(screen_rect)
            collision(pipe_list)

        gameDisplay.blit(background, (0,0))


        y_change += gravity
        bird_rect.centery += y_change

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        dodged += 0.01
        best_score.append(dodged)
        things_dodged(dodged)


        collision(pipe_list)
        bird(x,y)
        pygame.display.update()
        clock.tick(68.5)



game_intro()
game_loop()
pygame.quit()
quit()




