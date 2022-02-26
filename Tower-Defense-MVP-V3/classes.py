import pygame
import copy
import math

import objects
import images

import mathQuestion

class Button:
    def __init__(self, image, rect, functions = []):
        self.image = pygame.transform.scale(image, rect.size)
        self.rect = rect
        self.functions = functions

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.clickedOn()

    def render(self):
        objects.screen.blit(self.image, self.rect)

    def clickedOn(self):
        for function in self.functions:
            exec(function)

class ShopButton(Button):
    index = 0
    def __init__(self, tower):
        self.index = ShopButton.index
        ShopButton.index += 1
        rect = pygame.Rect((objects.width - 75, (self.index % 3) * 100 + 125), images.towerSize)
        self.tower = tower
        super().__init__(tower.image, rect)

    def render(self):
        if self.index // 3 == objects.shopButtonsShowed:
            objects.screen.blit(self.image, self.rect)

    def clickedOn(self):
        if self.index // 3 == objects.shopButtonsShowed and objects.money >= self.tower.price:
            tower = copy.copy(self.tower)
            tower.rect = copy.copy(self.tower.rect)
            objects.selectedTower = tower
            objects.towers.append(tower)
            objects.money -= self.tower.price

class Tower:
    def __init__(self, image, attack, towerRange, projectileSpeed, actionCooldown, price, shootInvisible, hotkey):
        # Static variables
        self.image = image
        self.originalImage = image
        self.attack = attack
        self.range = towerRange
        self.projectileSpeed = projectileSpeed
        self.actionCooldown = actionCooldown
        self.price = price
        self.shootInvisible = shootInvisible
        self.targetPriority = 'first'

        # Dynamic variables
        self.rect = image.get_rect()
        self.active = False
        self.cooldownCounter = 0
        self.target = 0
    
    def update(self):
        if not self.active:
            return
        if self.cooldownCounter > 0:
            self.cooldownCounter -= 1
            return
        bestTarget = None
        closestDist = None
        for enemy in objects.enemies:
            dist = ((enemy.rect.centerx - self.rect.centerx)**2 + (enemy.rect.centery - self.rect.centery)**2)**0.5 
            if self.range == 0 or dist <= self.range:
                if bestTarget is None or dist < closestDist and not (self.shootInvisible == False and enemy.isInvisible):
                    bestTarget = enemy
                    closestDist = dist

        if bestTarget is not None:
            ax = bestTarget.rect.centerx
            ay = bestTarget.rect.centery

            dx = bestTarget.path[bestTarget.target][0] - ax
            dy = bestTarget.path[bestTarget.target][1] - ay
            mag = (dx**2 + dy**2)**0.5
            if mag == 0:
                print("ERROR: ENEMY AT TARGET")
                return
            vx = round(dx/mag * bestTarget.speed)
            vy = round(dy/mag * bestTarget.speed)
            
            tx = self.rect.centerx
            ty = self.rect.centery
            s = self.projectileSpeed

            a = vx ** 2 + vy ** 2 - s ** 2
            b = 2 * (vx * (ax - tx) + vy * (ay - ty))
            c = (ay - ty) ** 2 + (ax - tx) ** 2
            d = (b ** 2 - 4 * a * c) ** 0.5

            t1 = (-b + d) / (2 * a)
            t2 = (-b - d) / (2 * a)

            if t1 < 0: # Chooses realistic time to collision 
                t1 = t2
            
            xTarget = t1 * vx + ax
            yTarget = t1 * vy + ay

            xDist = xTarget - tx
            yDist = yTarget - ty

            if xDist == 0:
                xDist = .00001
            angle = math.atan(yDist/xDist)
            if xDist < 0:
                angle += math.pi
            
            self.image = pygame.transform.rotate(self.originalImage, math.degrees(angle) - 180) # TODO: figure out rotation issues
            #pygame.draw.line(self.line, (38, 172, 255), (tx, ty), (s * math.cos(angle) + tx,s * math.sin(angle) + ty), 3)
            #pygame.draw.line(screen, Color(38, 172, 255), (ax, ay), (t1 * vx + ax, t1 * vy + ay), 3)
            #pygame.draw.line(screen, Color(38, 172, 255), (tx, ty), (t1 * vx + ax, t1 * vy + ay), 3)
            
            self.cooldownCounter = self.actionCooldown
            self.shoot(angle)

    def shoot(self, angle):
        objects.projectiles.append(Projectile(self.rect.center, self.attack, angle, self.projectileSpeed))

    def render(self):
        objects.screen.blit(self.image, self.rect)
        if (not self.active or objects.showTowerRange) and self.range > 0:
            pygame.draw.circle(objects.screen, (138, 172, 255), self.rect.center, self.range, 5)
            

