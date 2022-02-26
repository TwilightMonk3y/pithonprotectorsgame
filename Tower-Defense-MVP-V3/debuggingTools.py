# FILE DESCRIPTION: Contains all of the debug code for convenient toggling
import pygame

import objects
import data

DISPLAYPATHS = False
DISPLAYOBSTACLES = False
PRINTMOUSE = False

def Debug():
    # Print mouse position on click
    if PRINTMOUSE:
        if pygame.mouse.get_pressed(3)[0]:
            print("Mouse Position: ", end="")
            print(pygame.mouse.get_pos())

    # Display paths and shortest distance from held tower to said paths
    if DISPLAYPATHS: 
        objects.maps[objects.currentMap]['paths'] = data.loadMap('GiftOfNature.txt')
        for path in objects.maps[objects.currentMap]['paths']:
            pygame.draw.lines(objects.screen,(255, 0, 0), False, path)
        if objects.selectedTower != None:
            for path in objects.maps[objects.currentMap]['paths']:
                for point in path:
                    pygame.draw.line(objects.screen, (0, 0, 255), objects.selectedTower.rect.center, point)

    # Display Obstacles
    if DISPLAYOBSTACLES:
        for obstacle in objects.maps[objects.currentMap]['obstacles']:
            pygame.draw.rect(objects.screen, (0, 255, 0), obstacle)