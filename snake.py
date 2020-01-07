"""
The game snake in python
Author: Conor Stripling
"""

import pygame
import random
from enum import Enum

CUBE_DIMENSION = 10


class Direction(Enum):
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4


class Square:

    def __init__(self, top, left):
        self.top = top
        self.left = left
        self.color = pygame.color.Color("blue")

    def setColor(self, color):
        self.color = pygame.color.Color(color)


class FoodSquare(Square):
    def __init__(self):
        super().__init__(0, 0)
        self.top = random.randint(0, 20) * 10
        self.left = random.randint(0, 20) * 10
        self.color = pygame.color.Color("black")


class Snake:
    def __init__(self):
        self.head = Square(200, 200)
        self.body = [self.head, Square(200, 190), Square(200, 180), Square(200, 170),
                     Square(200, 160)]
        self.position = {"left": self.head.left, "top": self.head.top}
        self.direction = Direction.RIGHT

    def changeDirection(self, dir_):
        if dir_ == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT
        elif dir_ == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif dir_ == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        if dir_ == Direction.DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN

    def move(self):
        if self.direction == Direction.UP:
            self.position["top"] -= 10
        elif self.direction == Direction.DOWN:
            self.position["top"] += 10
        elif self.direction == Direction.LEFT:
            self.position["left"] -= 10
        elif self.direction == Direction.RIGHT:
            self.position["left"] += 10
        self.body.insert(0, Square(self.position["top"], self.position["left"]))
        self.head = self.body[0]
        self.body.pop()

    def isCollision(self):
        if self.head.top == 400 or self.head.left == 400 or self.head.top == 0 or self.head.left == 0:
            return True
        for i in range(1, len(self.body)):
            if self.head.left == self.body[i].left and self.head.top == self.body[i].top:
                return True
        return False

    def growSnake(self):
        self.body.insert(0, Square(self.position["top"], self.position["left"]))


class Game:
    def __init__(self):
        self.food = None
        self.dis = None
        self.game_over = False

    def createDisplay(self):
        pygame.init()
        self.dis = pygame.display.set_mode((400, 400))
        pygame.display.update()
        pygame.display.set_caption("Snake Game")
        self.dis.fill((225, 225, 225))

    def drawSnake(self, snake):
        for i in snake.body:
            pygame.draw.rect(self.dis, (i.color.r, i.color.g, i.color.b),
                             (i.left, i.top, CUBE_DIMENSION, CUBE_DIMENSION))

    def drawCube(self, cube_object):
        pygame.draw.rect(self.dis, (cube_object.color.r, cube_object.color.g, cube_object.color.b),
                         (cube_object.left, cube_object.top, CUBE_DIMENSION, CUBE_DIMENSION))

    def hasFood(self):
        return self.food is not None

    def onFoodBlock(self, snake):
        return snake.head.top == self.food.top and snake.head.left == self.food.left

    def generateScore(self, score):
        score_font = pygame.font.SysFont("comicsansms", 20)
        yellow = pygame.color.Color("yellow")
        value = score_font.render("Your Score: {0}".format(str(score)), True, (
            yellow.r, yellow.g, yellow.b))
        self.dis.blit(value, [0, 0])

    def runGame(self):
        if self.dis is None:
            self.createDisplay()
        s = Snake()
        self.drawSnake(s)
        score = 0
        self.generateScore(score)
        pygame.display.update()
        while not self.game_over:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        s.changeDirection(Direction.LEFT)
                    if event.key == pygame.K_RIGHT:
                        s.changeDirection(Direction.RIGHT)
                    if event.key == pygame.K_UP:
                        s.changeDirection(Direction.UP)
                    if event.key == pygame.K_DOWN:
                        s.changeDirection(Direction.DOWN)
                    if event.key == pygame.K_ESCAPE:
                        self.game_over = True
                if event.type == pygame.QUIT:
                    self.game_over = False
            self.dis.fill((225, 225, 225))
            s.move()
            self.drawSnake(s)
            if s.isCollision():
                self.game_over = True
            if not self.hasFood():
                self.food = FoodSquare()
            self.drawCube(self.food)
            if self.onFoodBlock(s):
                self.food = None
                s.growSnake()
                score += 1
            self.generateScore(score)
            pygame.display.update()
            pygame.time.Clock().tick(15)

        pygame.quit()
        quit()


def main():
    g = Game()
    g.runGame()


if __name__ == '__main__':
    main()