class SniperTower(Tower):
    def __init__(self):
        super().__init__(images.sniper_tank, 20, 0, 100, 40, 125, True, "s")

class PokerTower(Tower):
    def __init__(self):
        super().__init__(images.poker, 5, 25, 50, 25, 25, False, "p")
    
    def update(self):
        if not self.active:
            return
        if self.cooldownCounter > 0:
            self.cooldownCounter -= 1
            return

        bestTarget = None
        closestDist = None
        for enemy in objects.enemies:
            dist = ((enemy.rect.centerx - self.rect.centerx)**2 + (enemy.rect.centery - self.rect.centery)**2)**0.5 
            if self.range == 0 or dist <= self.range:
                if bestTarget is None or dist < closestDist and not (self.shootInvisible == False and enemy.isInvisible):
                    bestTarget = enemy
                    closestDist = dist
        if bestTarget is not None:
            # TODO: Do damage to the enemy
            self.cooldownCounter = self.actionCooldown

#image, attack, towerRange, projectileSpeed, actionCooldown, price, shootInvisible

class FlamethrowerTower(Tower): 
    def __init__(self):
        super().__init__(images.flamethrower, 5, 100, 50, 15, 100, False, "f")

    def render(self):
        objects.screen.blit(self.image, self.rect)
        if (not self.active or objects.showTowerRange) and self.range > 0:
            pygame.draw.circle(objects.screen, (138, 172, 255), self.rect.center, self.range, 5)

    def shoot(self, angle): # TODO: Needs fire instead of bullets
        objects.projectiles.append(Projectile(self.rect.center, self.attack, angle, self.projectileSpeed))


class GatlingTower(Tower):
    def __init__(self):
        super().__init__(images.gatling_turret, 3, 125, 50, 3, 250, True, "g")

class CannonTower(Tower):
    def __init__(self):
        super().__init__(images.cannon, 100, 125, 50, 75, 150, False, "c")
        self.radius = 50
    
    def shoot(self, angle):
        objects.projectiles.append(SplashProjectile(self.rect.center, self.attack, angle, self.projectileSpeed, self.radius))

class TurretTower(Tower):
    def __init__(self):
        super().__init__(images.turret, 3, 125, 50, 25, 75, True, "t")
#image, attack, towerRange, projectileSpeed, actionCooldown, price, shootInvisible

class GeneratorTower(Tower):
    def __init__(self):
        super().__init__(images.generator, 0, 10000, 100, 400, 750, True, "q")
        self.moneyGen = 100
        self.cooldownCounter = self.actionCooldown

    def update(self):
        if not self.active:
            return
        if self.cooldownCounter > 0:
            self.cooldownCounter -= 1
            return
        
        objects.money += self.moneyGen 
        self.cooldownCounter = self.actionCooldown

class ElectricuterTower(Tower): #TODO: Needs to chain zap
    def __init__(self):
        super().__init__(images.electricuter, 50, 100, 75, 40, 200, False, "e")
    
    def shoot(self, tx, ty, vx, vy, ax, ay, t1, bestTarget):
        objects.projectiles.append(SplashProjectile((tx, ty), self.attack, (t1 * vx + ax, t1 * vy + ay), t1, 1000))

