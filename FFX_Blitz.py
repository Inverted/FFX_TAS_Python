import FFX_Xbox
import time
import FFX_Logs
import FFX_memory

FFXC = FFX_Xbox.FFXC

def blitzMain(forceBlitzWin):
    aurochsFirst = blitzStart()
    
    #if aurochsFirst == False:
    #    while not FFX_memory.blitzBallControl():
    #        FFX_Xbox.menuB()
    
    #time.sleep(5)
    #FFX_Xbox.menuY()
    #time.sleep(1)
    #FFXC.set_value('BtnStart', 1)
    #time.sleep(0.2)
    #FFXC.set_value('BtnStart', 0)
    #time.sleep(0.2)
    ballControl = 0
    manualMovement()
    #if aurochsFirst == True:
    #    ballControl = 1
    #else:
    #    print("First we are going to pass to one of our defensemen.")
    #    clickCounter = 0
    #    while FFX_memory.blitzMenuNum() != 102 and FFX_memory.blitzMenuNum() != 38:
    #        clickCounter += 1
    #        FFX_Xbox.menuX()
    #        if clickCounter % 100 == 0:
    #            print("Attempting to open menu, pass to defense. ", clickCounter / 10)
    #        print("OK now we have the ball. Switching to manual.")
    #        manualMovement()
    
    
    
    
    print("Ready to continue onward.")
    allDefense() #First half actions here.
    
    print("Start of halftime")
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    halfTimeXP()
    if forceBlitzWin == True:
        FFX_memory.blitzballPatriotsStyle()
        #Why not cheat a bit? Works for Bill Belichick. Darth Hoodie anyone?
    
    secondHalfPrep()
    print("End of halftime")
    
    while FFX_memory.getStoryProgress() < 583:    
        if FFX_memory.getMap() != 62: #Wakka scene
            FFXC.set_value('BtnB', 1)
            time.sleep(0.04)
            FFXC.set_value('BtnB', 0)
            time.sleep(0.04)
        else:
            allDefense() #Now with Wakka in the game
    
    print("Game over. Thanks for playing!")
    return True

def blitzStart():
    counter = 0
    ready = 0
    skipCount = 0
    print("Ready to start Blitz match. Just going to do some clicking...")
    while FFX_memory.blitzGameActive() == False:
        if FFX_memory.menuControl():
            skipCount += 1
            print("Dialog skip ", skipCount)
            FFX_Xbox.menuB()
            FFX_Xbox.menuB()
            FFX_Xbox.menuB()
    
    aurochsFirst = True
    time.sleep(12) #Delay so that the coords have time to commit.
    blitzCoords = FFX_memory.blitzCoords()
    print("Coords: ", blitzCoords)
    if blitzCoords[0] > 10:
        print("Aurochs get the ball to start.")
        aurochsFirst = True
    elif blitzCoords[0] < -10:
        print("Opposing team gets the ball to start.")
        aurochsFirst = False
    else:
        print("Could not determine who gets the ball first.")
        aurochsFirst = False
    print("Aurochs got the ball first? ", aurochsFirst)
    return aurochsFirst

def allDefense():
    complete = False
    while complete == False:
        clock = FFX_memory.blitzClockMenu()
        menu = FFX_memory.blitzMenuNum()
        player = FFX_memory.blitzTargetPlayer()
        if FFX_memory.userControl():
            #print("Running")
            FFXC.set_value('AxisLx', 1)
            FFXC.set_value('AxisLy', 0)
            FFXC.set_value('BtnB',1)
            time.sleep(0.035)
            FFXC.set_value('BtnB',0)
            time.sleep(0.035)
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
            if FFX_memory.menuControl() == 1 and menu == 0:
                print("Dialog is open. Probably Goers just scored.")
                FFX_Xbox.menuB()
            elif FFX_memory.diagSkipPossible():
                FFX_Xbox.menuB()
            elif FFX_memory.menuControl() and (menu == 38 or menu == 24 or menu == 102):
                print("Breakthrough menu.")
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                breakOnePassLast()
            elif FFX_memory.getMap() != 62:
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                print("Story progressing")
                complete = True
            #else:
                #print("Nothingness")

def breakOnePassLast():
    FFX_memory.awaitMenuControl()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB() #Break one
    time.sleep(0.05)
    FFX_memory.awaitMenuControl()
    FFX_Xbox.menuUp() #Try to continue the Dribble
    FFX_Xbox.menuB()
    time.sleep(0.8)
    FFX_Xbox.menuUp() #Try to continue the Dribble
    FFX_Xbox.menuB()
    time.sleep(0.05)

def manualMovement():
    print("Attempting to take manual control.")
    
    #breakOnePassLast()
    #time.sleep(2)
    complete = False
    while complete == False:
        menuNum = FFX_memory.blitzMenuNum()
        if FFX_memory.getStoryProgress() > 535:
            print("Could not open the menu.")
            break
        if menuNum == 39 or menuNum == 29:
            print("Formation menu, not quite right.")
            FFX_memory.awaitMenuControl()
            FFX_Xbox.menuUp()
            FFX_Xbox.menuB()
            time.sleep(0.3)
        elif menuNum == 20:
            print("Movement menu has been opened.")
            FFX_memory.awaitMenuControl()
            #time.sleep(180) #Testing only
            FFX_Xbox.menuDown()
            #time.sleep(600) #Testing only
            FFX_Xbox.menuB()
            time.sleep(0.3)
            FFX_memory.awaitMenuControl()
            FFX_Xbox.menuUp()
            FFX_Xbox.menuB()
            time.sleep(0.3)
            complete = True
        elif menuNum == 38:
            print("Something is wrong. Break-through menu is open.")
            FFX_Xbox.menuB()
            time.sleep(5)
        else:
            player = FFX_memory.blitzTargetPlayer()
            if player == 12 or player == 18:
                print("Opposing team has the ball.")
                time.sleep(0.5)
            else:
                FFX_Xbox.menuY()
                print("Attempting to open menu.")

def halfTimeXP():
    print("Now it's halftime.")
    while FFX_memory.getStoryProgress() < 560:
        FFX_Xbox.menuB()

def secondHalfPrep():
    print("Setting up for second half.")
    while FFX_memory.blitzClockMenu() != 187:
        time.sleep(0.02)
    time.sleep(5)
    FFX_Xbox.menuA()
    FFX_Xbox.menuB()
    time.sleep(0.8)
    FFX_Xbox.menuA()
    FFX_Xbox.menuB()
    FFX_Xbox.SkipDialog(3)
    print("Ready to go.")