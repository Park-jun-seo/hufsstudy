import pgzrun
import gameinput
import gamemaps
from random import randint
from datetime import datetime
WIDTH = 600
HEIGHT = 660
global lot 
lot =0
player = Actor("pacman_o") # Load in the player Actor image
player.score = 0
player.lives = 3
level = 0
SPEED = 3

def draw(): # Pygame Zero draw function
    global pacDots, player
    screen.blit('header', (0, 0))
    screen.blit('colourmap', (0, 80))
    pacDotsLeft = 0
    for a in range(len(pacDots)):
        if pacDots[a].status == 0:
            pacDots[a].draw()
            pacDotsLeft += 1
        if pacDots[a].collidepoint((player.x, player.y)):
            if pacDots[a].status == 0:
                if pacDots[a].type == 2:
                    for g in range(len(ghosts)): ghosts[g].status = 1200
                else:
                    player.score += 10
            pacDots[a].status = 1
    if pacDotsLeft == 0: player.status = 2
    drawGhosts()
    getPlayerImage()
    player.draw()
    drawLives()
    screen.draw.text("LEVEL "+str(level) , topleft=(10, 10), owidth=0.5, ocolor=(0,0,255), color=(255,255,0) , fontsize=40)
    screen.draw.text(str(player.score) , topright=(590, 20), owidth=0.5, ocolor=(255,255,255), color=(0,64,255) , fontsize=60)
    if player.status == 3: drawCentreText("GAME OVER")
    if player.status == 2: drawCentreText("LEVEL CLEARED!\nPress Enter or Button A\nto Continue")
    if player.status == 1: drawCentreText("CAUGHT!\nPress Enter or Button A\nto Continue")

def drawCentreText(t):
    screen.draw.text(t , center=(300, 434), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=60)

def update(): # Pygame Zero update function
    global player, moveGhostsFlag, ghosts , poss
    
    if player.status == 0:
        if moveGhostsFlag == 4: moveGhosts()
        for g in range(len(ghosts)):
            if ghosts[g].status > 0: ghosts[g].status -= 1
            if ghosts[g].collidepoint((player.x, player.y)):
                if ghosts[g].status > 0:
                    player.score += 100
                    animate(ghosts[g], pos=(290, 370), duration=1/SPEED, tween='linear', on_finished=flagMoveGhosts)
                else:
                    player.lives -= 1
                    sounds.pac2.play()
                    if player.lives == 0:
                        player.status = 3
                        music.fadeout(3)
                    else:
                        if player.x <= 300 and player.y >= 370 :
                            poss = 0
                        else : 
                            poss = 1
                        player.status = 1
                        
                        
                        
        if player.inputActive:
            gameinput.checkInput(player)
            gamemaps.checkMovePoint(player)
            if player.movex or player.movey:
                inputLock()
                sounds.pac1.play()
                animate(player, pos=(player.x + player.movex, player.y + player.movey), duration=1/SPEED, tween='linear', on_finished=inputUnLock)
    if player.status == 1:
        i = gameinput.checkInput(player)
        
        
        if i == 1:
            player.status = 0
            if poss == 1 :
                player.x = 30
                player.y = 630
            elif poss == 0 :
                player.x = 570
                player.y = 110
        
    if player.status == 2:
        i = gameinput.checkInput(player)
        if i == 1:
            init()

def init():
    global player, level
    initDots()
    initGhosts()
    player.x = 290
    player.y = 570
    player.status = 0
    inputUnLock()
    level += 1
    music.play("pm1")
    music.set_volume(0.2)

def drawLives():
    for l in range(player.lives): screen.blit("pacman_o", (10+(l*32),40))

def getPlayerImage():
    global player
    dt = datetime.now()
    a = player.angle
    tc = dt.microsecond%(500000/SPEED)/(100000/SPEED)
    if tc > 2.5 and (player.movex != 0 or player.movey !=0):
        if a != 180:
            player.image = "pacman_c"
        else:
            player.image = "pacman_cr"
    else:
        if a != 180:
            player.image = "pacman_o"
        else:
            player.image = "pacman_or"
    player.angle = a

def drawGhosts():
    for g in range(len(ghosts)):
        if ghosts[g].x > player.x:
            if ghosts[g].status > 200 or (ghosts[g].status > 1 and ghosts[g].status%2 == 0):
                ghosts[g].image = "ghost5"
            else:
                ghosts[g].image = "ghost"+str(g+1)+"r"
        else:
            if ghosts[g].status > 200 or (ghosts[g].status > 1 and ghosts[g].status%2 == 0):
                ghosts[g].image = "ghost5"
            else:
                ghosts[g].image = "ghost"+str(g+1)
        ghosts[g].draw()

