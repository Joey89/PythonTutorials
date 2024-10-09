import pyautogui #pyautogui and pillow
import psutil
import numpy as np
import cv2
import os
import time
import re
import sys

##
## Set game to 1440x900 and top left of main screen
##
#Constant Game Settings
GAMEPATH = "C:/Program Files (x86)/Battle.net/Battle.net.exe"
CHARSCREENLOGO = "d2rCharScreenLogo.png"
PINDLEMOBS = "pindleMinion.png"
PINDLE = "pindle.png"
PLAYBTN = "playBtn.png"
D2RLOGO = "d2rlogo.png"
PLAYBTNLOGO = "bnetplaybtn.png"
PINDLEPORTAL = "pindleportal.png"
A5WP = "wp_a5.png"
TOWNPORTAL = "townportal.png"
FORCEKEY = "d"
NMDIFFICULTY = ""
NORMDIFFICULTY = ""
RUNCOUNTER=0
STASHEDTHISRUN = False
DEATHDETECTED = False
VarX = 0
VarY = 0
#user config
waitForGameCreationDelay = 5 # 5 sec
gameDiff = "hell" # hell, nightmare or normal
runSelections = ["eldritch", "pindle"]
buffs = ["F", "z"] # skills to buff with in town
safeBuff = ["g"] # swap to this after initial attack, only works for assassin.. swap to fade
character = "assassin" #"hammerdin", "assassin" #character..not yet imp
STASHCONFIG=[ #"e" in stash to represent it should be an empty slot
    ["", "", "", "", "e", "e" ,"e" ,"e", "e", "e"],
    ["", "", "", "", "e", "e" ,"e" ,"e", "e", "e"],
    ["", "", "", "", "e", "e" ,"e" ,"e", "e", "e"],
    ["", "", "", "", "e", "e" ,"e" ,"e", "e", "e"]
]
# assassin config
if character == 'assassin':
    Attack1 = "e" #lightning sentry
    Attack2 = "r" #death sentry
    Attack3 = "y" #mind blast
    UsingFade = False # true if Fade and false for BoS * set in buffs =[]
# hammerdin config

try:
    pyautogui.getAllTitles()   #to get all active titles of windows
    pyautogui.getWindowsWithTitle('Diablo II: Resurrected')[0].moveTo(0,0)  
    pyautogui.getWindowsWithTitle('Diablo II: Resurrected')[0].activate()
except:
    print('***no d2 windows')

