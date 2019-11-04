import random
import os

class GameObject(object):
    _display = ''

    def __init__(self, pX, pY):
        self.x = pX
        self.y = pY
        self.setSelf()
    
    def setSelf(self):
        game.table[self.y][self.x] = self
    
    def removeSelf(self):
        game.table[self.y][self.x] = 0

    def display(self):
        return self._display

    def doAction(self):
        self.removeSelf()
    
    #/border verification
    def getLeft(self):
        if self.x == 0:
            return False
        return True

    def getRight(self):
        if self.x == game.size - 1:
            return False
        return True

    def getTop(self):
        if self.y == 0:
            return False
        return True

    def getBottom(self):
        if self.y == game.size - 1:
            return False
        return True

    def destroy(self):
        self.removeSelf()

#end of GameObject

class Player(GameObject):
    _display = "o"

    def __init__(self, pX, pY):
        super().__init__(pX, pY)

    def doAction(self):
        super().doAction()

        lX = self.x
        lY = self.y
        
        if game.choice == 'z':
            if lY == 0:
                lY = game.size - 1
            else:
                lY -= 1
        
        if game.choice == 's':
            if lY == game.size - 1:
                lY = 0
            else:
                lY += 1
        
        if game.choice == 'q':
            if lX == 0:
                lX = game.size - 1
            else:
                lX -= 1
        
        if game.choice == 'd':
            if lX == game.size - 1:
                lX = 0
            else:
                lX += 1

        if game.choice == 'b':
            self.doActionBomb()

        if isinstance(game.table[lY][lX], Enemy):
            game.isEnd = True
            self.destroy()
            return
        
        if isinstance(game.table[lY][lX], Bomb) and game.bombCount < game.MAX_BOMB:
            game.bombCount += 1
            game.bombCooldown = 0
            game.table[lY][lX].destroy()

        self.x = lX
        self.y = lY

        self.setSelf()

    def doActionBomb(self):
        i = 0
        while i < game.size:
            j = 0
            while j < game.size:
                #search enemies on top and bottom
                if j == self.x and i != self.y:
                    if isinstance(game.table[i][j], Enemy):
                        game.table[i][j].destroy()
                
                #search enemies on right and left
                if i == self.y and j != self.x:
                    if isinstance(game.table[i][j], Enemy):
                        game.table[i][j].destroy()
                j += 1
            i += 1
           
        lX = random.randrange(0, game.size)
        lY = random.randrange(0, game.size)
        
        #prevent bomb from spawning in a enemy
        while isinstance(game.table[lY][lX], Enemy):
            lX = random.randrange(0, game.size)
            lY = random.randrange(0, game.size)

        Bomb(lX, lY)

    def destroy(self):
        super().destroy()

#end of Player

class Enemy(GameObject):
    list = []
    _display = "x"

    def __init__(self, pX, pY):
        super().__init__(pX, pY)
    
    @staticmethod
    def createEnemies(pNumber):
        count = 0
        while count < pNumber:
            lX = random.randrange(0, game.size)
            lY = random.randrange(0, game.size)
            
            #stop enemy from spawning in the player
            while [lX, lY] == [player.x, player.y]:
                lX = random.randrange(0, game.size)
                lY = random.randrange(0, game.size)

            lEnemy = Enemy(lX, lY)
            Enemy.list.append(lEnemy)

            count += 1
    
    @staticmethod
    def doActionAll():
        for i in range(0, len(Enemy.list)):
            Enemy.list[i].doAction()
    
    def doAction(self):
        super().doAction()
        lX = self.x
        lY = self.y

        if random.random() < 0.5:
            if random.random() < 0.5:
                if self.getRight():
                    lX += 1
                else:
                    lX -= 1
            else:
                if self.getLeft():
                    lX -= 1
                else:
                    lX += 1
        else:
            if random.random() < 0.5:
                if self.getBottom():
                    lY += 1
                else:
                    lY -= 1
            else:
                if self.getTop():
                    lY -= 1
                else:
                    lY += 1

        self.x = lX
        self.y = lY
        
        if [self.x, self.y] == [player.x, player.y]:
            game.isEnd = True
            player.destroy()
            return
        
        self.setSelf()

    def destroy(self):
        Enemy.list.remove(self)
        super().destroy()

#end of Enemy

class Bomb(GameObject):
    _display = "☼"

    def __init__(self, pX, pY):
        super().__init__(pX, pY)
#ADD WALLS CLASS HERE

class GameManager():
    def __init__(self, pSize):
        self.table = self.createTable(pSize)
        self.size = pSize
        self.choice = None
        self.isEnd = False
        self.bombCount = 1
        self.MAX_BOMB = 1
        self.bombCooldown = 0
        self.BOMB_TIMER = 15

    def display(self):
        self.__refresh()
        i = 0
        while i < game.size:
            line = "│"
            column = "┌"
            j = 0
            while j < game.size:
                if isinstance(self.table[i][j], GameObject):
                    line += " " + self.table[i][j].display() + " "
                else:
                    line += "   "
                column += "───"
                j += 1
            column += "┐ "
            line += "│"
            if i == 0:
                print(column)
            print(line)
            if i == game.size - 1:
                lColumn = list(column)
                column_ = ""
                lColumn[0] = "└"
                lColumn[len(lColumn)-2] = "┘"
                print(column_.join(lColumn))
            i += 1
    
    def __refresh(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def createTable(self, pSize):
        lTable = []
        i = 0
        while i < pSize:
            j = 0
            lTemp = []
            while j < pSize:
                lTemp.append(0)
                j += 1
            lTable.append(lTemp)
            i += 1
        return lTable
    
    def doChoice(self):
        if self.bombCooldown == 0 and self.bombCount > 0:
            self.choice = input("Move : zqsd | Bomb : b | Quit : x > ")
            while self.choice != 'z' and self.choice != 'q' and self.choice != 's' and self.choice != 'd' and self.choice != 'b':
                if self.choice == "x":
                    exit()
                self.choice = input("Move : zqsd | Bomb : b | Quit : x > ")
            if self.choice == "b":
                self.bombCooldown = self.BOMB_TIMER
                self.bombCount -= 1
        else:
            print("Bomb : up in", self.bombCooldown, "moves ")
            self.choice = input("Move : zqsd | Quit : x > ")
            while self.choice != 'z' and self.choice != 'q' and self.choice != 's' and self.choice != 'd':
                if self.choice == "x":
                    exit()
                self.choice = input("Move : zqsd | Quit : x > ")
                
            self.bombCooldown -= 1
            if self.bombCooldown == 0:
                self.bombCount += 1
        
        return self.choice
    
    def gameLoop(self):
        while not self.isEnd:
            self.display()
            self.doChoice()
            player.doAction()
            Enemy.doActionAll()         

            if len(Enemy.list) == 0:
                self.isEnd = True
                self.win()
                return
        self.lose()

    def win(self):
        self.display()
        print("Victory !")
    
    def lose(self):
        self.display()
        print("DEFEAT !")
    def start(self):
        self.display()
        lStart = input("Input anything to play or x to quit > ")
        if lStart == "x":
            exit()
        Enemy.createEnemies(N_ENEMIES)
        game.gameLoop()
        return
#end of GameManager

N_ENEMIES = 10
game = GameManager(10)
player = Player(0, 0)
game.start()

