import random
import pygame
import sys

red = (0xFF, 0x00, 0x00, 0x01)
green = (0x00, 0xFF, 0x00, 0x01)
blue = (0x00, 0x00, 0xFF, 0x01)
lightBlue = (0x03, 0xFC, 0xF8)
gray = (0x96, 0x96, 0x96)
darkGray = (0x36, 0x36, 0x36)
yellow = (0xFC, 0xD7, 0x03)
white = (0xFF, 0xFF, 0xFF)
black = (0x00, 0x00, 0x00)

targets = [None]
targetsRot = [None]

boardHeight = 10
boardLength = 10
sizeOfCell = 50

playerHits = 0
botHits = 0
botRetries = 0

boards = [[[0 for x in range(10)] for y in range(10)] for z in range(4)]
# numbers depict the state of the cell 0 - unoccupied (no miss), 1 - miss, 2 - hit, 3 - ship (ally),

alreadyShot = []

shipsNotPlaced = [None, 1, 2, 1, 2, 4]
shipToPlace = 0
# 0 - no ship selected; 1 - carrier (5); 2 - Battleships (4); 3 - Cruiser (3); 3 - Submarine (3); Destroyer (2)
shipRotation = 0
# 0 - vertical; 1 - horizontal

playersTurn = True
inWar = True
setupGoing = True
endGame = True

pygame.init()
clock = pygame.time.Clock()
clock.tick(3)
screenWidth = sizeOfCell * boardLength * 2 + 2 * sizeOfCell
screenHeight = sizeOfCell * boardHeight
dispScreen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Battleships")
dispScreen.fill(white)
pygame.display.update()


def drawTable(x, y, n):
    for i in range(boardHeight):
        for j in range(boardLength):
            cell = boards[n][i][j]
            posOfCell = (x + i * sizeOfCell, y + j * sizeOfCell, 50, 50)
            if cell == 0:
                pygame.draw.rect(dispScreen, blue, posOfCell)
            elif cell == 1:
                pygame.draw.rect(dispScreen, lightBlue, posOfCell)
            elif cell == 2:
                pygame.draw.rect(dispScreen, red, posOfCell)
            elif cell == 3:
                pygame.draw.rect(dispScreen, darkGray, posOfCell)
    for i in range(boardHeight + 1):
        pygame.draw.line(dispScreen, gray, (x + i * sizeOfCell, y), (x + i * sizeOfCell, boardLength * sizeOfCell))
    for i in range(boardLength + 1):
        pygame.draw.line(dispScreen, gray, (x, y + i * sizeOfCell), (x + boardLength * sizeOfCell, y + i * sizeOfCell))