# Functions.. eventually import these
def check_if_process_running(process_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            return True
    return False
#end func

def openD2R(gameName):
    os.startfile(gameName)
#end func

def detectCharScreen(CHARSCREENLOGO=CHARSCREENLOGO, PLAYBTN=PLAYBTN):
    try:
        CHARSCREENLOGO = pyautogui.locateOnScreen(CHARSCREENLOGO, grayscale=False, confidence=0.55)
        PLAYBTN = pyautogui.locateOnScreen(PLAYBTN, grayscale=True, confidence=0.75)
        return True
    except pyautogui.ImageNotFoundException:
        print('***failure to find char screen logo and play button FUNC detectCharScreen')
        return False 
#end func

def runCharScreen(CHARSCREENLOGO=CHARSCREENLOGO, PLAYBTN=PLAYBTN):
    # LOCATE IMAGES to detect char screen, Check for D2R firey char screen logo

    try:
        CHARSCREENLOGO = pyautogui.locateOnScreen(CHARSCREENLOGO, grayscale=True, confidence=0.5)
        PLAYBTN = pyautogui.locateOnScreen(PLAYBTN, grayscale=True, confidence=0.95)
    except pyautogui.ImageNotFoundException:
        print('char screen logo not found')
    if(CHARSCREENLOGO and PLAYBTN):
        print('Game State: At Character Screen')
        pyautogui.click(PLAYBTN)
        print("Starting Game: difficulty: %s" % (gameDiff) )
     
        if (gameDiff == "hell"):
            pyautogui.press("h")
        elif (gameDiff == "nightmare"):
                pyautogui.press("n")
        elif (gameDiff == "normal"):
                pyautogui.press("r")
        #endif
        time.sleep(waitForGameCreationDelay) # game wait timer
    else:
        print('failure detecting screen images')
    #endif
#end func

def buffChar(buffsE):
    #comment
    print("Casting in town buffs")
    for buff in buffsE:
        pyautogui.press(buff)
        time.sleep(1)
        pyautogui.rightClick(735,444)
        time.sleep(1.5)
    # end for
#end function

#def healMerc():

def mercIsDead():
    a2Merc = "a2mercimage.png"
    try:
        merc = pyautogui.locateCenterOnScreen(a2Merc, grayscale=False, confidence=0.65, region=(10,10,150,150))
        if(merc):
            #merc found
            print('Merc found')
            return False 
    except:
        print('**Merc not found')
        return True

timesWaitedForQK = 0
def reviveMerc(timesWaitedForQK=0):
    if timesWaitedForQK==0:
        MoveToWPA5()
        pyautogui.moveTo(360, 718)
        pyautogui.press(FORCEKEY)
        time.sleep(1)
        pyautogui.moveTo(274, 189)
        pyautogui.press(FORCEKEY)
        time.sleep(1.5)
        pyautogui.moveTo(274, 189)
        pyautogui.press(FORCEKEY)
        time.sleep(1.5)
    ### Search for Qual-Kehk
    
    #search for Qual
    image_list = ["QualKehk.png", "QualKehk2.png", "QualKehk3.png", "QualKehk4.png", "QualKehk5.png", "QualKehk6.png", "QualKehk.png"]
    if timesWaitedForQK == len(image_list)-1: timesWaitedForQK=1
    timesWaitedForQK+=1
    resmercimg = "resurrectmerc.png"
    try:
        print("trying to locate qual khek..")
        QualK = pyautogui.locateCenterOnScreen(image_list[timesWaitedForQK], grayscale=False, confidence=0.75, region=(10,10,900,600))
        #if(not QualK):continue
        if(QualK):
            pyautogui.moveTo(QualK[0], QualK[1])
            time.sleep(1.5)
            pyautogui.click(QualK[0], QualK[1])
            time.sleep(1)
            try:
                #search for trade
                Resurrect = pyautogui.locateCenterOnScreen(resmercimg, grayscale=False, confidence=0.75, region=(145,145,800,400))
                if(Resurrect):
                    pyautogui.moveTo(Resurrect[0], Resurrect[1])
                    time.sleep(1)
                    pyautogui.click(Resurrect[0], Resurrect[1])
                    time.sleep(1)
                    time.sleep(1)
                    print('Merc revived')
                    leaveGame()# leave game, game will detect you left.. cant easily path anywhere from here
            except:
                print('**unable to find resurect')
                return False
    except:
        time.sleep(.1)
        reviveMerc(timesWaitedForQK)

#sys.exit()
def detectInGame():
    img = "detectInGame.png"
    img_cv = cv2.imread(img)
    try:
        detectInGame = pyautogui.locateCenterOnScreen(img_cv, grayscale=True, confidence=0.60, region=(397, 896, 55, 55))
        if(detectInGame):
            return True
    except:
        print("** not in game")
        detectCharScreen()
        #sys.exit()
    return False
#end func
#detectInGame()

def checkHasPotions():
    time.sleep(1)
    pyautogui.press("`")
    img = "superhealingpot.png"
    img_cv = cv2.imread(img)
    imgMP = "supermanapot.png"
    img_mp =cv2.imread(imgMP)
    try:    ### try to find super pots
        pots = pyautogui.locateCenterOnScreen(img_cv, grayscale=False, confidence=0.45, region=(835, 835, 50, 50))
        time.sleep(.5)
        pots2 = pyautogui.locateCenterOnScreen(img_cv, grayscale=False, confidence=0.45, region=(885, 835, 50, 50))
        time.sleep(.5)
        potsMP = pyautogui.locateCenterOnScreen(img_mp, grayscale=False, confidence=0.45, region=(940, 835, 50, 50))
        time.sleep(.5)
        potsMP2 = pyautogui.locateCenterOnScreen(img_mp, grayscale=False, confidence=0.45, region=(995, 835, 50, 50))
        time.sleep(.5)
        pyautogui.press("`")
        if(pots and pots2 and potsMP and potsMP2):
            print('Have enough pots for now')
            time.sleep(2)
            return True
        else:
            return False
    except:     ### pots not found, try to find greater pots
            try:
                img = "has_pot_screenshot.png"
                img_cv = cv2.imread(img)
                imgMP = "greatermanapot.png"
                img_mp =cv2.imread(imgMP)
                pots = pyautogui.locateCenterOnScreen(img_cv, grayscale=False, confidence=0.45, region=(835, 835, 50, 50))
                time.sleep(.5)
                pots2 = pyautogui.locateCenterOnScreen(img_cv, grayscale=False, confidence=0.45, region=(885, 835, 50, 50))
                time.sleep(.5)
                potsMP = pyautogui.locateCenterOnScreen(img_mp, grayscale=False, confidence=0.45, region=(940, 835, 50, 50))
                time.sleep(.5)
                potsMP2 = pyautogui.locateCenterOnScreen(img_mp, grayscale=False, confidence=0.45, region=(995, 835, 50, 50))
                time.sleep(.5)
                pyautogui.press("`")
                if(pots and pots2 and potsMP and potsMP2):
                    print('Have enough pots for now')
                    time.sleep(2)
                    return True
                else:
                    return False
            except:
                print('**couldnt find hell or NM pots')
                print('**Not enough potions found')
                print(f'Gamemode set to {gameDiff} , nm uses greater, hell uses super.')
                pyautogui.press("`")
                return False
#endfunc

def checkHasTP(): #neeeds work, doesnt woprkk..
    pyautogui.press("q")
    try:
        noTP = pyautogui.locateCenterOnScreen('emptyTP.png', grayscale=False, confidence=0.60, region=(750, 870, 100, 100))
        if(noTP):
            return False
    except:
        print('')
    return True

#end check has hp
def checkHP():# and mp
    screenshot = pyautogui.screenshot( region=(235, 810, 120, 25) ) #last is height
    # Save the screenshot
    screenshot.save("checkHP.png")
    img = "checkHP.png"
    img_cv = cv2.imread(img)
    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
    # define range wanted color in HSV
    lower_val = np.array([0,175,175]) 
    upper_val = np.array([20,255,255]) 
    # Threshold the HSV image - any green color will show up as white
    mask = cv2.inRange(hsv, lower_val, upper_val)
    # if there are any white pixels on mask, sum will be > 0
    hasRed = np.sum(mask)
    if hasRed <= 0:
        print('Low HP! Using healing potion')
        #add check for healing pot, if not use next number
        #if both are empty, buy from malah
        if(RUNCOUNTER%2==0):
            pyautogui.press("1")
        else:
            pyautogui.press("2")
    #######
    ## check mp
    ######
    screenshotMP = pyautogui.screenshot( region=(1070, 806, 120, 45) ) #last is height
    # Save the screenshot
    screenshotMP.save("checkMP.png")
    imgMP = "checkMP.png"
    imgMP_cv = cv2.imread(imgMP)
    hsvMP = cv2.cvtColor(imgMP_cv, cv2.COLOR_BGR2HSV)
    # define range wanted color in HSV
    lower_valMP = np.array([100,125,125]) 
    upper_valMP = np.array([130,255,255]) 
    # Threshold the HSV image - any green color will show up as white
    maskMP = cv2.inRange(hsvMP, lower_valMP, upper_valMP)
    # if there are any white pixels on mask, sum will be > 0
    hasBlue = np.sum(maskMP)
    if hasBlue <= 0:
        print('Low MP! Using Mana potion')
        #add check for healing pot,/nopickup if not use next number #if both are empty, buy from malah
        if(RUNCOUNTER%2==0):
            pyautogui.press("3")
        else:
            pyautogui.press("4")
    # show image 
    # apply mask to image
    #res = cv2.bitwise_and(imgMP_cv,imgMP_cv,mask=maskMP)
    #fin = np.hstack((imgMP_cv,res))
    # display image
    #cv2.imshow("Res", fin)
    #cv2.imshow("Mask", maskMP)
    #v2.waitKey(0)
    #cv2.destroyAllWindows()
#end checkHP()

def Attack(direction="N"):
    checkHP()
    if character == "hammerdin":
        pyautogui.press("x")
        pyautogui.press("e")
        time.sleep(.05)
        # Hold down the 'shift' key
        i = 1
        while i < 9:
            # comment: 
            with pyautogui.hold("capslock"):
                pyautogui.sleep(.05)
                pyautogui.click(150,150) 
            i += 1
    #end hdin attack
    elif character == "assassin":
        attackDelayTimer = .25
        if UsingFade:
            attackDelayTimer = .45
        pyautogui.press(Attack1)
        i = 1
        if(direction=="E"): # Pindle is E
            AX = 950
            AY = 375
            while i<6: # cast lightning sentry 5x times
                pyautogui.rightClick(AX,AY) 
                pyautogui.sleep(attackDelayTimer)
                i+=1

            i=1
            checkHP() # adds a slight delay so removed below .5s this is good here
            pyautogui.press(safeBuff) # cast FADE
            pyautogui.rightClick(AX,AY)

            pyautogui.press(Attack2) # cast death sentry
            while i<2:# cast death sentry 1x times
                pyautogui.sleep(.1)
                pyautogui.rightClick(AX,AY)
                i+=1
            i=1
            j = int(AY)
            k = int(AX)
            checkHP()
            pyautogui.press(Attack3) # cast mind blast
            while i<4:# cast mind blast 3x times
                #j = j  - ( 25 * i )
                #k = k + ( 5 * i )
                pyautogui.sleep(attackDelayTimer)
                pyautogui.rightClick(k,j)
                i+=1 
        elif(direction=="N"): # N is eldritch
            AX = 780
            AY = 392
            # cast 5 traps
            i = 1
            j = int(AY)
            while i<6: # cast lightning sentry 5x times
                j=j-(10*i)
                pyautogui.rightClick(AX,j) 
                pyautogui.sleep(attackDelayTimer)
                i+=1
            i=1
            checkHP() # adds a slight delay so removed below .5s this is good here
            pyautogui.press(safeBuff) # cast FADE
            pyautogui.rightClick(AX,AY)

            pyautogui.press(Attack2) # cast death sentry
            while i<2:# cast death sentry 1x times
                pyautogui.sleep(.1)
                pyautogui.rightClick(AX,AY)
                i+=1
            i=1
            j = int(AY)
            k = int(AX)
            checkHP()
            pyautogui.press(Attack3) # cast mind blast
            while i<4:# cast mind blast 3x times
                j = j  - ( 20 * i )
                k = k + ( 10 * i )
                pyautogui.sleep(.25 + attackDelayTimer)
                pyautogui.rightClick(k,j)
                i+=1 
    #### end assassin attack
#end Attack

def detectInventoryFull():
    return False
#end func 

def stashItems():
    try:
        STASH = "stash_a5.png"
        stash = pyautogui.locateCenterOnScreen(STASH, grayscale=True, confidence=0.7, region=(950, 300, 400, 400))
        if(stash): 
            pyautogui.moveTo(stash[0] + VarX, 
            stash[1]+ VarY)
            time.sleep(1)
            pyautogui.click(stash[0] + VarX, stash[1]+ VarY)
            time.sleep(4)
            #here we are at the stash open screen
            STASHSTARTX  = 920
            STASHSTARTY = 500
            for row in STASHCONFIG:
                for slot in row:
                    if slot == "e":
                        #stash items in empty slot
                        with pyautogui.hold("ctrl"):
                            pyautogui.sleep(.15)
                            pyautogui.click(STASHSTARTX,STASHSTARTY) 
                    STASHSTARTX+=43
                STASHSTARTX=920
                STASHSTARTY+=45
            pyautogui.press('esc')#close stash
            time.sleep(1)
            return True
    except:
        print('*** Error stashing')
    return False
#end func

def sellItems():
    return True
#end func

def MoveToWPA5(click=False):

    if deathScreenDetected():
        print("*** character death detected..trying to grab bod")
        leaveGame()
        return False
    #Path to WP
    print("Running to A5 Waypoint")
    if character == "hammerdin":
        pyautogui.press("r")
        time.sleep(.5)
        pyautogui.moveTo(338 + VarX, 773 + VarY)
        pyautogui.click(404 + VarX, 766 + VarY)
        time.sleep(1.5)
        pyautogui.click(408 + VarX, 710 + VarY)
        time.sleep(1.25)
    elif character == "assassin":
        pyautogui.moveTo(338 + VarX, 704 + VarY)
        pyautogui.click(404 + VarX, 766 + VarY)
        time.sleep(1.5)
        pyautogui.moveTo(408 + VarX, 710 + VarY)
        time.sleep(.25)
        pyautogui.press(FORCEKEY)
        time.sleep(1.25)
    try:
        wayPoint = pyautogui.locateCenterOnScreen(A5WP, grayscale=True, confidence=0.55, region=(150, 300, 800,  600))
        if(wayPoint): 
            pyautogui.moveTo(wayPoint[0] + VarX, wayPoint[1]+ VarY)
            time.sleep(1) 
            if(click):
                pyautogui.click(wayPoint)
                time.sleep(1)
                return True
            else:
                pyautogui.press(FORCEKEY)
                time.sleep(2)
                if RUNCOUNTER%5==0 and RUNCOUNTER>0: # stash every 5 runs?:
                    print('Attempting to stash items')
                    if stashItems() is True:
                        print('stash success')
                return True
        return False
    except:
        print("** Failed getting Waypoint, Leave game and continue runs.. ")
        leaveGame()
#end function

def MoveBackWPA5(click=False):
    #Path to WP froms tash
    print("Running to A5 Waypoint")
    try:
        wayPoint = pyautogui.locateCenterOnScreen(A5WP, grayscale=False, confidence=0.55, region=(90, 360, 400, 400))
        if(wayPoint): 
            pyautogui.moveTo(wayPoint[0] + VarX, wayPoint[1]+ VarY)
            time.sleep(1) 
            if(click):
                pyautogui.click(wayPoint)
                time.sleep(1)
                return True
            else:
                pyautogui.press(FORCEKEY)
                time.sleep(2)

                if RUNCOUNTER%2==0 and RUNCOUNTER>0:
                    print('Attempting to stash items')
                    if stashItems() is True:
                        print('stash success')
                        MoveBackWPA5()
                        return True
        return False
    except:
        print("** Failed getting Waypoint, Leave game and continue runs.. ")
        leaveGame()
#end func

def deathScreenDetected():
    try:
        deathDetected = pyautogui.locateCenterOnScreen("deathscreen.png", grayscale=False, confidence=0.70, region=(470,231,500,400))
        if(deathDetected): 
            #hit esc then leave game
            DEATHDETECTED = True
            pyautogui.press('esc')# leave death screen
            return True
    except:
        #not dead
        print("")
        DEATHDETECTED = False      
        return False
#end func

def clickBody():
    if character == "assassin":
        bodyImg = "assassin_dead.png"
    try:
        deathDetected = pyautogui.locateCenterOnScreen(bodyImg, grayscale=False, confidence=0.55, region=(150,150,1200,600))
        if(deathDetected): 
            #click corpse
            pyautogui.click(deathDetected[0], deathDetected[1])
            time.sleep(1)
            DEATHDETECTED = False 
            print('grabbing corpse.')
    except:
        print('body not found keep looking..')
        clickBody()
#end func

def shop(timesWaited=0):
    #act detect
    if timesWaited==0:
        pyautogui.moveTo(50, 349)
        time.sleep(2)
        pyautogui.press(FORCEKEY)
        pyautogui.moveTo(735, 338)
        time.sleep(2)
        pyautogui.press(FORCEKEY)
        time.sleep(2)
    #search for malah
    image_list = ["malah.png", "malah2.png", "malah3.png", "malah4.png", "malah5.png", "malah6.png", "malah7.png", "malah8.png", "malah9.png", "malah.png"]
    if timesWaited == len(image_list)-1: timesWaited=1
    timesWaited+=1
    healingpot = "superhealingpot.png"
    manapot = "supermanapot.png"
    try:
        print("trying to locate malah..")
        malah = pyautogui.locateCenterOnScreen(image_list[timesWaited], grayscale=False, confidence=0.65, region=(10,10,900,600))
        #if(not malah):continue
        if(malah):
            pyautogui.moveTo(malah[0], malah[1])
            time.sleep(1.5)
            pyautogui.click(malah[0], malah[1])
            time.sleep(1)
            #search for trade
            trade = pyautogui.locateCenterOnScreen('trade.png', grayscale=True, confidence=0.85, region=(50,50,800,500))
            if(trade):
                pyautogui.moveTo(trade[0], trade[1])
                time.sleep(1)
                pyautogui.click(trade[0], trade[1])
                time.sleep(1)
                time.sleep(1)
                with pyautogui.hold("shift"):
                    time.sleep(1)
                    #pyautogui.rightClick(532, 603) # healing pot
                    time.sleep(1)
                    #find healing and shift buy
                    try:
                        healingPot = pyautogui.locateCenterOnScreen(healingpot, grayscale=False, confidence=0.90, region=(10,10,900,600))
                        if(healingPot):
                            #pyautogui.keyDown("shift")#buy healing / MP pots
                            pyautogui.moveTo(healingPot[0], healingPot[1])
                            time.sleep(1.5)
                            pyautogui.rightClick(healingPot[0], healingPot[1])
                            time.sleep(1)
                            pyautogui.moveTo(155, 155)
                            time.sleep(1)
                    except:
                        print( 'failed getting healing pots')
                    time.sleep(1)
                    try:
                        #find mana and shift buy
                        manaPot = pyautogui.locateCenterOnScreen(manapot, grayscale=False, confidence=0.90, region=(10,10,900,600))
                        if(manaPot):
                            #pyautogui.keyDown("shift")#buy healing / MP pots
                            pyautogui.moveTo(manaPot[0], manaPot[1])
                            time.sleep(1.5)
                            pyautogui.rightClick(manaPot[0], manaPot[1])
                            time.sleep(1)
                            pyautogui.moveTo(155, 155)
                            time.sleep(1)
                    except:
                        print( 'failed getting mana pots')
                    time.sleep(1)
                    #find tp scroll and shift buy
                    try:
                        tpScroll = pyautogui.locateCenterOnScreen('tp_scroll.png', grayscale=False, confidence=0.80, region=(10,10,900,600))
                        if(tpScroll):
                            #pyautogui.keyDown("shift")#buy healing / MP pots
                            pyautogui.moveTo(tpScroll[0], tpScroll[1])
                            time.sleep(1.5)
                            pyautogui.rightClick(tpScroll[0], tpScroll[1])
                            time.sleep(1)
                            pyautogui.moveTo(155, 155)
                            time.sleep(1)
                    except:
                        print( 'failed getting tp scrolls')
                    time.sleep(1)
                   # pyautogui.keyUp("shift") ###end shift down
                time.sleep(1)
                #esc out of malah window
                pyautogui.press("esc")
                time.sleep(1)
                pyautogui.click(729, 694)
                time.sleep(1)
                pyautogui.click(979, 609)
                time.sleep(1)
                pyautogui.click(963, 278)
                time.sleep(1)
                pyautogui.click(851, 613)
                time.sleep(1)
                #ready for a5 wp script.. in main..
    except:
        time.sleep(.1)
        shop(timesWaited)
#end func

def leaveGame():
    if deathScreenDetected():
        print("*** character death detected.. going to try to grab body next run")
    #time.sleep(.25)
    pyautogui.press("esc")
    time.sleep(.55)

    leaveGame = pyautogui.locateCenterOnScreen("saveandexit.png", grayscale=False, confidence=0.75, region=(10, 10, 800, 600))
    if(leaveGame):
        pyautogui.moveTo(leaveGame[0] + VarX, leaveGame[1]+ VarY)
        time.sleep(.1)
        pyautogui.leftClick(leaveGame[0] + VarX, leaveGame[1]+ VarY)
        time.sleep(3)
#end leaveGame()

def tp():
    pyautogui.press("q")
    time.sleep(.55)
    pyautogui.rightClick(150,150)
    time.sleep(1)
    try:
        townPortal = pyautogui.locateCenterOnScreen(TOWNPORTAL, grayscale=False, confidence=0.60, region=(10, 10, 1000, 700))
        if(townPortal):
            pyautogui.moveTo(townPortal[0] + VarX, townPortal[1]+ VarY)
            time.sleep(.25)
            pyautogui.leftClick(townPortal[0] + VarX, townPortal[1]+ VarY)
            time.sleep(4)
    except:
        print("**failed to find tp, leaving game..")
        leaveGame()
#end function

def eldritch():
    attackDelayTimer = 0
    if UsingFade:
        attackDelayTimer = .25
    # Eldritch script..
    if( detectInGame() ):
        if (detectInventoryFull()):
            #stashItems()
            sellItems()
            # exit game here to restart loop
        else:
            buffChar(buffs)
            #run eldritch.
            moveToA5 = MoveToWPA5(True)
            if not moveToA5:
                return False
            #move to eldritch
            pyautogui.click(311 + VarX, 304 + VarY)
            time.sleep(1.25 + attackDelayTimer)
            pyautogui.click(603 + VarX, 99 + VarY)
            time.sleep(1 + attackDelayTimer)
            pyautogui.click(708 + VarX, 111 + VarY)
            time.sleep(.25 + attackDelayTimer)
            # Begin attacks
            if( character == "hammerdin"):
                pyautogui.click(708 + VarX, 111 + VarY)
                time.sleep(1)
                pyautogui.click(704 + VarX, 261 + VarY)
                time.sleep(.35)
                checkHP()
                Attack()
                pyautogui.keyUp("capslock")
                pyautogui.moveTo(655 + VarX, 531 + VarY)
                pyautogui.press(FORCEKEY)
                time.sleep(.1)
                Attack()    
            elif character == "assassin":
                pyautogui.click(704 + VarX, 261 + VarY)
                time.sleep(.5)
                checkHP()
                Attack()
                time.sleep(4)#wait for attacks to kill then move forwards
                pyautogui.moveTo(770 + VarX, 257 + VarY)
                pyautogui.press(FORCEKEY)
                time.sleep(.25)
            Loot()
            lastBoxx = len(runSelections)-1
            if runSelections[lastBoxx] == "eldritch":
                print('leave game')
                leaveGame()
            else:
                tp()

def pindle():
    # Pindle script..
    if( detectInGame() ):
        # check inventory.. sell if need too
        if (detectInventoryFull()):
            #stashItems()
            sellItems()
            # exit game here to restart loop
        else:
            buffChar(buffs)
            moveToA5 = MoveToWPA5()
            if not moveToA5:
                return False
            #Path to Pindle
            pyautogui.click(485 + VarX, 783 + VarY)
            time.sleep(2)
            pyautogui.click(485 + VarX, 783 + VarY)
            time.sleep(1.5)
            pyautogui.click(506 + VarX, 545 + VarY)
            time.sleep(1.5)
            try:
                # Click red portal
                portal = pyautogui.locateCenterOnScreen(PINDLEPORTAL, grayscale=False, confidence=0.45, region=(125, 125, 600, 500))
                if(portal): 
                    pyautogui.moveTo(portal[0] + VarX, portal[1]+ VarY)
                    time.sleep(1)

                    pyautogui.leftClick(portal[0] + VarX, portal[1]+ VarY)
                    time.sleep(2)
                #endif
                # Path to pindle
                pyautogui.moveTo(804 + VarX, 181 + VarY)
                pyautogui.press(FORCEKEY)
                time.sleep(1)
                pyautogui.moveTo(1247 + VarX, 176 + VarY)
                pyautogui.press(FORCEKEY)
                time.sleep(1.5)
                pyautogui.moveTo(1304 + VarX, 191 + VarY)
                pyautogui.press(FORCEKEY)
                time.sleep(1.45)
                if(character == "hammerdin"):
                    pyautogui.moveTo(803 + VarX, 275 + VarY)
                    pyautogui.press(FORCEKEY)
                    time.sleep(.75)# should be at entrance way..
                    pyautogui.moveTo(990 + VarX, 356 + VarY)
                    pyautogui.press(FORCEKEY)
                    time.sleep(.15)
                    pyautogui.moveTo(990 + VarX, 356 + VarY)
                    pyautogui.press(FORCEKEY)
                    time.sleep(.1)
                if( character == "assassin"):
                    pyautogui.moveTo(853 + VarX, 300 + VarY)
                    pyautogui.press(FORCEKEY)
                    time.sleep(.25)# should be at entrance way..
                # Detect mobs, force move next to them .. would be nice?
                # Begin attacks
                checkHP()
                if character == "hammerdin":
                    Attack()
                    pyautogui.keyUp("capslock")
                    pyautogui.moveTo(655 + VarX, 531 + VarY)
                    pyautogui.press(FORCEKEY)
                    time.sleep(.1)
                    Attack()
                elif character == "assassin":
                    Attack("E")
                    time.sleep(3.5)
                    pyautogui.moveTo(940 + VarX, 375 + VarY)
                    pyautogui.press(FORCEKEY)
                    time.sleep(.5)
                Loot()
                lastBoxx = len(runSelections)-1
                if runSelections[lastBoxx] == "pindle":
                    print('leave game')
                    leaveGame()
                else:
                    tp()
            except:
                print("** Red Portal wasnt found exiting game. ")
                leaveGame()
        #endif
    #endif
#end function

def Loot():
    pyautogui.press("alt")
    lootRunes()
    checkHP()
    lootUniques()
    lootSets()
    pyautogui.press("alt")
#end func Loot()

def lootRunes():
    print("rune search..")
    #snapshot the screen
    screenshot = pyautogui.screenshot(region=(10, 10, 1300, 700))
    # Save the screenshot
    screenshot.save("region_screenshot.png")
    img = "region_screenshot.png"
    img_cv = cv2.imread(img)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    gSelect = cv2.imread("rune.png")
    result = cv2.matchTemplate(img_cv, gSelect, cv2.TM_CCORR_NORMED)
    threshold = .85
    yloc, xloc = np.where(result>=threshold)
    w = gSelect.shape[1]
    h = gSelect.shape[0]

    count = 0
    for (x, y) in zip(xloc, yloc):
        if(count>=1):
            screenshot = pyautogui.screenshot(region=(10, 10, 1300, 700))
            # Save the screenshot
            screenshot.save("region_screenshot.png")
            img = "region_screenshot.png"
            img_cv = cv2.imread(img)
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            gSelect = cv2.imread("rune.png")
            result = cv2.matchTemplate(img_cv, gSelect, cv2.TM_CCORR_NORMED)

            yloc, xloc = np.where(result>=threshold)
            w = gSelect.shape[1]
            h = gSelect.shape[0]
            for (x, y) in zip(xloc, yloc):
                cv2.rectangle(img_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
                pyautogui.moveTo(x + 5 + (w/2) , y + 5 + (h/2))
                time.sleep(1)
                pyautogui.click(x + 5 + (w/2) , y + 5 +(h/2))
                time.sleep(1)      
        else:
            cv2.rectangle(img_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
            pyautogui.moveTo(x  + 5  + (w/2) , y  + 5 +  (h/2))
            time.sleep(1)
            pyautogui.click(x  + 5 +  (w/2) , y  + 5 + (h/2))
            time.sleep(1)
        count+=1
#end func

def lootSets():
    print("set search..")
    lootScreenShots = ["set.png", "set2.png", "set3.png"]
    #snapshot the screen
    screenshot = pyautogui.screenshot(region=(10, 10, 1300, 700))
    # Save the screenshot
    screenshot.save("region_screenshot.png")
    img = "region_screenshot.png"
    img_cv = cv2.imread(img)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV )
    gSelect = cv2.imread("set1.png")
    result = cv2.matchTemplate(img_cv, gSelect, cv2.TM_CCOEFF_NORMED)
    threshold = .75
    yloc, xloc = np.where(result>=threshold)
    w = gSelect.shape[1]
    h = gSelect.shape[0]

    if not yloc.any():
        gSelect = cv2.imread("set2.png")
        result = cv2.matchTemplate(img_cv, gSelect, cv2.TM_CCOEFF_NORMED)
        yloc, xloc = np.where(result>=threshold) 
        if not yloc.any():
            gSelect = cv2.imread("set3.png")
            result = cv2.matchTemplate(img_cv, gSelect, cv2.TM_CCOEFF_NORMED)
            yloc, xloc = np.where(result>=threshold) 
    count = 0
    nCount = 0
    for (x, y) in zip(xloc, yloc):
        if(count>=1):
            screenshot = pyautogui.screenshot(region=(10, 10, 1300, 700))
            # Save the screenshot
            screenshot.save("region_screenshot.png")
            img = "region_screenshot.png"
            img_cv = cv2.imread(img)
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV )
            gSelect = cv2.imread("set1.png")
            result = cv2.matchTemplate(img_cv, gSelect, cv2.TM_CCOEFF_NORMED)
            yloc2, xloc2 = np.where(result>=threshold)
            w2 = gSelect.shape[1]
            h2 = gSelect.shape[0]
            if not yloc2.any():
                gSelect = cv2.imread("set2.png")
                result = cv2.matchTemplate(img_cv, gSelect, cv2.TM_CCOEFF_NORMED)
                yloc2, xloc2 = np.where(result>=threshold) 

                if not yloc2.any():
                    gSelect = cv2.imread("set3.png")
                    result = cv2.matchTemplate(img_cv, gSelect, cv2.TM_CCOEFF_NORMED)
                    yloc2, xloc2  = np.where(result>=threshold) 
            for (j, i) in zip(xloc2, yloc2):
                if(x>=155 and y>=155):
                    #cv2.rectangle(img_rgb, (j, i), (j + w2, i + h2), (0, 255, 0), 2)
                    pyautogui.moveTo(j  + 10 + (w2/2) , i  + 10 + (h2/2))
                    time.sleep(1)
                    pyautogui.click(j + 10 + (w2/2) , i + 10 + (h2/2))
                    time.sleep(1)  
        else:
            if(x>=155 and y>=155):
                #cv2.rectangle(img_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
                pyautogui.moveTo(x  + 10 +  (w/2) , y + 10 +  (h/2))
                time.sleep(1)
                pyautogui.click(x  + 10+  (w/2) , y  + 10 + (h/2))
                time.sleep(1)  
        count+=1
#end loot sets

def lootUniques():
    print("unique search..")
    #snapshot the screen
    screenshot = pyautogui.screenshot(region=(10, 10, 1300, 700))
    # Save the screenshot
    screenshot.save("region_screenshot.png")
    img = "region_screenshot.png"
    img_cv = cv2.imread(img)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV )
    gSelect = cv2.imread("unique.png")
    result = cv2.matchTemplate(img_cv, gSelect, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    yloc, xloc = np.where(result>=threshold)
    w = gSelect.shape[1]
    h = gSelect.shape[0]
    if not yloc.any():
        gSelect = cv2.imread("unique2.png")
        result = cv2.matchTemplate(img_cv, gSelect, cv2.TM_CCOEFF_NORMED)
        yloc, xloc = np.where(result>=threshold) 
        if not yloc.any():
            gSelect = cv2.imread("unique3.png")
            result = cv2.matchTemplate(img_cv, gSelect, cv2.TM_CCOEFF_NORMED)
            yloc, xloc = np.where(result>=threshold) 
    count = 0
    nCount = 0
    for (x, y) in zip(xloc, yloc):
        if(count>=1):
            screenshot = pyautogui.screenshot(region=(10, 10, 1300, 700))
            # Save the screnshot
            screenshot.save("region_screenshot.png")
            img = "region_screenshot.png"
            img_cv = cv2.imread(img)
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV )
            gSelect = cv2.imread("unique.png")
            result = cv2.matchTemplate(img_cv, gSelect, cv2.TM_CCOEFF_NORMED)
            yloc2, xloc2 = np.where(result>=threshold)
            w2 = gSelect.shape[1]
            h2 = gSelect.shape[0]
            if not yloc2.any():
                gSelect = cv2.imread("unique2.png")
                result = cv2.matchTemplate(img_cv, gSelect, cv2.TM_CCOEFF_NORMED)
                yloc2, xloc2 = np.where(result>=threshold) 

                if not yloc2.any():
                    gSelect = cv2.imread("unique3.png")
                    result = cv2.matchTemplate(img_cv, gSelect, cv2.TM_CCOEFF_NORMED)

                    yloc2, xloc2  = np.where(result>=threshold) 
            for (j, i) in zip(xloc2, yloc2):
                if(x>=155 and y>=155):
                    cv2.rectangle(img_rgb, (j, i), (j + w2, i + h2), (0, 255, 0), 2)
                    pyautogui.moveTo(j  + 10 + (w2/2) , i  + 10 + (h2/2))
                    time.sleep(1)
                    pyautogui.click(j + 10 + (w2/2) , i + 10 + (h2/2))
                    time.sleep(1)  
        else:
            if(x>=155 and y>=155):
                #cv2.rectangle(img_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
                pyautogui.moveTo(x  + 10 +  (w/2) , y + 10 +  (h/2))
                time.sleep(1)
                pyautogui.click(x  + 10+  (w/2) , y  + 10 + (h/2))
                time.sleep(1)  

        count+=1
