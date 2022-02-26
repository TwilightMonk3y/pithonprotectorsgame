# FILE DESCRIPTION: This file manages what happens during the gameplay part of the game
import pygame

import classes
import objects
import images

buttons = []
shopButtons = []

myFont = pygame.font.Font(None, 35)

# Shop buttons
# Set 1 of towers
shopButtons.append(classes.ShopButton(classes.SniperTower()))
shopButtons.append(classes.ShopButton(classes.PokerTower()))
shopButtons.append(classes.ShopButton(classes.FlamethrowerTower()))
# Set 2 of towers
shopButtons.append(classes.ShopButton(classes.GatlingTower()))
shopButtons.append(classes.ShopButton(classes.CannonTower()))
shopButtons.append(classes.ShopButton(classes.TurretTower()))
#Set 3 of towers
shopButtons.append(classes.ShopButton(classes.GeneratorTower()))
shopButtons.append(classes.ShopButton(classes.ElectricuterTower()))
shopButtons.append(classes.ShopButton(classes.ShinerTower()))
#Set 4 of towers
shopButtons.append(classes.ShopButton(classes.MageTower()))
shopButtons.append(classes.ShopButton(classes.HybridTower()))
shopButtons.append(classes.ShopButton(classes.DestroyerTower()))
#Set 5 of towers
shopButtons.append(classes.ShopButton(classes.MissileLauncher()))
shopButtons.append(classes.ShopButton(classes.SkeletonTower()))
shopButtons.append(classes.ShopButton(classes.SkeletonTower()))

# Buttons on the Gameplay screen
buttons.append(classes.Button(images.scrollUpButton, pygame.Rect(objects.width - 75, 0, 50, 50), [f'objects.shopButtonsShowed -= 1\nif objects.shopButtonsShowed < 0: objects.shopButtonsShowed = {len(shopButtons)/3 - 1}'])) # Shop up button
buttons.append(classes.Button(images.scrollDownButton, pygame.Rect(objects.width - 75, 400, 50, 50), [f'objects.shopButtonsShowed += 1\nif objects.shopButtonsShowed >= {len(shopButtons)/3}: objects.shopButtonsShowed = 0'])) # Shop down button
buttons.append(classes.Button(images.roundButton, pygame.Rect(0, objects.height - 100, 100, 100), ['if objects.enemyIndex == len(objects.waves[objects.wave]) and objects.wave < len(objects.waves): objects.wave += 1; objects.enemyIndex = 0'])) # Next round button
buttons.append(classes.Button(images.settingsButton, pygame.Rect(860,10, 50, 50), ["objects.gameState = 'settings'","objects.lastGameState = 'gameplay'"])) # Open settings button

def GameplayUpdate(): # TODO: Check at the order
    for event in pygame.event.get(pygame.KEYDOWN):
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
        if event.key == pygame.K_SPACE:
            objects.popUpBox = True
        if event.key == pygame.K_RETURN:
            objects.popUpBox = False
            
    for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
        for button in buttons:
            button.update()
        for button in shopButtons:
            button.update()
        if objects.popUpBox:
            for button in objects.popUpButtons:
                button.update()

    # Tower placement code
    for event in pygame.event.get(pygame.MOUSEBUTTONUP):
        if objects.selectedTower != None:
            validplacement = True
            for path in objects.maps[objects.currentMap]['paths']:
                for point in path:
                    dx = point[0] - objects.selectedTower.rect.centerx
                    dy = point[1] - objects.selectedTower.rect.centery
                    dist = (dx**2+dy**2)**.5
                    if dist < 40:
                        validplacement = False
                        break
            if validplacement == True:
                objects.selectedTower.active = True
                objects.selectedTower = None

    if objects.selectedTower != None:
        objects.selectedTower.rect.center = pygame.mouse.get_pos()

    for tower in objects.towers:
        tower.update()
    for projectile in objects.projectiles:
        projectile.update()
    for enemy in objects.enemies:
        enemy.update()

    if objects.health <= 0:
        print("game over...")
        pygame.quit()

    # Enemy spawning # TODO: Rework/ Clean up logic
    if objects.spawnCooldown == 0:
        if objects.enemyIndex == len(objects.waves[objects.wave]):
            #print('Round over!')
            if objects.autoStart and objects.enemyIndex == len(objects.waves[objects.wave]) and objects.wave < len(objects.waves):
                objects.wave += 1
                objects.enemyIndex = 0
        else:
            objects.enemies.append(objects.waves[objects.wave][objects.enemyIndex])
            objects.enemyIndex += 1
    if objects.enemyIndex != len(objects.waves[objects.wave]):
        objects.spawnCooldown += 1
        if objects.spawnCooldown == objects.spawnInterval:
            objects.spawnCooldown = 0

    
        
def GameplayRender():
    objects.screen.blit(objects.maps[objects.currentMap]['image'], objects.gameRect)
    pygame.draw.rect(objects.screen, (255,255,255), objects.shopRect)

    for tower in objects.towers:
        tower.render()
    for projectile in objects.projectiles:
        projectile.render()
    for enemy in objects.enemies:
        enemy.render()

    for button in buttons:
        button.render()
    for button in shopButtons:
        button.render()

    if objects.popUpBox:
        for popUpButton in objects.popUpButtons:
            popUpButton.render()
        objects.screen.blit(objects.popUpBoxImage, objects.popUpBoxRect)
        print(objects.selectedAnswer)

    hpDisplay = myFont.render("Health: " + str(objects.health), 1, (0, 0, 0))
    doughDisplay = myFont.render("Money: " + str(objects.money), 1, (0, 0, 0))
    objects.screen.blit(hpDisplay, (5, 5))
    objects.screen.blit(doughDisplay, (5, 20))