def moveGhosts():
    global moveGhostsFlag 
    global gospe
    global far
    far =0
    gospe = 1
    dmoves = [(1,0),(0,1),(-1,0),(0,-1)]
    moveGhostsFlag = 0
    for g in range(len(ghosts)):
        dirs = gamemaps.getPossibleDirection(ghosts[g])
        if inTheCentre(ghosts[g]):
            ghosts[g].dir = 3
        else:
            if ghosts[g].status <= 200:
                if far == 0 :
                    gospe = 0.95
                elif  far ==1 :
                    gospe = 0.95
                followPlayer(g, dirs)

            elif ghosts[g].status > 200:
                if  far == 0 :
                    gospe = 0.8
                elif far == 1 :
                    gospe = 0.7
                followPlayer(g, dirs)
                ambushPlayer(g, dirs)


        if dirs[ghosts[g].dir] == 0 :
            d = -1
            while d == -1:
                rd = randint(0,3)
                if aboveCentre(ghosts[g]) and rd == 1:
                    rd = 0
                if dirs[rd] == 1:
                    d = rd
            ghosts[g].dir = d
        
        animate(ghosts[g], pos=(ghosts[g].x + dmoves[ghosts[g].dir][0]*20, ghosts[g].y + dmoves[ghosts[g].dir][1]*20), duration=gospe/SPEED, tween='linear', on_finished=flagMoveGhosts)
'''
def moveGhosts():
    global moveGhostsFlag
    dmoves = [(1,0),(0,1),(-1,0),(0,-1)]
    moveGhostsFlag = 0
    for g in range(len(ghosts)):
        dirs = gamemaps.getPossibleDirection(ghosts[g])
        if inTheCentre(ghosts[g]):
            ghosts[g].dir = 3
        else:
            if g == 0: followPlayer(g, dirs)
            if g == 1: ambushPlayer(g, dirs)
        
        if dirs[ghosts[g].dir] == 0 :
            d = -1
            while d == -1:
                rd = randint(0,3)
                if aboveCentre(ghosts[g]) and rd == 1:
                    rd = 0
                if dirs[rd] == 1:
                    d = rd
            ghosts[g].dir = d
        animate(ghosts[g], pos=(ghosts[g].x + dmoves[ghosts[g].dir][0]*20, ghosts[g].y + dmoves[ghosts[g].dir][1]*20), duration=1/SPEED, tween='linear', on_finished=flagMoveGhosts)
'''
def followPlayer(g, dirs):
    global lot
    p=0
    pp=0
    m=0
    l=0
    #print('x = %d y = %d '%(player.x ,player.y))
    d = ghosts[g].dir
    if (abs( player.y - ghosts[g].y)>=150) and (abs( player.x - ghosts[g].x)>=150) :
        far =1
    elif (abs( player.y - ghosts[g].y)<=150) and (abs( player.x - ghosts[g].x)<=150) :
        far =0
    while p<4 :
        l=p+1
        while  l<4:
            
            if (abs(ghosts[p].x - ghosts[l].x) <= 0 and abs(ghosts[p].y - ghosts[l].y) <= 0) and ghosts[p].dir == ghosts[l].dir and (abs( player.y - ghosts[g].y)<=50) and (abs( player.x - ghosts[g].x)<=50) :
                if ghosts[p].dir == 0 :
                    ghosts[p].dir = 2
                elif  ghosts[p].dir == 2 :
                    ghosts[p].dir = 0
                elif  ghosts[p].dir == 3 :
                    ghosts[p].dir = 1
                elif  ghosts[p].dir == 1 :
                    ghosts[p].dir = 3
                
            l = l+1
        p = p+1
    if lot == 0 :
        if d == 1 or d == 3 or d == 0 or d == 2:
            if player.x > ghosts[g].x and dirs[0] == 1: ghosts[g].dir = 0
            if player.x < ghosts[g].x and dirs[2] == 1: ghosts[g].dir = 2
            lot = 1


        if d == 0 or d == 2:
            if player.y > ghosts[g].y and dirs[1] == 1 and not aboveCentre(ghosts[g]): ghosts[g].dir = 1
            if player.y < ghosts[g].y and dirs[3] == 1: ghosts[g].dir = 3
            lot = 1
        

    if lot == 1 :
        if d == 0 or d == 2:
            if player.y > ghosts[g].y and dirs[1] == 1 and not aboveCentre(ghosts[g]): ghosts[g].dir = 1
            if player.y < ghosts[g].y and dirs[3] == 1: ghosts[g].dir = 3
            lot == 0
        
        if d == 1 or d == 3 or d == 0 or d == 2:
            if player.x > ghosts[g].x and dirs[0] == 1: ghosts[g].dir = 0
            if player.x < ghosts[g].x and dirs[2] == 1: ghosts[g].dir = 2
            lot == 0

        
    


