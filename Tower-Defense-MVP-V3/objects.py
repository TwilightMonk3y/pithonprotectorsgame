import pygame

# Constants
DEVELOPMENT = True
fps = 60
windowSize = width, height = 1000,500
gameRect = pygame.Rect(0, 0, int(width * .85), height)
shopRect = pygame.Rect(int(width * .85), 0, int(width * .15), height)
towerSize = 50, 50

gameState = ''
lastGameState = ''
difficultyLevel = ''
autoStart = 0
speed = ''
questionDifficulty = ''


screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)

# Gameplay variables
selectedTower = None
roundNumber = 0
showTowerRange = False
shopButtonsShowed = 0
popUpBox = False
popUpBoxImage = pygame.Surface((500,200))
popUpBoxRect = popUpBoxImage.get_rect()
popUpBoxAnswers = [0,0,0,0]
selectedAnswer = 0
popUpButtons = []
currentBoss = None

spawnCooldown = 0
spawnInterval = 60

waves = []
wave = 0
enemyIndex = 0

maps = []
buttons = []
currentMap = 0

towers = []
enemies = []
projectiles = []

# Player variables
health = 100
money = 1000
