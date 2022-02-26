#FILE DESCRIPTION: This file manages the math aspect of the game.
import pygame
import random
import classes
import images
#import math

#import data
import objects

def generateQuestions():
    question1 = ''
    question2 = ''
    answer1 = 0
    answer2 = 0
    answer3 = 0
    answer4 = 0
    operations = ['+', '-', '/', '*']
    objects.popUpBox = True
    randNums = [random.randint(1, 100),random.randint(1, 100), random.randint(1, 100), random.randint(1, 100)]

    positions = [0,0,0,0]
    positions[random.randint(0,3)] = 1
    # searching
    # while searching 
    #     guess random position
    #     if position empty
    #         searching is false and fill position
    searching = True
    while searching:
        r = random.randint(0,3)
        if 0 == positions[r]:
            positions[r] = 2
            searching = False
    searching = True
    while searching:
        r = random.randint(0,3)
        if 0 == positions[r]:
            positions[r] = 3
            searching = False
    searching = True
    while searching:
        r = random.randint(0,3)
        if 0 == positions[r]:
            positions[r] = 4
            searching = False

    print(positions)

    currentOperator = operations[random.randint(0,3)]
    
    question1 = str(randNums[0]) + currentOperator + str(randNums[1])
    if currentOperator == '/':
      question1 = str(randNums[0]) + currentOperator + str(randNums[1]) + '. Round down.'
    if currentOperator == '+':
      answer1 = randNums[0] + randNums[1]
    if currentOperator == '-':
      answer1 = randNums[0] - randNums[1]
    if currentOperator == '*':
      answer1 = randNums[0] * randNums[1]
    if currentOperator == '/':
      answer1 = randNums[0] // randNums[1]
    
    currentOperator = operations[random.randint(0,3)]
    question2 = str(randNums[2]) + currentOperator + str(randNums[3])
    if currentOperator == '/':
      question2 = str(randNums[2]) + currentOperator + str(randNums[3]) + '. Round down.'
    if currentOperator == '+':
      answer2 = randNums[2] + randNums[3]
    if currentOperator == '-':
      answer2 = randNums[2] - randNums[3]
    if currentOperator == '*':
      answer2 = randNums[2] * randNums[3]
    if currentOperator == '/':
      answer2 = randNums[2] // randNums[3]

    currentOperator = operations[random.randint(0,3)]
    question3 = str(randNums[2]) + currentOperator + str(randNums[3])
    if currentOperator == '/':
      question3 = str(randNums[2]) + currentOperator + str(randNums[3]) + '. Round down.'
    if currentOperator == '+':
      answer3 = randNums[2] + randNums[3]
    if currentOperator == '-':
      answer3 = randNums[2] - randNums[3]
    if currentOperator == '*':
      answer3 = randNums[2] * randNums[3]
    if currentOperator == '/':
      answer3 = randNums[2] // randNums[3]

    currentOperator = operations[random.randint(0,3)]
    question4 = str(randNums[2]) + currentOperator + str(randNums[3])
    if currentOperator == '/':
      question4 = str(randNums[2]) + currentOperator + str(randNums[3]) + '. Round down.'
    if currentOperator == '+':
      answer4 = randNums[2] + randNums[3]
    if currentOperator == '-':
      answer4 = randNums[2] - randNums[3]
    if currentOperator == '*':
      answer4 = randNums[2] * randNums[3]
    if currentOperator == '/':
      answer4 = randNums[2] // randNums[3]

    # Things to put inside popUpBox: Questions, Answers, Background
    # Draw Background

    pygame.font.init()

    spacing = 15

    popUpBoxFont = pygame.font.Font("Fonts/hamberger.ttf", 30)
    question1 = popUpBoxFont.render(question1, True, (0,0,0))
    question2 = popUpBoxFont.render(question2, True, (0,0,0))
    answer1 = popUpBoxFont.render(str(answer1), True, (0,0,0))
    answer2 = popUpBoxFont.render(str(answer2), True, (0,0,0))
    answer3 = popUpBoxFont.render(str(random.randint(-100,100)), True, (0,0,0))
    answer4 = popUpBoxFont.render(str(random.randint(-100,100)), True, (0,0,0))

    tempdata = [answer1, answer2, answer3, answer4]
    answer1 = tempdata[positions[0]-1]
    answer2 = tempdata[positions[1]-1]
    answer3 = tempdata[positions[2]-1]
    answer4 = tempdata[positions[3]-1]
    # Create a new place to save our old data
    # Copy answers 1-4 into the list but in the right place
    # Copy them back into their respective locations

    questionWidth = question1.get_size()[0] + spacing * 3 + question2.get_size()[0]
    answerWidth = answer1.get_size()[0] + spacing * 5 + answer2.get_size()[0] + answer3.get_size()[0] + answer4.get_size()[0]
    
    if questionWidth < answerWidth:
        objects.popUpBoxImage = pygame.Surface((answerWidth, 200))
    else:
        objects.popUpBoxImage = pygame.Surface((questionWidth, 200))
    

    objects.popUpBoxImage.fill((255,255,255))

    objects.popUpBoxImage.blit(question1, (spacing,0))
    objects.popUpBoxImage.blit(question2, (spacing * 2 + question1.get_size()[0],0))
    #objects.popUpBoxImage.blit(question3, (spacing * 3 + question1.get_size()[0],100))
    #objects.popUpBoxImage.blit(question4, (spacing * 4 + question1.get_size()[0],100))

    xAns1 = question1.get_size()[0]/2 - answer1.get_size()[0]/2 + spacing
    xAns2 = question2.get_size()[0]/2 - answer2.get_size()[0]/2 + spacing * 2 + question1.get_size()[0]
    xAns3 = question1.get_size()[0]/2 - answer3.get_size()[0]/2 + spacing
    xAns4 = question2.get_size()[0]/2 - answer4.get_size()[0]/2 + spacing * 2 + question1.get_size()[0]
    objects.popUpBoxImage.blit(answer1, (xAns1, 100))
    objects.popUpBoxImage.blit(answer2, (xAns2, 100))
    objects.popUpBoxImage.blit(answer3, (xAns3, 150))
    objects.popUpBoxImage.blit(answer4, (xAns4, 150))
    #objects.popUpBoxImage.blit(answer5, (spacing,150))
    #objects.popUpBoxImage.blit(answer6, (spacing * 2 + answer1.get_size()[0],150))
    #objects.popUpBoxImage.blit(answer7, (spacing * 3 + answer1.get_size()[0], 150))
    #objects.popUpBoxImage.blit(answer8, (spacing * 4 + answer1.get_size()[0], 150))
    
    objects.popUpBoxRect = objects.popUpBoxImage.get_rect()
    objects.popUpBoxRect.center = objects.gameRect.center

    objects.popUpButtons = []
    objects.popUpButtons.append(classes.Button(images.blue, pygame.Rect((spacing + objects.popUpBoxRect.x, objects.popUpBoxRect.y), question1.get_size()), ['objects.selectedAnswer = 1']))
    objects.popUpButtons.append(classes.Button(images.blue, pygame.Rect((spacing * 2 + question1.get_size()[0] + objects.popUpBoxRect.x, objects.popUpBoxRect.y), question2.get_size()), ['objects.selectedAnswer = 2']))
    
    objects.popUpButtons.append(classes.Button(images.blue, pygame.Rect((xAns1 + objects.popUpBoxRect.x, 100 + objects.popUpBoxRect.y), answer1.get_size()), ['objects.popUpBox = False', f'if {positions[0]} != objects.selectedAnswer: objects.currentBoss.health = objects.currentBoss.health * 2; print("wrong answer")']))
    objects.popUpButtons.append(classes.Button(images.blue, pygame.Rect((xAns2 + objects.popUpBoxRect.x, 100 + objects.popUpBoxRect.y), answer2.get_size()), ['objects.popUpBox = False', f'if {positions[1]} != objects.selectedAnswer: objects.currentBoss.health = objects.currentBoss.health * 2; print("wrong answer")']))
    objects.popUpButtons.append(classes.Button(images.blue, pygame.Rect((xAns3 + objects.popUpBoxRect.x, 150 + objects.popUpBoxRect.y), answer3.get_size()), ['objects.popUpBox = False', f'if {positions[2]} != objects.selectedAnswer: objects.currentBoss.health = objects.currentBoss.health * 2; print("wrong answer")']))
    objects.popUpButtons.append(classes.Button(images.blue, pygame.Rect((xAns4 + objects.popUpBoxRect.x, 150 + objects.popUpBoxRect.y), answer4.get_size()), ['objects.popUpBox = False', f'if {positions[3]} != objects.selectedAnswer: objects.currentBoss.health = objects.currentBoss.health * 2; print("wrong answer")']))

    '''
    # FONT PRACTICE

    ['dejavuserif', 'dejavusansmono', 'freesans', 'dejavusans', 'freeserif', 'freemono', None]
    JonnyFont  = pygame.font.Font("Fonts/PermanentMarker.ttf", 50)
    AdrianFont = pygame.font.Font(pygame.font.match_font("freemono"), 20)
    AndrewFont = pygame.font.Font("Fonts/hamberger.ttf", 70)

    # Font.render(text, antialias, color, background=None)
    JonnyImg  = JonnyFont.render("qwertyuiopasdfghjklzxcvbnm", True, (0,0,0))
    AdrianImg = AdrianFont.render("Hello World", True, (0, 0, 0))
    AndrewImg = AndrewFont.render("hello world",True,(0,0,0))

    objects.popUpBoxImage.blit(JonnyImg,(0,0))
    objects.popUpBoxImage.blit(AdrianImg,(0,50))
    objects.popUpBoxImage.blit(AndrewImg,(0,70))
    '''