class ShinerTower(Tower):
    def __init__(self):
        super().__init__(images.shiner, 0, 110, 100, 50, 175, True, "s")
    
    def update(self):
        if not self.active:
            return
        if self.cooldownCounter > 0:
            self.cooldownCounter -= 1
            return

        bestTarget = None
        closestDist = None
        for enemy in objects.enemies:
            dist = ((enemy.rect.centerx - self.rect.centerx)**2 + (enemy.rect.centery - self.rect.centery)**2)**0.5 
            if self.range == 0 or dist <= self.range:
                if bestTarget is None or dist < closestDist and not (self.shootInvisible == False and enemy.isInvisible):
                    bestTarget = enemy
                    closestDist = dist
        if bestTarget is not None:
            #objects.projectiles.append(Projectile((tx, ty), self.attack, (t1 * vx + ax, t1 * vy + ay), t1, bestTarget))
            self.cooldownCounter = self.actionCooldown

class MageTower(Tower): # needs to shoot 3 bullets
    def __init__(self):
        super().__init__(images.mage, 50, 120, 50, 75, 150, False, "m")
    def shoot(self, angle):
        objects.projectiles.append(Projectile(self.rect.center, self.attack, angle, self.projectileSpeed))
        objects.projectiles.append(Projectile(self.rect.center, self.attack, angle + .5, self.projectileSpeed))
        objects.projectiles.append(Projectile(self.rect.center, self.attack, angle - .5, self.projectileSpeed))
        

class HybridTower(Tower):
    def __init__(self):
        super().__init__(images.hybrid, 40, 100, 50, 60, 200, False, "h")
        self.moneyGen = 50
        self.cooldownCounter = self.actionCooldown

    def update(self):
        if not self.active:
            return
        if self.cooldownCounter > 0:
            self.cooldownCounter -= 1
            return
        
        objects.money += self.moneyGen 
        self.cooldownCounter = self.actionCooldown
        super().update()

class SkeletonTower(Tower):
    def __init__(self):
        super().__init__(images.silver_skeleton, 0, 0, 0, 0, 0, False, "1")
        def update(self):
            print('placeholder tower')

#image, attack, towerRange, projectileSpeed, actionCooldown, price, shootInvisible

class MissileLauncher(Tower):
    def __init__(self):
        super().__init__(images.missile_launcher, 125, 175, 50, 40, 200, True, "m")
        self.radius = 75
    
    def shoot(self, angle):
        objects.projectiles.append(SplashProjectile(self.rect.center, self.attack, angle, self.projectileSpeed, self.radius))

class DestroyerTower(Tower):
    def __init__(self):
        super().__init__(images.destroyer, 15, 150, 500, 1, 50000, True, "d")

class Projectile:
    def __init__(self, start, damage, angle, speed):
        self.pos = start
        self.damage = damage
        self.xSpeed = speed * math.cos(angle)
        self.ySpeed = speed * math.sin(angle)
        self.rect = None

    def update(self):
        self.pos = (self.pos[0] + self.xSpeed, self.pos[1] + self.ySpeed)
        # Check if projectile collides with any enemies
        if self.rect == None:
            return
        for enemy in objects.enemies:
            if enemy.rect.colliderect(self.rect):
                enemy.health -= self.damage
                objects.projectiles.remove(self)
                return
    
    def render(self):
        self.rect = pygame.draw.circle(objects.screen, (0,0,255), self.pos, 5)

class SplashProjectile:
    def __init__(self, start, damage, angle, speed, radius):
        self.pos = start
        self.damage = damage
        self.xSpeed = speed * math.cos(angle)
        self.ySpeed = speed * math.sin(angle)
        self.radius = radius
        self.rect = None
        self.explode = False

    def update(self):
        self.pos = (self.pos[0] + self.xSpeed, self.pos[1] + self.ySpeed)
        # Check if projectile collides with any enemies
        if self.rect == None:
            return
        for enemy in objects.enemies:
            if enemy.rect.colliderect(self.rect):
                for enemy2 in objects.enemies:
                    dist = ((enemy2.rect.centerx-self.rect.centerx)**2+(enemy2.rect.centery-self.rect.centery)**2)**.5
                    if dist <= self.radius:
                        enemy2.health -= self.damage
                self.explode = True
                return
    def render(self):
        self.rect = pygame.draw.circle(objects.screen, (0,0,255), self.pos, 5)
        if self.explode:
            pygame.draw.circle(objects.screen, (0,0,255), self.pos, self.radius)
            objects.projectiles.remove(self)

