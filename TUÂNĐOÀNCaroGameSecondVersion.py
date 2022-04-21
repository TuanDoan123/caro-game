import pygame, sys, random
from pygame.locals import *

FPS = 5
WINDOWWIDTH = 800
WINDOWHIGHT = 800
BOARDWIDTH = 15
BOARDHIGHT = 15
BOXSIZE = 50
GAP = 1
XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * (BOXSIZE + GAP))/2)
YMARGIN = int((WINDOWHIGHT - BOARDHIGHT * (BOXSIZE + GAP))/2)
waitTime = 10000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BGCOLOR = ( 3, 54, 73)
YELLOW = (255, 255,   0)
ORANGE = (255, 128,   0)

COLORTEXT = YELLOW
BGTEXT = WHITE

PLAYERTILE = 'X'
COMPUTERTILE = 'O'

def main():
    global windowSurf

    pygame.init()
    mainClock = pygame.time.Clock()
    windowSurf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHIGHT))
    pygame.display.set_caption('CARO TUÂN ĐOÀN')

    board = getBoard()
    introduce(board)
    while True:
        computerGo = False
        drawBoard(board)
        spotx, spoty = (0, 0)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                spotx, spoty = event.pos
        boxx, boxy = getBoxAtPixel(spotx, spoty)

        if (boxx, boxy) != (None, None) and board[boxx][boxy] == None:
            makeTile(board, boxx, boxy, PLAYERTILE)
            upDateTile(board, 1)

            result1 = scoreTile(board, boxx, boxy, PLAYERTILE)
            if result1 == 1:
                upDateText('You won', 'Continue')
                board = getBoard()
                continue
            elif equal(board):
                upDateText('Hòa', 'Continue')
                board = getBoard()
            computerGo = True
        if computerGo:
            computerx, computery = computerChosen(board, boxx, boxy)
            makeTile(board, computerx, computery, COMPUTERTILE)
            upDateTile(board, 1)

            result1 = scoreTile(board, computerx, computery, COMPUTERTILE)
            if result1 == 1:
                upDateText('Tuân Đoàn won', 'Continue')
                board = getBoard()
            elif equal(board):
                upDateText('Hòa', 'Continue')
                board = getBoard()
        pygame.display.update()
        mainClock.tick(FPS)

def introduce(board):
    drawBoard(board)
    makeText('Welcom to Caro Tuân Đoàn', COLORTEXT, int(WINDOWWIDTH/2), int(WINDOWHIGHT/2), 60)
    pygame.display.update()
    pygame.time.wait(5000)

def upDateTile(board, time):
    drawBoard(board)
    pygame.display.update()
    pygame.time.wait(time)

def upDateText(firstText, secondText):
    makeText(firstText, COLORTEXT, int(WINDOWWIDTH / 2), int(WINDOWHIGHT / 2) - 30, 80)
    makeText(secondText, COLORTEXT, int(WINDOWWIDTH / 2), int(WINDOWHIGHT / 2) + 30, 80)
    pygame.display.update()
    pygame.time.wait(waitTime)

def getBoard():
    board = []
    for i in range(BOARDWIDTH):
        board.append([None]*BOARDHIGHT)
    return board

def leftTopAtBox(boxx, boxy):
    left = XMARGIN + boxx * (BOXSIZE + GAP)
    top = YMARGIN + boxy * (BOXSIZE + GAP)
    return (left, top)

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHIGHT):
            left, top = leftTopAtBox(boxx, boxy)
            rect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if rect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def makeTile(board, boxx, boxy, tile):
    board[boxx][boxy] = tile

def drawTile(board, boxx, boxy):
    left, top = leftTopAtBox(boxx, boxy)
    pygame.draw.rect(windowSurf, WHITE, (left, top, BOXSIZE, BOXSIZE))
    if board[boxx][boxy] == PLAYERTILE:
        pygame.draw.line(windowSurf, RED, (left + 10, top + 10), (left + BOXSIZE - 10, top + BOXSIZE - 10), 10)
        pygame.draw.line(windowSurf, RED, (left + BOXSIZE - 10, top + 10), (left + 10, top + BOXSIZE - 10), 10)
    elif board[boxx][boxy] == COMPUTERTILE:
        pygame.draw.circle(windowSurf, BLUE, (left + int(BOXSIZE/2), top + int(BOXSIZE/2)), int(BOXSIZE/2 - 5), 10)

def drawBoard(board):
    windowSurf.fill(BGCOLOR)

    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHIGHT):
            drawTile(board, boxx, boxy)

def getBoardCopy(board):
    boardCopy = getBoard()
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHIGHT):
            boardCopy[boxx][boxy] = board[boxx][boxy]
    return boardCopy

def computerChosen(board, playerboxx, playerboxy):
    preferSequence = []
    for i in range(1, 17):
        preferSequence.append(i)

    numSequence = []
    for x in range(len(preferSequence)):
        if x <= 8:
            for i in range(2):
                numSequence.append(x)
        else:
            numSequence.append(x)

    first = True
    for i in range(len(preferSequence) + 9):
        if i <= 17:
            if first:
                tile = COMPUTERTILE
                first = False
            else:
                tile = PLAYERTILE
                first = True
        else:
            tile = COMPUTERTILE
        for boxx in range(BOARDWIDTH):
            for boxy in range(BOARDHIGHT):
                boardCopy = getBoardCopy(board)
                if boardCopy[boxx][boxy] == None:
                    makeTile(boardCopy, boxx, boxy, tile)
                    result1 = scoreTile(boardCopy, boxx, boxy, tile)
                    if result1 == preferSequence[numSequence[i]]:
                        return boxx, boxy
    return playerboxx, playerboxy - 1

