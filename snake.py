'''
The game snake in python
Author: Conor Stripling
'''

import pygame
import random


class Cube:
    def __init__(self, x, y, top, left):
        self.x = x
        self.y = y
        self.top = top
        self.left = left
        self.color = pygame.color.Color("blue")

    def setColor(self, color):
        # color is a string
        self.color = pygame.color.Color(color)

    def moveCube(self, direction):
        if direction == "UP":
            self.top -= 10
        elif direction == "DOWN":
            self.top += 10
        elif direction == "LEFT":
            self.left -= 10
        elif direction == "RIGHT":
            self.left += 10


class FoodCube(Cube):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 0)
        self.top = random.randint(0, 20) * 10
        self.left = random.randint(0, 20) * 10
        self.color = pygame.color.Color("black")


class Snake:
    def __init__(self):
        self.head = Cube(10, 10, 200, 200)
        self.body = [self.head, Cube(10, 10, 200, 190), Cube(10, 10, 200, 180), Cube(10, 10, 200, 170),
                     Cube(10, 10, 200, 160)]
        self.position = [self.head.left, self.head.top]
        self.direction = "RIGHT"

    def changeDirection(self, direction):
        if direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"
        elif direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        if direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"

    def move(self):
        if self.direction == "UP":
            self.position[1] -= 10
        elif self.direction == "DOWN":
            self.position[1] += 10
        elif self.direction == "LEFT":
            self.position[0] -= 10
        elif self.direction == "RIGHT":
            self.position[0] += 10
        self.body.insert(0, Cube(10, 10, self.position[1], self.position[0]))
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
        self.body.insert(0, Cube(10, 10, self.position[1], self.position[0]))


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
            pygame.draw.rect(self.dis, (i.color.r, i.color.g, i.color.b), (i.left, i.top, i.x, i.y))

    def drawCube(self, cube_object):
        pygame.draw.rect(self.dis, (cube_object.color.r, cube_object.color.g, cube_object.color.b),
                         (cube_object.left, cube_object.top, cube_object.x, cube_object.y))

    def hasFood(self):
        if self.food is None:
            return False
        return True

    def onFoodBlock(self, snake):
        if snake.head.top == self.food.top and snake.head.left == self.food.left:
            return True
        return False

    def runGame(self):
        if self.dis is None:
            self.createDisplay()
        s = Snake()
        self.drawSnake(s)
        pygame.display.update()

        while not self.game_over:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        s.changeDirection("LEFT")
                    if event.key == pygame.K_RIGHT:
                        s.changeDirection("RIGHT")
                    if event.key == pygame.K_UP:
                        s.changeDirection("UP")
                    if event.key == pygame.K_DOWN:
                        s.changeDirection("DOWN")
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
                self.food = FoodCube(10, 10)
            self.drawCube(self.food)
            if self.onFoodBlock(s):
                self.food = None
                s.growSnake()
            pygame.display.update()
            pygame.time.Clock().tick(15)

        pygame.quit()
        quit()


def main():
    g = Game()
    g.runGame()


if __name__ == '__main__':
    main()