class ZapProjectile:
    def __init__(self, start, damage, target, radius):
        self.start = start
        self.damage = damage
        self.targets = [target]
        self.radius = radius

    def update(self):
        for target in self.targets:
            for enemy in objects.enemies:
                dist = ((enemy.rect.centerx-target.rect.centerx)**2+(enemy.rect.centery-target.rect.centery)**2)**.5
                if dist <= self.radius:
                    inList = False
                    for target2 in self.targets:
                        if enemy == target2:
                            inList = True
                    if inList is False:
                        self.targets.append(enemy)
                        # TODO: finish zapping projectile
        pass

    def render(self):
        self.rect = pygame.draw.circle(objects.screen, (0,0,255), self.pos, 5)
        if self.explode:
            pygame.draw.circle(objects.screen, (0,0,255), self.pos, self.radius)
            objects.projectiles.remove(self)


class Enemy:
    def __init__(self, image, health, speed, attack, destroyPrice, path, isInvisible): #TODO: Make path be selected on spawn
        # Static variables
        self.image = image
        self.health = health
        self.speed = speed
        self.attack = attack
        self.destroyPrice = destroyPrice
        self.path = path
        self.isInvisible = isInvisible
        
        # Dynamic variables
        self.rect = image.get_rect()
        self.rect.center = self.path[0]
        self.target = 0

    # Function that gets the enemy to update their position along path
    def update(self):
        # Deal damage if it makes it to the end of the path
        #if self.target >= len(self.path):
            #objects.enemies.remove(self)
            #objects.healthattack -= self.
            #return

        # Get money if defeated
        if self.health <= 0:
            objects.enemies.remove(self)
            objects.money += self.destroyPrice
            return

        # Find distance to the waypoint
        dx = self.path[self.target][0] - self.rect.centerx
        dy = self.path[self.target][1] - self.rect.centery
        mag = (dx**2 + dy**2)**0.5 # How far to waypoint
        dist = self.speed          # How far we can go

        # Moves to the waypoint while they are shorter than the movement distance
        while mag <= dist:
            self.rect.center = self.path[self.target]
            self.target += 1
            # Delete self at end of the path
            if self.target >= len(self.path):
                objects.enemies.remove(self)
                objects.health -= 1
                return
            dx = self.path[self.target][0] - self.rect.centerx
            dy = self.path[self.target][1] - self.rect.centery
            mag = (dx**2 + dy**2)**0.5
            dist -= mag

        # Moves towards next waypoint
        if dist > 0:
            dx = round(dx/mag * self.speed)
            dy = round(dy/mag * self.speed)
            self.rect = self.rect.move(dx,dy)

    def render(self):
        objects.screen.blit(self.image, self.rect)

class Ghost(Enemy):
    def __init__(self, path):
        super().__init__(images.ghost, 20, 5, 5, 3, path, True)

class Skeleton(Enemy):
    def __init__(self, path):
        super().__init__(images.skeleton, 7, 3, 5, 1, path, False)

class Goblin(Enemy):
    def __init__(self, path):
        super().__init__(images.goblin, 25, 10, 5, 10, path, False)

class Silver_Skeleton(Enemy):
    def __init__(self, path):
        super().__init__(images.silver_skeleton, 15, 3, 5, 5, path, False)

class Gold_Skeleton(Enemy):
    def __init__(self, path):
        super().__init__(images.gold_skeleton, 25, 3, 5, 10, path, False)
    
class Boss(Enemy):
    def __init__(self, image, health, speed, attack, destroyPrice, path, isInvisible):
        super().__init__(image, health, speed, attack, destroyPrice, path, isInvisible)
        self.first_time = True

    def update(self):
        if self.first_time: # first time calling move
            mathQuestion.generateQuestions()
            objects.currentBoss = self
            self.first_time = False
        if objects.popUpBox is False: # if popup box is false
            super().update()
    
    def render(self):
        if objects.popUpBox is False: # if popup box is false
            super().render()
        

class Giant(Boss):
    def __init__(self, path):
        super().__init__(images.giant, 100, 2, 5, 15, path, False)
        
class Ghost_Giant(Boss):
    def __init__(self, path):
        super().__init__(images.ghost_giant, 100, 2, 5, 20, path, True)