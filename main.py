from cgitb import reset
from pickletools import float8, long1
import random
from tokenize import Double
import pygame
import sys

# Inicialização
pygame.init()
clock = pygame.time.Clock()
# Configurando a janela
screenWidth = 1280
screenHeight = 960
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Pong')
# Objetos
ball = pygame.Rect(screenWidth / 2 - 15, screenHeight / 2 - 15, 30, 30)
player = pygame.Rect(screenWidth - 20, screenHeight / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screenHeight / 2 - 70, 10, 140)
# variaveis
ballSpeedX = 0.5  # 500 pixels por segundo
ballSpeedY = 0.5
opponentSpeed = 10


def inputs():
    global gameStarted
    # Processando as entradas (eventos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            gameStarted = True
    (x, y) = pygame.mouse.get_pos()
    player.y = y - 70


def draw():
    global font, player1Point, player2Point, gameStarted, gameEnded
    
    # Desenho
    if(gameStarted and not gameEnded):
        screen.fill((0, 0, 0))
        pygame.draw.ellipse(screen, (200, 200, 200), ball)
        pygame.draw.rect(screen, (200, 200, 200), player)
        pygame.draw.rect(screen, (200, 200, 200), opponent)
        point1 = font.render(str(player1Point), True, pygame.Color(255, 255, 255))
        point2 = font.render(str(player2Point), True, pygame.Color(255, 255, 255))
        screen.blit(point1, (screenWidth / 2 - 100, 100))
        screen.blit(point2, (screenWidth / 2 + 100, 100))
        # Atualizando a janela 60fps
        pygame.display.flip()

    if(gameEnded):
        screen.fill((0, 0, 0))
        gameOver = font.render("Game Over", True, pygame.Color(255, 255, 255))
        screen.blit(gameOver, (screenWidth / 2 - (gameOver.get_width() / 2), screenHeight / 2 - (gameOver.get_height() / 2)))
        pygame.display.flip()

    elif(not gameStarted):
        screen.fill((0, 0, 0))
        pong = font.render("Pong", True, pygame.Color(255, 255, 255))
        start = font.render("Clique com o mouse para iniciar", True, pygame.Color(255, 255, 255))
        screen.blit(pong, (screenWidth / 2 - (pong.get_width() / 2), screenHeight / 2 - 200))
        screen.blit(start, (screenWidth / 2 - (start.get_width() / 2), screenHeight / 2))
        pygame.display.flip()


def resetBall():
    global ballSpeedX, ballSpeedY

    ball.center = (screenWidth / 2, screenHeight / 2)
    ballSpeedX = random.choice((-0.5, 0.5))


def update(dt):
    global ballSpeedX, ballSpeedY, player1Point, player2Point, gameStarted, gameEnded, calc

    # Atualização
    if(gameStarted and not gameEnded):
        ball.x += ballSpeedX * dt
        ball.y += ballSpeedY * dt
        if opponent.bottom < ball.y:
            opponent.bottom += opponentSpeed
        if opponent.top > ball.y:
            opponent.top -= opponentSpeed

        if (ball.y <= 0 or ball.bottom >= screenHeight):
            ballSpeedY *= -1
            print(ballSpeedY)
        
        if ball.bottom >= opponent.top and ball.top <= opponent.bottom and ball.left <= opponent.right:
            delta = ball.centery - opponent.centery
            ballSpeedY = delta * 0.01
            if ballSpeedY < 0 and ballSpeedY * dt < -1:
                ballSpeedY = -1 / dt
            elif ballSpeedY > 0 and ballSpeedY * dt < 1:
                ballSpeedY = 1 / dt
            ballSpeedX *= -1
        elif ball.bottom >= player.top and ball.top <= player.bottom and ball.right >= player.left:
            delta = ball.centery - player.centery
            ballSpeedY = delta * 0.01
            if ballSpeedY < 0 and ballSpeedY * dt > -1:
                ballSpeedY = -1 / dt
            elif ballSpeedY > 0 and ballSpeedY * dt < 1:
                ballSpeedY = 1 / dt
            ballSpeedX *= -1

        if ball.left >= screenWidth:
            player1Point += 1
            if(player1Point < 5):
                resetBall()
            elif(player1Point >= 5):
                gameEnded = True
        elif ball.right <= 0:
            player2Point +=1
            if(player2Point < 5):
                resetBall()
            elif(player2Point >= 5):
                gameEnded = True    


previous = pygame.time.get_ticks()
lag = 0
FPS = 500
MS_PER_UPDATE = 1000/FPS
player1Point = 0
player2Point = 0
gameStarted = False
gameEnded = False
calc = 0
font = pygame.font.SysFont('arial', 32)

while True:
    current = pygame.time.get_ticks()
    elapsed = current - previous
    previous = current
    lag += elapsed

    #Entradas
    inputs()
    while lag >= MS_PER_UPDATE:
        # Atualização
        update(MS_PER_UPDATE)
        lag -= MS_PER_UPDATE
    #Desenho
    draw()