def ambushPlayer(g, dirs):
    d = ghosts[g].dir
    p=0
    global far
    if (abs( player.y - ghosts[g].y)>=200) and (abs( player.x - ghosts[g].x)>=200) :
        far =1
    elif (abs( player.y - ghosts[g].y)<=200) and (abs( player.x - ghosts[g].x)<=200) :
        far =0


    if not aboveCentre(ghosts[g]): ghosts[g].dir = 1
    
        
    if player.movex > 0 :

        if dirs[0] == 1 :
            ghosts[g].dir = 0
       
        if dirs[0] == 0 :
            if dirs[1] ==1 and dirs[3] ==1 :
                if player.y > ghosts[g].y :
                  ghosts[g].dir = 3
                if player.y < ghosts[g].y :
                    ghosts[g].dir = 1
                if player.y == ghosts[g].y :
                    p = randint(0,1)
                    if p == 0 :
                        ghosts[g].dir = 3
                    else :
                        ghosts[g].dir = 1
                    
            if dirs[1] ==0 and dirs[3] ==1 :
                ghosts[g].dir = 3
            if dirs[1] ==1 and dirs[3] ==0 :
                ghosts[g].dir = 1
    if player.movex < 0 :
        
        if dirs[2] == 1 :
            ghosts[g].dir = 2
       
        if dirs[2] == 0 :
            if dirs[1] ==1 and dirs[3] ==1 :
                if player.y > ghosts[g].y :
                  ghosts[g].dir = 3
                if player.y < ghosts[g].y :
                    ghosts[g].dir = 1
                if player.y == ghosts[g].y :
                    p = randint(0,1)
                    if p == 0 :
                        ghosts[g].dir = 3
                    else :
                        ghosts[g].dir = 1
            if dirs[1] ==0 and dirs[3] ==1 :
                ghosts[g].dir = 3
            if dirs[1] ==1 and dirs[3] ==0 :
                ghosts[g].dir = 1

    if player.movey > 0 :
        
        if dirs[1] == 1 :
            ghosts[g].dir = 1
        if dirs[1] == 0 :
            if dirs[0] ==1 and dirs[2] ==1 :
                if player.x > ghosts[g].x :
                    ghosts[g].dir = 2
                if player.x < ghosts[g].x :
                    ghosts[g].dir = 0
                if player.x == ghosts[g].x :
                    p = randint(0,1)
                    if p == 0 :
                        ghosts[g].dir = 2
                    else :
                        ghosts[g].dir = 0
            if dirs[0] ==0 and dirs[2] ==1 :
                ghosts[g].dir = 2
            if dirs[0] ==1 and dirs[2] ==0 :
                ghosts[g].dir = 0
    
    if player.movey < 0 :
        
        if dirs[3] == 1 :
            ghosts[g].dir = 3
        if dirs[3] == 0 :
            if dirs[0] ==1 and dirs[2] ==1 :
                if player.x > ghosts[g].x :
                    ghosts[g].dir = 2
                if player.x < ghosts[g].x :
                    ghosts[g].dir = 0
                if player.x == ghosts[g].x :
                    p = randint(0,1)
                    if p == 0 :
                        ghosts[g].dir = 2
                    else :
                        ghosts[g].dir = 0
            if dirs[0] ==0 and dirs[2] ==1 :
                ghosts[g].dir = 2
            if dirs[0] ==1 and dirs[2] ==0 :
                ghosts[g].dir = 0
    if (abs( player.y - ghosts[g].y)<=100) and (abs( player.x - ghosts[g].x)<=100) :
        if player.x > ghosts[g].x and dirs[2] == 1: ghosts[g].dir = 2
        if player.x < ghosts[g].x and dirs[0] == 1: ghosts[g].dir = 0
        if player.y > ghosts[g].y and dirs[3] == 1 : ghosts[g].dir = 3
        if player.y < ghosts[g].y and dirs[1] == 1: ghosts[g].dir = 1







def inTheCentre(ga):
    if ga.x > 220 and ga.x < 380 and ga.y > 320 and ga.y < 420:
        return True
    return False

def aboveCentre(ga):
    if ga.x > 220 and ga.x < 380 and ga.y > 300 and ga.y < 320:
        return True
    return False

def flagMoveGhosts():
    global moveGhostsFlag
    moveGhostsFlag += 1

def ghostCollided(ga,gn):
    for g in range(len(ghosts)):
        if ghosts[g].colliderect(ga) and g != gn:
            return True
    return False
    
def initDots():
    global pacDots
    pacDots = []
    a = x = 0
    while x < 30:
        y = 0
        while y < 29:
            d = gamemaps.checkDotPoint(10+x*20, 10+y*20)
            if d == 1:
                pacDots.append(Actor("dot",(10+x*20, 90+y*20)))
                pacDots[a].status = 0
                pacDots[a].type = 1
                a += 1
            if d == 2:
                pacDots.append(Actor("power",(10+x*20, 90+y*20)))
                pacDots[a].status = 0
                pacDots[a].type = 2
                a += 1
            y += 1
        x += 1

def initGhosts():
    global ghosts, moveGhostsFlag
    moveGhostsFlag = 4
    ghosts = []
    g = 0
    while g < 4:
        ghosts.append(Actor("ghost"+str(g+1),(270+(g*20), 370)))
        ghosts[g].dir = randint(0, 3)
        ghosts[g].status = 0
        g += 1

def inputLock():
    global player
    player.inputActive = False

def inputUnLock():
    global player
    player.movex = player.movey = 0
    player.inputActive = True
    
init()
pgzrun.go()
