# FILE DESCRIPTION: This file manages what happens in the gameStates other than gameplay
import pygame

import classes
import objects
import images
import data

my_font = pygame.font.Font(None, 35)
big_font = pygame.font.Font(None, 50)

# Creation of the buttons for each of the gamestates
menuButtons = [
    classes.Button(images.startButton, images.startrect,
                   ["objects.gameState = 'gameplay'"]),
    classes.Button(images.button2, images.start2rect,
                   ["objects.gameState = 'instructions'"]),
    classes.Button(images.button3, images.start3rect,
                   ["objects.gameState = 'settings'"])
]

instructionsButtons = [classes.Button(images.settingsButton, pygame.Rect(860,10, 50, 50), ["objects.gameState = 'menu'"])] # Back button

settingButtons = [
    classes.Button(images.exitButton, pygame.Rect(650, 75, 25, 25), # Return
                   ["objects.gameState = objects.lastGameState"]),
    classes.Button(images.startButton, pygame.Rect(450, 150, 25, 25),
                   ["objects.difficultyLevel = 'Arithmetics'"]),  # Difficulty
    classes.Button(images.startButton, pygame.Rect(500, 150, 25, 25),
                   ["objects.difficultyLevel = 'Algebra'"]),
    classes.Button(images.startButton, pygame.Rect(550, 150, 25, 25),
                   ["objects.difficultyLevel = 'Geometry'"]),
    classes.Button(images.startButton, pygame.Rect(600, 150, 25, 25),
                   ["objects.difficultyLevel = 'Algebra 2'"]),
    classes.Button(images.onButton, pygame.Rect(500, 200, 25, 25),
                   ["objects.autoStart = True"]),  # Autostart
    classes.Button(images.startButton, pygame.Rect(550, 200, 25, 25),
                   ["objects.autoStart = False"]),
    classes.Button(images.startButton, pygame.Rect(500, 250, 25, 25),
                   ["objects.speed = 'Fast'"]),  # Speed
    classes.Button(images.startButton, pygame.Rect(550, 250, 25, 25),
                   ["objects.speed = 'Slow'"]),
    classes.Button(images.startButton, pygame.Rect(450, 300, 25, 25),
                   ["objects.questionDifficulty = 'Easy'"]),  #Difficulty
    classes.Button(images.startButton, pygame.Rect(500, 300, 25, 25),
                   ["objects.questionDifficulty = 'Medium'"]),
    classes.Button(images.startButton, pygame.Rect(550, 300, 25, 25),
                   ["objects.questionDifficulty = 'Hard'"])
]
# Creation of more content needed for the settings gamestate
settingsText = [
    big_font.render('Settings', True, (249, 250, 232)),
    my_font.render('Subject Difficulty', True, (249, 250, 232)),
    my_font.render('Auto Start', True, (249, 250, 232)),
    my_font.render('Speed', True, (249, 250, 232)),
    my_font.render('Question Difficulty', True, (249, 250, 232))
]
textLocation = [(300, 100), (100, 150), (100, 200), (100, 250), (100, 300)]

# Update and Render methods for the MainMenu gamestate
def MainMenuUpdate():
    for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
        for button in menuButtons:
            button.update()
        break

def MainMenuRender():
    objects.screen.blit(images.background1, (0, 0))
    for button in menuButtons:
        button.render()

# Update and Render methods for the Instructions gamestate
y_offset = 0
def InstructionsUpdate():
    global y_offset
    for event in pygame.event.get():
        if event.type == pygame.MOUSEWHEEL:
            y_offset += 50 * event.y
        if y_offset > 0:
            y_offset = 0
        elif y_offset < -850:
            y_offset = -850
    for button in instructionsButtons:
        button.update()


def InstructionsRender():
    objects.screen.fill((0, 0, 0))
    global y_offset
    counter = 0
    for line in data.lines:
        objects.screen.blit(line, (20, counter + y_offset))
        counter += line.get_height() + 5
    for button in instructionsButtons:
        button.render()

# Update and Render methods for the Settings gamestate
def SettingsUpdate():
    for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
        for settingButton in settingButtons:
            settingButton.update()
        break

def SettingsRender():
    objects.screen.blit(images.background3, (0, 0))
    for number in range(len(settingsText)):  # Drawing text on screen
        objects.screen.blit(settingsText[number], textLocation[number])
    for settingButton in settingButtons:
        settingButton.render()