def botSetup(n):
    rot = round(random.random())
    if rot == 1:
        x = int(8 - random.random() * 6)
        y = int(random.random() * 10)
        boards[n][x - 2][y] = 3
        boards[n][x - 1][y] = 3
        boards[n][x + 0][y] = 3
        boards[n][x + 1][y] = 3
        boards[n][x + 2][y] = 3
    elif rot == 0:
        y = int(8 - random.random() * 6)
        x = int(random.random() * 10)
        boards[n][x][y - 2] = 3
        boards[n][x][y - 1] = 3
        boards[n][x][y + 0] = 3
        boards[n][x][y + 1] = 3
        boards[n][x][y + 2] = 3

    battleships = 2
    while battleships != 0:
        x = 0
        y = 0
        rot = round(random.random())
        if rot == 1:
            x = int(8 - random.random() * 7)
            y = int(random.random() * 10)
            if boards[n][x - 1][y] == 0 and boards[n][x + 0][y] == 0 and boards[n][x + 1][y] == 0 and boards[n][x + 2][
                y] == 0:
                boards[n][x - 1][y] = 3
                boards[n][x + 0][y] = 3
                boards[n][x + 1][y] = 3
                boards[n][x + 2][y] = 3
                battleships -= 1
        elif rot == 0:
            y = int(8 - random.random() * 7)
            x = int(random.random() * 10)
            if boards[n][x][y - 1] == 0 and boards[n][x][y + 0] == 0 and boards[n][x][y + 1] == 0 and boards[n][x][
                y + 2] == 0:
                boards[n][x][y - 1] = 3
                boards[n][x][y + 0] = 3
                boards[n][x][y + 1] = 3
                boards[n][x][y + 2] = 3
                battleships -= 1

    cruisers = 1
    while cruisers != 0:
        x = 0
        y = 0
        rot = round(random.random())
        if rot == 1:
            x = int(9 - random.random() * 8)
            y = int(random.random() * 10)
            if boards[n][x - 1][y] == 0 and boards[n][x + 0][y] == 0 and boards[n][x + 1][y] == 0:
                boards[n][x - 1][y] = 3
                boards[n][x + 0][y] = 3
                boards[n][x + 1][y] = 3
                cruisers -= 1
        elif rot == 0:
            x = int(random.random() * 10)
            y = int(9 - random.random() * 8)
            if boards[n][x][y - 1] == 0 and boards[n][x][y + 0] == 0 and boards[n][x][y + 1] == 0:
                boards[n][x][y - 1] = 3
                boards[n][x][y + 0] = 3
                boards[n][x][y + 1] = 3
                cruisers -= 1

    submarines = 2
    while submarines != 0:
        x = 0
        y = 0
        rot = round(random.random())
        if rot == 1:
            x = int(9 - random.random() * 8)
            y = int(random.random() * 10)
            if boards[n][x - 1][y] == 0 and boards[n][x + 0][y] == 0 and boards[n][x + 1][y] == 0:
                boards[n][x - 1][y] = 3
                boards[n][x + 0][y] = 3
                boards[n][x + 1][y] = 3
                submarines -= 1
        elif rot == 0:
            x = int(random.random() * 10)
            y = int(9 - random.random() * 8)
            if boards[n][x][y - 1] == 0 and boards[n][x][y + 0] == 0 and boards[n][x][y + 1] == 0:
                boards[n][x][y - 1] = 3
                boards[n][x][y + 0] = 3
                boards[n][x][y + 1] = 3
                submarines -= 1

    patrolBoats = 4
    while patrolBoats != 0:
        x = 0
        y = 0
        rot = round(random.random())
        if rot == 1:
            x = int(9 - random.random() * 9)
            y = int(random.random() * 10)
            if boards[n][x + 0][y] == 0 and boards[n][x + 1][y] == 0:
                boards[n][x + 0][y] = 3
                boards[n][x + 1][y] = 3
                patrolBoats -= 1
        elif rot == 0:
            x = int(random.random() * 10)
            y = int(9 - random.random() * 9)
            if boards[n][x][y + 0] == 0 and boards[n][x][y + 1] == 0:
                boards[n][x][y + 0] = 3
                boards[n][x][y + 1] = 3
                patrolBoats -= 1