#end loot uniques

def checkItemPickupDisabled():
    pyautogui.press("enter")
    time.sleep(.5)
    pyautogui.write("/nopickup")
    time.sleep(.5)
    pyautogui.press("enter")
    try:
        disabled = pyautogui.locateOnScreen("pickupdisabled.png", grayscale=True, confidence=0.75, region=(200,700, 150, 150))
        if disabled:
            print('No pickup has been disabled')
    except:
        checkItemPickupDisabled()
#checkItemPickupDisabled()

def runInGameScripts():
    if deathScreenDetected():
        print("*** character death detected..trying to grab bod")
    if DEATHDETECTED:
        clickBody()
    #start of game
    #check potions, buy if none
    checkHP()
    if mercIsDead():
        reviveMerc()
        ## should leave game and reset here.
    elif not checkHasPotions(): # in elif to avoid infinite loop when both runcounter and merc dead
        shop()
    elif RUNCOUNTER%12==0 and RUNCOUNTER>0:
        print(" shopping due to run counter ")
        shop()
    
    checkItemPickupDisabled()

    for run in runSelections:
        checkHP()
        if run == "eldritch":
            print("Starting " + str(run))
            eldritch()
        if run == "pindle":
            print("Starting " + str(run))
            pindle()
#end function

def main():
    ## first part here will be static, trying to detect game state
    #detect if game is open
    GAMEOPEN = check_if_process_running("D2R.exe")
    ONLINELOGO = "onlinelogo.png"
    if(GAMEOPEN):
        try:
            pyautogui.getAllTitles()   #to get all active titles of windows
            pyautogui.getWindowsWithTitle('Diablo II: Resurrected')[0].moveTo(0,0)  
            pyautogui.getWindowsWithTitle('Diablo II: Resurrected')[0].activate()
        except:
            print('no d2 windows found') 
        print('Game open, detecting state.')
        #AT CHAR SCREEN?
        charScreen = detectCharScreen()
        if(charScreen):
            try:
                #CHECK FOR ONLINE / OFFLINE
                ONLINELOGO = pyautogui.locateOnScreen(ONLINELOGO, grayscale=False, confidence=0.85, region=(1000,25, 300, 100))
                if(ONLINELOGO):
                    print('were online')
                    runCharScreen()
                    time.sleep(5)
                    runInGameScripts() #ingame
                    if deathScreenDetected():
                        print("*** character death detected.. exit application")
            except pyautogui.ImageNotFoundException:
                print("Online not found.")
                print('...were offline')
                print('...closing now')
                sys.exit()
        else: 
            # Char screen not detected..
            # Could be in game?, Could be in BNET menu
            print("CharScreen not detected")
            if( detectInGame() ):
                print(" you are in game but have errored,  will try to run in game scripts.. this could be bad")
                runInGameScripts() #ingame
        #endif
    else: # game is not open
        print("not detected")
        #########################
        # Open Bnet and click d2r to char screen
        #########################
        openD2R(GAMEPATH)
        D2LOGO = pyautogui.locateOnScreen(D2RLOGO, grayscale=True, confidence=0.75, region=(0, 0, 500, 500))
        if(D2LOGO):
            pyautogui.click(D2LOGO)
            time.sleep(1)
            # Next click the Play button
            BNetPlayBtn = pyautogui.locateOnScreen(PLAYBTNLOGO, grayscale=True, confidence=0.65, region=(10, 450, 350, 150))
            time.sleep(1)
            if(BNetPlayBtn):
                pyautogui.click(BNetPlayBtn)
                # wait 5 sec, click through
                numberScreens = 4
                for i in range(numberScreens):
                    # comment: 
                    time.sleep(6)
                    pyautogui.click(100, 100)
                # end for
        ##################
        # YOU SHOULD BE AT CHARACTER SCREEN NOW
        ###################
        #AT CHAR SCREEN?
        print('Game open, detecting state.')
        charScreen = detectCharScreen()
        if(charScreen):
            try:
                #CHECK FOR ONLINE
                ONLINELOGO = pyautogui.locateOnScreen(ONLINELOGO, grayscale=False, confidence=0.85, region=(1000,25, 300, 100))
                if(ONLINELOGO):
                    print('were online')
                    runCharScreen()
                    runInGameScripts() #ingame
            except pyautogui.ImageNotFoundException:
                print("Online not found.")
                print('...were offline')
                print('...closing now')
                sys.exit()
        else: 
            print("test")
        #endif

#Loot()
#Attack()

#if deathScreenDetected():
#    print("*** character death detected.. exit application")
#sys.exit()


while True:
    print("Current runs completed: %s" % RUNCOUNTER + " / Starting %i" % int(RUNCOUNTER+1))
    main()
    RUNCOUNTER+=1


