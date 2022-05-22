import random

import pygame
import sys

# Inicialização
pygame.init()

# Configurando a janela
screenWidth = 1280
screenHeight = 960
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Pong')


#Classes



class Entity:
    def __init__(self):
        self.physics = PhysicsComponent()
        self.graphics = GraphicsComponent()

    def update(self, world, dt):
        pass

    def draw(self, dt):
        pass


class Component():
    def __init__(self, parent):
        self.parent = parent


class PhysicsComponent(Component):
    def update(self, world, dt):
        pass


class GraphicsComponent(Component):
    def draw(self, dt):
        pass


class World(Entity):
    def __init__(self) -> None:
        self.physics_entities = []
        self.singleton_entities = []
        self.ball = Ball()
        self.player = Player(self.ball)
        self.opponent = Opponent(self.ball)
        self.judge = Judge()

        self.physics_entities.append(self.ball)
        self.physics_entities.append(self.player)
        self.physics_entities.append(self.opponent)
        self.singleton_entities.append(self.judge)

    def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, dt):
        for e in self.physics_entities:
            e.update(self, dt)

    def draw(self, dt):
        screen.fill((0, 0, 0))
        for e in self.singleton_entities:
            e.draw(dt)
        for e in self.physics_entities:
            e.draw(dt)
        # Atualizando a janela 60fps
        pygame.display.flip()


class Ball(Entity):
    def __init__(self):
        self.body = pygame.Rect(screenWidth / 2 - 15, screenHeight / 2 - 15, 30, 30)
        self.speedX = 0.4
        self.speedY = 0.4

        self.physics = BallPhysicsComponent(self)
        self.graphics = BallGraphicsComponent(self)

    def update(self, world, dt):
        self.physics.update(world, dt)
    
    def draw(self, dt):
        self.graphics.draw(dt)
            
    def resetBall(self):
        self.body.center = (screenWidth / 2, screenHeight / 2)
        self.speedX = random.choice((-0.5, 0.5))

    def change_course(self, dt):
        self.speedY = dt * 0.01
        self.speedX *= -1


class BallPhysicsComponent(PhysicsComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.body = parent.body

    def update(self, world, dt):
        self.body.x = self.body.x + self.parent.speedX * dt
        self.body.y = self.body.y + self.parent.speedY * dt
        if self.body.top <= 0 or self.body.bottom >= screenHeight:
            self.parent.speedY = -self.parent.speedY
        if self.body.left > screenWidth or self.body.right < 0:
            for e in world.singleton_entities:
                if(self.body.left > screenWidth):
                    e.change_score(False)
                elif(self.body.right < 0):
                    e.change_score(True)
            self.parent.resetBall()



class BallGraphicsComponent(GraphicsComponent):   
    def draw(self, dt):
        pygame.draw.ellipse(screen, (200, 200, 200), self.parent.body)


class Player(Entity):
    def __init__(self, ball):
        self.body = pygame.Rect(screenWidth - 20, screenHeight / 2 - 70, 10, 140)
        self.score = 0

        self.physics = PlayerPhysicsComponent(self)
        self.graphics = PlayerGraphicsComponent(self)

    def update(self, world, dt):
        self.physics.update(world, dt)

    def draw(self, dt):
        self.graphics.draw(dt)


class PlayerPhysicsComponent(PhysicsComponent):
    def __init__(self, parent):
        self.parent = parent
        self.body = parent.body

    def update(self, world, dt):
        for e in world.physics_entities:
            if e == self.parent: 
                continue
            if e.body.bottom >= self.body.top and e.body.top <= self.body.bottom and e.body.right >= self.body.left:
                delta = e.body.centery - self.body.centery
                e.change_course(delta)
        (x, y) = pygame.mouse.get_pos()
        self.body.y = y - 70


class PlayerGraphicsComponent(GraphicsComponent):
    def draw(self, dt):
        pygame.draw.rect(screen, (200, 200, 200), self.parent.body)


class Opponent(Entity):
    def __init__(self, ball):
        self.body = pygame.Rect(10, screenHeight / 2 - 70, 10, 140)
        self.speed = 8
        self.score = 0

        self._ball = ball
        self.physics = OpponentPhysicsComponent(self)
        self.graphics = OpponentGraphicsComponent(self)

    def update(self, world, dt):
        self.physics.update(world, dt)

    def draw(self, dt):
        self.graphics.draw(dt)


class OpponentPhysicsComponent(PhysicsComponent):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.body = parent.body
        self._ball = parent._ball
        self.speed = parent.speed

    def update(self, world, dt):
        if self.body.bottom < self._ball.body.y:
            self.body.bottom += self.speed
        if self.body.top > self._ball.body.y:
            self.body.top -= self.speed
            
        for e in world.physics_entities:
            if e == self.parent: 
                continue
            if e.body.bottom >= self.body.top and e.body.top <= self.body.bottom and e.body.left <= self.body.right:
                delta = e.body.centery - self.body.centery
                e.change_course(delta)


class OpponentGraphicsComponent(GraphicsComponent):
    def draw(self, dt):
        pygame.draw.rect(screen, (200, 200, 200), self.parent.body)


class Judge(Entity):
    def __init__(self):
        self.player_score = 0
        self.opponent_score = 0

        self.player_score_text = ScoreTextGraphicsComponent(self, True, (screenWidth / 2 + 120, 200))
        self.opponent_score_text = ScoreTextGraphicsComponent(self, False, (screenWidth / 2 - 120, 200))
    
    def draw(self, dt):
        self.player_score_text.draw(dt)
        self.opponent_score_text.draw(dt)

    def change_score(self, is_player):
        if is_player:
            self.player_score += 1
            self.player_score_text.change_score()
        elif not is_player:
            self.opponent_score += 1
            self.opponent_score_text.change_score()


class ScoreTextGraphicsComponent(GraphicsComponent):
    def __init__(self, parent, is_player,coord):
        super().__init__(parent)
        self.coord = coord
        self.font = pygame.font.SysFont('arial', 32)
        self.is_player = is_player
        self.text = self.font.render("0", True, pygame.Color(255, 255, 255))

    def change_score(self):
        if self.is_player:
            self.text = self.font.render(str(self.parent.player_score), True, pygame.Color(255, 255, 255))
        elif not self.is_player:
            self.text = self.font.render(str(self.parent.opponent_score), True, pygame.Color(255, 255, 255))

    def draw(self, dt):
        screen.blit(self.text, self.coord)


#Objetos
world = World()
previous = pygame.time.get_ticks()
lag = 0
FPS = 60
MS_PER_UPDATE = 1000 / FPS
while True:
    current = pygame.time.get_ticks()
    elapsed = current - previous
    previous = current
    lag += elapsed
    # Entradas
    world.inputs()
    # Atualização
    while lag >= MS_PER_UPDATE:
        # Atualização
        world.update(MS_PER_UPDATE)
        lag -= MS_PER_UPDATE
    # Desenho
    world.draw(MS_PER_UPDATE)