while setupGoing:
    drawTable(0, 0, 0)
    drawTable(sizeOfCell * 12, 0, 1)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if shipRotation == 0:
                    shipRotation = 1
                else:
                    shipRotation = 0
            elif event.key == pygame.K_1:
                if shipsNotPlaced[1] == 0:
                    pass
                else:
                    shipToPlace = 1
            elif event.key == pygame.K_2:
                if shipsNotPlaced[2] == 0:
                    pass
                else:
                    shipToPlace = 2
            elif event.key == pygame.K_3:
                if shipsNotPlaced[3] == 0:
                    pass
                else:
                    shipToPlace = 3
            elif event.key == pygame.K_4:
                if shipsNotPlaced[4] == 0:
                    pass
                else:
                    shipToPlace = 4
            elif event.key == pygame.K_5:
                if shipsNotPlaced[5] == 0:
                    pass
                else:
                    shipToPlace = 5

        elif event.type == pygame.QUIT:
            endGame = False
            inWar = False
            setupGoing = False
    if shipToPlace == 1:
        mousePos = pygame.mouse.get_pos()
        if shipRotation == 0:
            if 2 * sizeOfCell < mousePos[0] < (boardLength - 2) * sizeOfCell:
                sumOfCells = 0
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) - 2)][(int(mousePos[1] / sizeOfCell))]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) - 1)][(int(mousePos[1] / sizeOfCell))]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) + 0)][(int(mousePos[1] / sizeOfCell))]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) + 1)][(int(mousePos[1] / sizeOfCell))]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) + 2)][(int(mousePos[1] / sizeOfCell))]
                if sumOfCells != 0:
                    pygame.draw.rect(dispScreen, red, ((int(mousePos[0] / sizeOfCell) - 2) * sizeOfCell,
                                                       int(mousePos[1] / sizeOfCell) * sizeOfCell, 5 * sizeOfCell,
                                                       50))
                else:
                    pygame.draw.rect(dispScreen, green, ((int(mousePos[0] / sizeOfCell) - 2) * sizeOfCell,
                                                         int(mousePos[1] / sizeOfCell) * sizeOfCell, 5 * sizeOfCell,
                                                         50))
                    if pygame.mouse.get_pressed()[0]:
                        boards[0][(int(mousePos[0] / sizeOfCell) - 2)][(int(mousePos[1] / sizeOfCell))] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell) - 1)][(int(mousePos[1] / sizeOfCell))] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell) + 0)][(int(mousePos[1] / sizeOfCell))] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell) + 1)][(int(mousePos[1] / sizeOfCell))] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell) + 2)][(int(mousePos[1] / sizeOfCell))] = 3
                        shipToPlace = 0
                        shipRotation = 0
                        shipsNotPlaced[1] -= 1
        elif shipRotation == 1:
            if 2 * sizeOfCell < mousePos[1] < (boardHeight - 2) * sizeOfCell and mousePos[0] < boardLength * sizeOfCell:

                sumOfCells = 0
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) - 2)]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) - 1)]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 0)]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 1)]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 2)]
                if sumOfCells != 0:
                    pygame.draw.rect(dispScreen, red, ((int(mousePos[0] / sizeOfCell)) * sizeOfCell,
                                                       int((mousePos[1] / sizeOfCell) - 2) * sizeOfCell, 50,
                                                       5 * sizeOfCell))
                else:
                    pygame.draw.rect(dispScreen, green, ((int(mousePos[0] / sizeOfCell)) * sizeOfCell,
                                                         int((mousePos[1] / sizeOfCell) - 2) * sizeOfCell, 50,
                                                         5 * sizeOfCell))
                    if pygame.mouse.get_pressed()[0]:
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) - 2)] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) - 1)] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 0)] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 1)] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 2)] = 3
                        shipToPlace = 0
                        shipRotation = 0
                        shipsNotPlaced[1] -= 1

    if shipToPlace == 2:
        mousePos = pygame.mouse.get_pos()
        if shipRotation == 0:
            if 2 * sizeOfCell < mousePos[0] < (boardLength - 1) * sizeOfCell:
                sumOfCells = 0
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) - 2)][(int(mousePos[1] / sizeOfCell))]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) - 1)][(int(mousePos[1] / sizeOfCell))]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) + 0)][(int(mousePos[1] / sizeOfCell))]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) + 1)][(int(mousePos[1] / sizeOfCell))]
                if sumOfCells != 0:
                    pygame.draw.rect(dispScreen, red, ((int(mousePos[0] / sizeOfCell) - 2) * sizeOfCell,
                                                       int(mousePos[1] / sizeOfCell) * sizeOfCell, 4 * sizeOfCell,
                                                       50))
                else:
                    pygame.draw.rect(dispScreen, green, ((int(mousePos[0] / sizeOfCell) - 2) * sizeOfCell,
                                                         int(mousePos[1] / sizeOfCell) * sizeOfCell, 4 * sizeOfCell,
                                                         50))
                    if pygame.mouse.get_pressed()[0]:
                        boards[0][(int(mousePos[0] / sizeOfCell) - 2)][(int(mousePos[1] / sizeOfCell))] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell) - 1)][(int(mousePos[1] / sizeOfCell))] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell) + 0)][(int(mousePos[1] / sizeOfCell))] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell) + 1)][(int(mousePos[1] / sizeOfCell))] = 3
                        shipToPlace = 0
                        shipRotation = 0
                        shipsNotPlaced[2] -= 1
        if shipRotation == 1:
            if 2 * sizeOfCell < mousePos[1] < (boardHeight - 1) * sizeOfCell and mousePos[0] < boardLength * sizeOfCell:
                sumOfCells = 0
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) - 2)]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) - 1)]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 0)]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 1)]
                if sumOfCells != 0:
                    pygame.draw.rect(dispScreen, red, ((int(mousePos[0] / sizeOfCell)) * sizeOfCell,
                                                       int((mousePos[1] / sizeOfCell) - 2) * sizeOfCell, 50,
                                                       4 * sizeOfCell))
                else:
                    pygame.draw.rect(dispScreen, green, ((int(mousePos[0] / sizeOfCell)) * sizeOfCell,
                                                         int((mousePos[1] / sizeOfCell) - 2) * sizeOfCell, 50,
                                                         4 * sizeOfCell))
                    if pygame.mouse.get_pressed()[0]:
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) - 2)] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) - 1)] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 0)] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 1)] = 3
                        shipToPlace = 0
                        shipRotation = 0
                        shipsNotPlaced[2] -= 1

    if shipToPlace == 3:
        mousePos = pygame.mouse.get_pos()
        if shipRotation == 0:
            if 1 * sizeOfCell < mousePos[0] < (boardLength - 1) * sizeOfCell:
                sumOfCells = 0
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) - 1)][(int(mousePos[1] / sizeOfCell))]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) + 0)][(int(mousePos[1] / sizeOfCell))]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) + 1)][(int(mousePos[1] / sizeOfCell))]
                if sumOfCells != 0:
                    pygame.draw.rect(dispScreen, red, ((int(mousePos[0] / sizeOfCell) - 1) * sizeOfCell,
                                                       int(mousePos[1] / sizeOfCell) * sizeOfCell, 3 * sizeOfCell,
                                                       50))
                else:
                    pygame.draw.rect(dispScreen, green, ((int(mousePos[0] / sizeOfCell) - 1) * sizeOfCell,
                                                         int(mousePos[1] / sizeOfCell) * sizeOfCell, 3 * sizeOfCell,
                                                         50))
                    if pygame.mouse.get_pressed()[0]:
                        boards[0][(int(mousePos[0] / sizeOfCell) - 1)][(int(mousePos[1] / sizeOfCell))] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell) + 0)][(int(mousePos[1] / sizeOfCell))] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell) + 1)][(int(mousePos[1] / sizeOfCell))] = 3
                        shipToPlace = 0
                        shipRotation = 0
                        shipsNotPlaced[3] -= 1
        if shipRotation == 1:
            if 1 * sizeOfCell < mousePos[1] < (boardHeight - 1) * sizeOfCell and mousePos[0] < boardLength * sizeOfCell:
                sumOfCells = 0
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) - 1)]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 0)]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 1)]
                if sumOfCells != 0:
                    pygame.draw.rect(dispScreen, red, ((int(mousePos[0] / sizeOfCell)) * sizeOfCell,
                                                       int((mousePos[1] / sizeOfCell) - 1) * sizeOfCell, 50,
                                                       3 * sizeOfCell))
                else:
                    pygame.draw.rect(dispScreen, green, ((int(mousePos[0] / sizeOfCell)) * sizeOfCell,
                                                         int((mousePos[1] / sizeOfCell) - 1) * sizeOfCell, 50,
                                                         3 * sizeOfCell))
                    if pygame.mouse.get_pressed()[0]:
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) - 1)] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 0)] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 1)] = 3
                        shipToPlace = 0
                        shipRotation = 0
                        shipsNotPlaced[3] -= 1

    if shipToPlace == 4:
        mousePos = pygame.mouse.get_pos()
        if shipRotation == 0:
            if 1 * sizeOfCell < mousePos[0] < (boardLength - 1) * sizeOfCell:
                sumOfCells = 0
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) - 1)][(int(mousePos[1] / sizeOfCell))]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) + 0)][(int(mousePos[1] / sizeOfCell))]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) + 1)][(int(mousePos[1] / sizeOfCell))]
                if sumOfCells != 0:
                    pygame.draw.rect(dispScreen, red, ((int(mousePos[0] / sizeOfCell) - 1) * sizeOfCell,
                                                       int(mousePos[1] / sizeOfCell) * sizeOfCell, 3 * sizeOfCell, 50))
                else:
                    pygame.draw.rect(dispScreen, green, ((int(mousePos[0] / sizeOfCell) - 1) * sizeOfCell,
                                                         int(mousePos[1] / sizeOfCell) * sizeOfCell, 3 * sizeOfCell,
                                                         50))
                    if pygame.mouse.get_pressed()[0]:
                        boards[0][(int(mousePos[0] / sizeOfCell) - 1)][(int(mousePos[1] / sizeOfCell))] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell) + 0)][(int(mousePos[1] / sizeOfCell))] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell) + 1)][(int(mousePos[1] / sizeOfCell))] = 3
                        shipToPlace = 0
                        shipRotation = 0
                        shipsNotPlaced[4] -= 1
        if shipRotation == 1:
            if 1 * sizeOfCell < mousePos[1] < (boardHeight - 1) * sizeOfCell and mousePos[0] < boardLength * sizeOfCell:
                sumOfCells = 0
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) - 1)]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 0)]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 1)]
                if sumOfCells != 0:
                    pygame.draw.rect(dispScreen, red, ((int(mousePos[0] / sizeOfCell)) * sizeOfCell,
                                                       int((mousePos[1] / sizeOfCell) - 1) * sizeOfCell, 50,
                                                       3 * sizeOfCell))
                else:
                    pygame.draw.rect(dispScreen, green, ((int(mousePos[0] / sizeOfCell)) * sizeOfCell,
                                                         int((mousePos[1] / sizeOfCell) - 1) * sizeOfCell, 50,
                                                         3 * sizeOfCell))
                    if pygame.mouse.get_pressed()[0]:
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) - 1)] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 0)] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 1)] = 3
                        shipToPlace = 0
                        shipRotation = 0
                        shipsNotPlaced[4] -= 1

    if shipToPlace == 5:
        mousePos = pygame.mouse.get_pos()
        if shipRotation == 0:
            if 1 * sizeOfCell < mousePos[0] < boardLength * sizeOfCell:
                sumOfCells = 0
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) - 1)][(int(mousePos[1] / sizeOfCell))]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell) + 0)][(int(mousePos[1] / sizeOfCell))]
                if sumOfCells != 0:
                    pygame.draw.rect(dispScreen, red, ((int(mousePos[0] / sizeOfCell) - 1) * sizeOfCell,
                                                       int(mousePos[1] / sizeOfCell) * sizeOfCell, 2 * sizeOfCell,
                                                       50))
                else:
                    pygame.draw.rect(dispScreen, green, ((int(mousePos[0] / sizeOfCell) - 1) * sizeOfCell,
                                                         int(mousePos[1] / sizeOfCell) * sizeOfCell, 2 * sizeOfCell,
                                                         50))
                    if pygame.mouse.get_pressed()[0]:
                        boards[0][(int(mousePos[0] / sizeOfCell) - 1)][(int(mousePos[1] / sizeOfCell))] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell) + 0)][(int(mousePos[1] / sizeOfCell))] = 3
                        shipToPlace = 0
                        shipRotation = 0
                        shipsNotPlaced[5] -= 1
        if shipRotation == 1:
            if 1 * sizeOfCell < mousePos[1] < boardHeight * sizeOfCell and mousePos[0] < boardLength * sizeOfCell:
                sumOfCells = 0
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) - 1)]
                sumOfCells += boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 0)]
                if sumOfCells != 0:
                    pygame.draw.rect(dispScreen, red, ((int(mousePos[0] / sizeOfCell)) * sizeOfCell,
                                                       int((mousePos[1] / sizeOfCell) - 1) * sizeOfCell, 50,
                                                       2 * sizeOfCell))
                else:
                    pygame.draw.rect(dispScreen, green, ((int(mousePos[0] / sizeOfCell)) * sizeOfCell,
                                                         int((mousePos[1] / sizeOfCell) - 1) * sizeOfCell, 50,
                                                         2 * sizeOfCell))
                    if pygame.mouse.get_pressed()[0]:
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) - 1)] = 3
                        boards[0][(int(mousePos[0] / sizeOfCell))][(int(mousePos[1] / sizeOfCell) + 0)] = 3
                        shipToPlace = 0
                        shipRotation = 0
                        shipsNotPlaced[5] -= 1

    if shipsNotPlaced == [None, 0, 0, 0, 0, 0]:
        setupGoing = False
    pygame.display.update()

