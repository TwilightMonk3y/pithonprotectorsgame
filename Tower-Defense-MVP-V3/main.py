# FILE DESCRIPTION: This file is the start file that manages what parts of the code should be working and offloads the work to the respective files
import pygame
import sys
import os
def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()
pygame.font.init()

import objects
import gameFunctions
import menuFunctions
import debuggingTools

clock = pygame.time.Clock()
while 1:
    # Stops the game when it is exited
    for event in pygame.event.get(pygame.QUIT):
        pygame.quit()
        sys.exit()
        
    # State Machine that makes it so only one state can be updating or rendering at a time
    if pygame.key.get_pressed()[pygame.K_s] or objects.gameState == 'settings':
        menuFunctions.SettingsUpdate()
        menuFunctions.SettingsRender()

    elif objects.gameState == 'gameplay':
        gameFunctions.GameplayUpdate()
        gameFunctions.GameplayRender() 
        
        if objects.DEVELOPMENT:
            debuggingTools.Debug()     

    elif objects.gameState == 'instructions':
        menuFunctions.InstructionsUpdate()
        menuFunctions.InstructionsRender()

    else:
        menuFunctions.MainMenuUpdate()
        menuFunctions.MainMenuRender()

    # Controls framerate
    clock.tick(objects.fps)
    pygame.display.flip()
