import pygame
import random
import os
import math

import objects
import images
import classes

def loadMap(level_path):
    current_path = os.path.dirname(__file__)
    map_loc = os.path.join(current_path, level_path)
    maptxt = open(map_loc, 'r')
    data = maptxt.read()
    maptxt.close()
    data = data.split("\n")

    paths = []
    path = []
    for line in data:
        if len(line) == 0:
            pass 
        elif line[0] == "#":
            if path != []:
                paths.append(path)
                path = []
        else:
            coords = line.split(" ")
            if len(coords) == 2:
                coords = int(coords[0]), int(coords[1])
                path.append(coords)
    paths.append(path)

    # Splits the paths into a bunch of smaller ones
    pathResolution = 5
    hiResPaths = []
    hiResPath = []
    for path in paths:
        for i in range(len(path)-1):
            start = path[i]
            end = path[i+1]
            dx = end[0]-start[0]
            dy = end[1]-start[1]
            dist = (dx**2+dy**2)**.5
            numPoints = math.floor(dist/pathResolution)
            dx = dx/numPoints
            dy = dy/numPoints
            for n in range(numPoints):
                hiResPath.append((math.floor(start[0] + dx*n), math.floor(start[1] + dy*n)))
        hiResPaths.append(hiResPath)
        hiResPath = []

    return hiResPaths

# Gift of Nature
obstaclesGON = [objects.shopRect] #TODO: set up obstacles for giftOfNature
giftOfNature = {'image': images.giftOfNature,
                'paths': loadMap('GiftOfNature.txt'), 
                'obstacles': obstaclesGON}

objects.maps.append(giftOfNature)

# Cranesite
obstaclesCS = [objects.shopRect, pygame.Rect(155,0,25,361), pygame.Rect(40,338,120,25), pygame.Rect(40,350,25,125), pygame.Rect(45,450,544,25), pygame.Rect(563,470,25,67),pygame.Rect(0,130,771,25), pygame.Rect(750,0,25,976), pygame.Rect(773,316,300,25), pygame.Rect(491,10,278,25)]

numBoxes = 8
areaRect = pygame.Rect(237,155,250,300)
boxWidth = 85
boxHeight = areaRect[3]/numBoxes

for i in range(numBoxes):
    xPos = areaRect[0] + (areaRect[2] - boxWidth) / numBoxes * i
    yPos = areaRect[1] + areaRect[3] - boxHeight * (i + 1)
    diagonalRect = pygame.Rect(xPos, yPos, boxWidth, boxHeight)
    obstaclesCS.append(diagonalRect)

craneSite = {'image': images.craneSite, 
             'paths': loadMap('Cranesite.txt'), 
             'obstacles': obstaclesCS}
objects.maps.append(craneSite)

# TODO: Base paths off of current map
wave1 = [classes.Skeleton(random.choice(giftOfNature['paths']))]
for i in range(5):
    wave1.append(classes.Ghost(random.choice(giftOfNature['paths'])))
wave2 = [classes.Silver_Skeleton(random.choice(giftOfNature['paths']))]
for i in range(3):
    wave2.append(classes.Skeleton(random.choice(giftOfNature['paths'])))
wave3 = [classes.Silver_Skeleton(random.choice(giftOfNature['paths'])), classes.Skeleton(random.choice(giftOfNature['paths']))]
for i in range(4):
    wave3.append(classes.Silver_Skeleton(random.choice(giftOfNature['paths'])))
    wave3.append(classes.Skeleton(random.choice(giftOfNature['paths'])))
wave4 = [classes.Goblin(random.choice(giftOfNature['paths']))]
for i in range(5):
    wave4.append(classes.Goblin(random.choice(giftOfNature['paths'])))
    wave4.append(classes.Ghost(random.choice(giftOfNature['paths'])))