def makeText(text, color, x, y, size):
    basicFont = pygame.font.Font(None, size)
    textSurf = basicFont.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.center = (x, y)
    windowSurf.blit(textSurf, textRect)

def isOnBoard(x, y):
    return 0 <= x <= BOARDWIDTH - 1 and 0 <= y <= BOARDHIGHT - 1

def scoreTile(board, boxx, boxy, tile):
    result1 = []
    for x, y in [(1,1), (0,1), (1, -1), (1,0)]:
        isSpace = False
        score = 0
        space = 0
        boxxorg = boxx
        boxyorg = boxy
        while isOnBoard(boxxorg, boxyorg):
            boxxorg += x
            boxyorg += y
            if isOnBoard(boxxorg, boxyorg):
                if board[boxxorg][boxyorg] == tile:
                    continue
                elif board[boxxorg][boxyorg] == None:
                    space += 1
                    isSpace = True
                else:
                    isSpace = True
            if not isOnBoard(boxxorg, boxyorg) or isSpace:
                boxxorg -= x
                boxyorg -= y
                while isOnBoard(boxxorg, boxyorg):
                    score += 1
                    boxxorg -= x
                    boxyorg -= y
                    if isOnBoard(boxxorg, boxyorg):
                        if board[boxxorg][boxyorg] == tile:
                            continue
                        elif board[boxxorg][boxyorg] == None:
                            space += 1
                            boxxorg = -1
                            boxyorg = -1
                        else:
                            boxxorg = -1
                            boxyorg = -1
        result1.append((score, space))

    result2 = []
    for x, y in [(1,1), (0,1), (1, -1), (1,0)]:
        spaceReal = 0
        isSpace = False
        score = 0
        space = 0
        boxxorg = boxx
        boxyorg = boxy
        while isOnBoard(boxxorg, boxyorg):
            boxxorg += x
            boxyorg += y
            if isOnBoard(boxxorg, boxyorg):
                if board[boxxorg][boxyorg] == tile:
                    space = 0
                    continue
                elif board[boxxorg][boxyorg] == None:
                    if space == 0:
                        space += 1
                        continue
                    space = 0
                    isSpace = True
                else:
                    space = 0
                    isSpace = True
            space = 0
            if not isOnBoard(boxxorg, boxyorg) or isSpace:
                while isOnBoard(boxxorg - x, boxyorg - y):
                    boxxorg -= x
                    boxyorg -= y
                    if isOnBoard(boxxorg, boxyorg):
                        if board[boxxorg][boxyorg] == tile:
                            score += 1
                            space = 0
                            continue
                        elif board[boxxorg][boxyorg] == None:
                            if space == 0:
                                spaceReal += 1
                                space += 1
                                continue
                            boxxorg = -10
                            boxyorg = -10
                        else:
                            boxxorg = -10
                            boxyorg = -10
                boxxorg = -10
                boxyorg = -10
        result2.append((score, spaceReal))

    numList = []
    for x in range(5, 10):
        for y in range(3):
            if (x, y) in result1:
                numList.append(1)

    if  result1.count((4, 1)) >= 2 or \
        (4, 2) in result1 or \
        result2.count((4, 2)) >= 2 or \
        result2.count((4, 1)) >= 2 or \
        (4, 2) in result2 and (4, 1) in result2:
            numList.append(2)

    if  result1.count((3, 2)) >= 2 or \
        (4, 1) in result1 and (3, 2) in result1 or \
        result2.count((3, 3)) >= 2 or \
        (4, 2) in result2 and (3, 3) in result2 or \
        (4, 1) in result2 and (3, 3) in result2:
            numList.append(3)

    if result2.count((3, 2)) >= 2 or \
        (4, 2) in result2 and (3, 2) in result2 or \
        (4, 1) in result2 and (3, 2) in result2 or \
        (3, 3) in result2 and (3, 2) in result2:
        numList.append(4)

    for i in range(5):
        if i <= 1:
            a = 3
            b = 1  - i
        else:
            a = 2
            b = 5 - i
        if (4, 2) in result2 and (a, b) in result2 or \
            (4, 1) in result2 and (a, b) in result2 or \
            (3, 3) in result2 and (a, b) in result2:
            numList.append(5 + i)

    if (4, 1) in result1:
        numList.append(10)

    if (3, 2) in result1:
        numList.append(11)

    if (4, 2) in result2 or (4, 1) in result2 or (3, 3) in result2:
        numList.append(12)

    for i in range(4):
        if i <= 1:
            a = 3
        else:
            a = 2
        if (3, 2) in result2 and (a, i) in result2:
            numList.append(13)

    if (3, 2) in result2 and (2, 1) in result2 or \
        (3, 2) in result2 and (2, 0) in result2 or \
        (3, 2) in result2:
        numList.append(14)

    for i in range(3):
         if (3, 1) in result2 and (2, 3 - i) in result2:
             numList.append(15)
    for i in range(3):
        if result2.count((2, 3 - i)) >= 2:
            numList.append(15)
    for i in range(2):
        if (2, 3) in result2 and (2, 2 - i) in result2:
            numList.append(15)
    if (2, 2) in result2 and (2, 1) in result2 or \
        result2.count((3, 1)) >= 2:
        numList.append(15)

    if (2, 2) in result1:
        numList.append(16)

    if len(numList) > 0:
        return min(numList)

def equal(board):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHIGHT):
            if board[boxx][boxy] == None:
                return False
    return True

if __name__ == '__main__':
    main()