botSetup(2)

while inWar:
    drawTable(0, 0, 0)
    drawTable(sizeOfCell * 12, 0, 1)
    if playerHits == 30 or botHits == 30:
        inWar = False
    for event in pygame.event.get():
        if playersTurn:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseClick = event.pos
                print(mouseClick)
                if mouseClick[0] > sizeOfCell * 12:
                    if boards[1][int(mouseClick[0] / sizeOfCell) - 12][int(mouseClick[1] / sizeOfCell)] == 0:
                        print(int(mouseClick[0] / sizeOfCell) - 12)
                        print(int(mouseClick[1] / sizeOfCell))
                        if boards[2][int(mouseClick[0] / sizeOfCell) - 12][int(mouseClick[1] / sizeOfCell)] == 3:
                            boards[1][int(mouseClick[0] / sizeOfCell) - 12][int(mouseClick[1] / sizeOfCell)] = 2
                            playerHits += 1
                        else:
                            boards[1][int(mouseClick[0] / sizeOfCell) - 12][int(mouseClick[1] / sizeOfCell)] = 1
                        playersTurn = False
        elif event.type == pygame.QUIT:
            endGame = False
            inWar = False
    if not playersTurn:
        if targets == [None]:
            if botRetries <= 10:
                x = int(random.random() * 5)
                y = int(random.random() * 10)
                if y % 2 == 0:
                    x = x * 2
                else:
                    x = x * 2 - 1
            else:
                x = int(random.random() * 10)
                y = int(random.random() * 10)
            print(x)
            print(y)
            print(botRetries)
            if boards[3][x][y] == 0:
                if boards[0][x][y] == 0:
                    boards[3][x][y] = 1
                    boards[0][x][y] = 1
                    targets = [None]
                    playersTurn = True
                elif boards[0][x][y] == 3:
                    boards[3][x][y] = 2
                    boards[0][x][y] = 2
                    botHits += 1
                    playersTurn = True
                    n = int(random.random() * 4)
                    if n % 4 == 0 and y <= 8:
                        targets = [x, y + 1]
                    elif n % 4 == 1 and y >= 1:
                        targets = [x, y - 1]
                    elif n % 4 == 2 and x <= 8:
                        targets = [x + 1, y]
                    elif n % 4 == 3 and x >= 1:
                        targets = [x - 1, y]
                    else:
                        targets = [None]
            else:
                botRetries += 1
        else:
            x = targets[0]
            y = targets[1]
            print(targets)
            print(botRetries)
            if boards[3][x][y] == 0:
                if boards[0][x][y] == 0:
                    boards[3][x][y] = 1
                    boards[0][x][y] = 1
                    targets = [None]
                    playersTurn = True
                elif boards[0][x][y] == 3:
                    boards[3][x][y] = 2
                    boards[0][x][y] = 2
                    botHits += 1
                    playersTurn = True
                    n = int(random.random() * 4)
                    if n % 4 == 0 and y <= 8:
                        targets = [x, y + 1]
                    elif n % 4 == 1 and y >= 1:
                        targets = [x, y - 1]
                    elif n % 4 == 2 and x <= 8:
                        targets = [x + 1, y]
                    elif n % 4 == 3 and x >= 1:
                        targets = [x - 1, y]
                    else:
                        targets = [None]
            else:
                targets = [None]
                botRetries += 1
    pygame.display.update()

if botHits > playerHits:
    dispScreen.fill(black)
    font = pygame.font.SysFont(None, 24)
    img = font.render('The AI won', True, white)
    dispScreen.blit(img, (screenWidth / 2 - 50, screenHeight / 2 - 24))
    pygame.display.update()
elif playerHits > botHits:
    dispScreen.fill(black)
    font = pygame.font.SysFont(None, 24)
    img = font.render('You won', True, white)
    dispScreen.blit(img, (screenWidth / 2 - 50, screenHeight / 2 - 24))
    pygame.display.update()

while endGame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            endGame = False

pygame.quit()
sys.exit(0)