wave5 = [classes.Ghost(random.choice(giftOfNature['paths']))]#*10
for i in range(3):
    wave5.append(classes.Ghost(random.choice(giftOfNature['paths'])))
    wave5.append(classes.Skeleton(random.choice(giftOfNature['paths'])))
    wave5.append(classes.Goblin(random.choice(giftOfNature['paths'])))
wave6 = [classes.Giant(random.choice(giftOfNature['paths']))]
for i in range(10):
    wave6.append(classes.Goblin(random.choice(giftOfNature['paths'])))
wave7 = [classes.Giant(random.choice(giftOfNature['paths']))]
for i in range(5):
    wave7.append(classes.Goblin(random.choice(giftOfNature['paths'])))
    wave7.append(classes.Ghost_Giant(random.choice(giftOfNature['paths'])))
wave8 = [classes.Goblin(random.choice(giftOfNature['paths']))]
for i in range(10):
    wave8.append(classes.Giant(random.choice(giftOfNature['paths'])))
    wave8.append(classes.Ghost_Giant(random.choice(giftOfNature['paths'])))
wave9 = [classes.Goblin(random.choice(giftOfNature['paths']))]
for i in range(10):
    wave9.append(classes.Goblin(random.choice(giftOfNature['paths'])))
objects.waves = [[], wave1, wave2, wave3, wave4, wave5, wave6, wave7, wave8, wave9]
#objects.waves = [[], wave6]
 # TEMP

# Instructions # TODO: Needs to be cleaned up
lines = []

text_image = """&How to Play Robots vs Math& &What is Robots V.S. Math?& Robots v.s. Math is a tower defense game where you place& towers that stop enemies from getting to the end of a path. &Towers& Evey tower has its own range, attack speed, cost, and damage. The damage is& how much damage it does to enemies. For example, an enemy has 5 health. The& tower does 2 damage. Then the tower will need 3 shots to get 5 damage or more done. Then nothing else will hit the enemy since it is destroyed. The cost is how much it costs to place. If a tower costs 150, you will need 150 to place it down. If you don’t have 150, you can’t place it down. Your cash can’t go below 0. The attack speed is how fast the tower is able to deal damage to enemies. For example, some towers might do less damage, but have greater attack speed, or do more damage, but do not have that much attack speed. The range is how far the tower is able to do damage to enemies. For example: If the tower’s range is 200 pixels, it will only be able to hit enemies that are within 200 pixels of the tower. &Placing Towers& To place a tower, drag it from the side of the map to wherever you see fit. The& closer the tower is to paths, the better it usually is, because the tower can attack enemies.& Towers cannot be placed on the designated paths for the enemy to move. &Gadgets& Gadgets are mini-tools to help stop the enemies from going to the end of the track.& Some include a trap to damage enemies. Another one is a bomb to explode near& enemies. &Enemies& Enemies move along designated paths to try to get to the end of it. Each enemy has& its own health, speed, and special properties. Some don’t have any special ones.& For example, the ghost can only be hit by certain towers with sharp sensors, and its invisibility can be removed by a tower. To stop an enemy, place towers. The tower’s range will be where it will hit the enemies. If the enemy is out of range, nothing can damage it. If it is inside the range, the tower can damage it. &Winning& The way to win the game is to survive every single one of the levels available& without losing all your lives. You lose lives by letting enemies get to the end of the path. &Losing& You start off with 10 lives. Every enemy that is at the end of the path will disappear& and you will lose 1 life. You can no longer damage the enemies if it reaches the end of the path. If you leak to 0 lives, you lose."""

text_image = text_image.split("&")

#for i in range(len(text_image)):
#  print('hi')
#  if (text_image[i][0] == "&"):
    #make bold???
#    print('do something')

  
boldLines = [0,1,4,22,28,32,44,49]

pygame.font.init()
my_font = pygame.font.Font(None, 35)
big_font = pygame.font.Font(None, 50)

for line in text_image:
    if(len(lines) in boldLines):
        lines.append(big_font.render(line, True, (255,0,0)))
    else:
        lines.append(my_font.render(line, True, (0,0,255)))