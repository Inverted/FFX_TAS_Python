import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_memory

FFXC = FFX_Xbox.FFXC
 
def arrival():
    print("Waiting for Yuna/Tidus to stop laughing.")
    FFX_memory.awaitControl()
    print("Now onward to scenes and Mi'ihen skip. Good luck!")
    #FFXC.set_value('AxisLy', 1)
    #FFXC.set_value('AxisLx', -1)
    #time.sleep(1.4)
    #FFXC.set_value('AxisLx', 0)
    #FFX_Xbox.SkipDialog(0.4)
    #FFXC.set_value('AxisLy', 0)
    #print("Touching save sphere. Should be some tutorial dialog popping up.")
    #FFX_Screen.awaitPixel(1105,472,(186, 186, 186))
    #time.sleep(0.1)
    #FFX_Xbox.menuB()
    #time.sleep(0.5)
    #FFX_Xbox.menuB()
    #time.sleep(0.5)
    #FFX_Xbox.menuA()
    #FFX_Xbox.menuB()
    FFXC.set_value('AxisLy', 1)
    #FFXC.set_value('AxisLx', 1)
    #time.sleep(2)
    FFXC.set_value('AxisLx', 0)
    time.sleep(10)
    FFX_Xbox.SkipDialog(7) #No save sphere touched
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToControl() #Auron piercing tutorial
    
    FFX_menu.miihenStart()
    FFX_Battle.healUp(3)
    selfDestruct = 0
    
    checkpoint = 0
    lastCP = 0
    while checkpoint != 100:
        pos = FFX_memory.getCoords()
        if lastCP != checkpoint:
            print("Checkpoint: ", checkpoint)
            lastCP = checkpoint
        if FFX_memory.getMap() == 58 or FFX_memory.getStoryProgress() >= 750:
            checkpoint = 100
        elif FFX_memory.userControl():
            #print(checkpoint)
            if checkpoint == 0:
                if pos[1] > 1348:
                    checkpoint = 3
                else:
                    FFXC.set_value('AxisLy', 1)
                    if pos[1] > 1230 and pos[0] < -44:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[1] > 1230 and pos[0] > -38:
                        FFXC.set_value('AxisLx', -1)
                    elif pos[1] > 1080 and pos[1] < 1120 and pos[0] < -30:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 3:
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                time.sleep(0.3)
                checkpoint = 8
            #elif checkpoint == 6:
            #    FFXC.set_value('AxisLy', 1)
            #    time.sleep(0.05)
            #    FFXC.set_value('AxisLy', 0)
            #    checkpoint = 8
            elif checkpoint == 8:
                if pos[1] > 1359.5:
                    checkpoint = 10
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', 0)
                else:
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(0.08)
                    FFXC.set_value('AxisLy', 0)
                    time.sleep(0.08)
            elif checkpoint == 10: #Waiting for the spear guy.
                FFXC.set_value('BtnB', 1)
                time.sleep(0.03)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.03)
            elif checkpoint == 20:
                if pos[1] < 500:
                    checkpoint = 30
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30:
                if pos[1] > 900:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1) #Diagonal section (Callie)
            elif checkpoint == 40:
                if pos[1] < 700:
                    checkpoint = 50
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1) #Diagonal section (Callie)
            elif checkpoint == 50:
                if pos[1] > 2770:
                    checkpoint = 60
                else:
                    if pos[0] < -25:
                        FFXC.set_value('AxisLy', 0)
                    else:
                        FFXC.set_value('AxisLy', 1)
                    if pos[0] < -20:
                        FFXC.set_value('AxisLx', 1)
                    elif pos[0] > 10:
                        FFXC.set_value('AxisLx', -1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 60:
                if pos[1] > 2900:
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
                    FFX_Xbox.menuB()
            elif checkpoint == 70:
                FFXC.set_value('AxisLy', 1)
                if pos[1] < 900:
                    FFXC.set_value('AxisLx', 1)
                elif pos[0] < -30:
                    FFXC.set_value('AxisLx', 1)
                elif pos[0] > 10:
                    FFXC.set_value('AxisLx', -1)
                else:
                    FFXC.set_value('AxisLx', 0)
        elif FFX_Screen.BattleScreen():
            print("Starting battle")
            if selfDestruct == 0:
                selfDestruct = FFX_Battle.MiihenRoad(selfDestruct)
                if FFX_memory.menuOpen() and FFX_memory.userControl() == False:
                    FFX_memory.clickToControl() # After-battle screen is still open.
            else:
                FFX_Battle.MiihenRoad(selfDestruct)
                if FFX_memory.menuOpen() and FFX_memory.userControl() == False:
                    FFX_memory.clickToControl() # After-battle screen is still open.
            print("Battle complete")
        elif FFX_memory.diagSkipPossible():
            FFX_Xbox.menuB()
        elif checkpoint == 10 and FFX_Screen.PixelTestTol(478,768,(222, 222, 222),5):
            print("Talking to the guy for free spear.")
            time.sleep(1.2)
            FFX_Xbox.menuB() #Close dialog
            time.sleep(0.6)
            FFXC.set_value('BtnB', 1)
            time.sleep(0.035)
            FFXC.set_value('BtnB', 0)
            #while not FFX_memory.menuOpen():
            #    FFXC.set_value('BtnY', 1)
            #    time.sleep(0.035)
            #    FFXC.set_value('BtnY', 0)
            #    time.sleep(0.035)
            #time.sleep(2)
            #FFXC.set_value('BtnA', 1)
            #time.sleep(0.35)
            #FFXC.set_value('BtnA', 0)
            FFXC.set_value('AxisLy', 1)
            time.sleep(0.4)
            FFXC.set_value('BtnB', 1)
            time.sleep(0.05)
            FFXC.set_value('BtnB', 0)
            FFXC.set_value('AxisLy', 0)
            for x in range(50):
                FFXC.set_value('BtnB', 1)
                time.sleep(0.035)
                FFXC.set_value('BtnB', 0)
                time.sleep(0.035)
                
            
            #Now to try to skip into the next scene
            checkpoint = 20
        else:
            FFXC.set_value('AxisLx', 0)
            FFXC.set_value('AxisLy', 0)
    print("Travel agency")
    if FFX_memory.getStoryProgress() < 750:
        FFXC.set_value('AxisLy', 1)
        FFX_Xbox.SkipDialog(10)
        FFXC.set_value('AxisLy', 0)
    return selfDestruct

def midPoint():
    #Should now be at the Mi'ihen travel agency.
    FFX_memory.clickToControl3()
    
    FFXC.set_value('AxisLy', -1)
    time.sleep(0.6)
    FFXC.set_value('AxisLx', -1)
    time.sleep(20)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    
    print("Evening scene")
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(1)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_memory.clickToControl3() #Dude gives us some Lv.1 spheres
    
    print("Let's grab some P.downs")
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.4)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.3)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.menuB()
    time.sleep(1.5)
    FFX_Xbox.menuB()
    time.sleep(1.5)
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    time.sleep(1.5)
    FFX_Xbox.menuB()
    FFX_Xbox.menuDown()
    FFX_Xbox.menuB()
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB() #Extra P.downs
    FFX_Xbox.menuA()
    FFX_Xbox.menuA()
    
    #Start conversation with Rin
    FFXC.set_value('AxisLy', -1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    print("Conversation with Rin")
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', -1)
    FFXC.set_value('AxisLx', -1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    time.sleep(2)
    FFXC.set_value('AxisLy', 0) #Leave the shop
    
    FFX_memory.clickToControl()
    FFXC.set_value('AxisLy', 1)
    time.sleep(3)
    FFXC.set_value('AxisLy', 0)
    FFX_Battle.chocoEater()
    
    FFXC.set_value('AxisLx', 1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(2.5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuA()
    FFX_Xbox.menuB()
    time.sleep(0.4)
    FFX_Xbox.menuUp()
    FFX_Xbox.menuB()
    #FFX_Xbox.touchSaveSphere()
    FFX_memory.awaitControl()
    FFXC.set_value('AxisLx', -1)
    FFXC.set_value('AxisLy', 1)
    time.sleep(0.5)
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)

def lowRoad(selfDestruct): #Starts just after the save sphere.
    print("Starting low road section.")
    if selfDestruct == 0:
        print("Self Destruct has not yet been learned.")
    else:
        print("Self Destruct already learned. Good to go.")
    checkpoint = 0
    while checkpoint != 100:
        if FFX_Screen.BattleScreen():
            print("Starting battle")
            if selfDestruct == 0:
                selfDestruct = FFX_Battle.MiihenRoad(selfDestruct)
            else:
                FFX_Battle.MiihenRoad(selfDestruct)
            print("Battle complete")
        else:
            #print("Lowroad, Checkpoint: ", checkpoint)
            pos = FFX_memory.getCoords()
            if pos == [0.0,0.0]: #This means we've lost control of the character for any reason.
                FFXC.set_value('AxisLx', 0)
                FFXC.set_value('AxisLy', 0)
                FFX_Xbox.menuB()
            elif checkpoint == 0:
                if pos[1] > -350:
                    checkpoint = 10
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 10:
                if pos[0] < 30:
                    checkpoint = 20
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
                    
            elif checkpoint == 20:
                if pos[1] > 0:
                    checkpoint = 30
                else:
                    if pos[0] < -5:
                        FFXC.set_value('AxisLy', 0)
                    else:
                        FFXC.set_value('AxisLy', 1)
                    if pos[0] < 0:
                        FFXC.set_value('AxisLx', 1)
                    else:
                        FFXC.set_value('AxisLx', 0)
            elif checkpoint == 30:
                if pos[0] > 220:
                    checkpoint = 40
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1) #To the next zone
            elif checkpoint == 40:
                if pos[0] > 450:
                    checkpoint = 50
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1)
            elif checkpoint == 50:
                if pos[0] > 600:
                    checkpoint = 60
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 0)
            elif checkpoint == 60:
                FFXC.set_value('AxisLx', 0)
                if selfDestruct != 0:
                    FFXC.set_value('AxisLy', 0)
                    checkpoint = 70
                else:
                    FFXC.set_value('AxisLy', -1)
                    time.sleep(1)
                    FFXC.set_value('AxisLy', 1)
                    time.sleep(1)
                    FFXC.set_value('AxisLy', 0) #Wait for SelfDestruct if needed
            elif checkpoint == 70:
                if pos[1] < 0:
                    checkpoint = 80
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', -1)
            elif checkpoint == 80:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 0)
                time.sleep(5.8)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.5)
                FFXC.set_value('AxisLx', 0)
                checkpoint = 100


def unused2():
    stepCount = 0
    stuckCount = 0
    stepMax = 180
    complete = 0
    while complete == 0:
        if FFX_Screen.BattleScreen():
            print("Starting battle")
            if selfDestruct == 0:
                selfDestruct = FFX_Battle.MiihenRoad(selfDestruct)
                if FFX_memory.menuOpen() and FFX_memory.userControl() == False:
                    FFX_memory.clickToControl() # After-battle screen is still open.
            else:
                FFX_Battle.MiihenRoad(selfDestruct)
                if FFX_memory.menuOpen() and FFX_memory.userControl() == False:
                    FFX_memory.clickToControl() # After-battle screen is still open.
            print("Battle complete")
        elif FFX_Screen.PixelTestTol(788,325,(255, 253, 99),15):
            complete = 1
        elif FFX_Screen.Minimap2():
            stepCount += 1
            print("Mi'ihen pathing: ", stepCount)
            if stepCount < 43:
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < 55:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', -1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif stepCount == 55:
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLx', 0)
            elif stepCount < 115:
                FFXC.set_value('AxisLy', 1)
                if stepCount % 4 < 2:
                    FFXC.set_value('AxisLx', 1)
                time.sleep(0.1)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            else:
                stuckCount += 1
                print("Limit reached.")
                if stuckCount > 20:
                    FFXC.set_value('AxisLy', -1)
                    time.sleep(1.5)
                    FFXC.set_value('AxisLx', 1)
                    time.sleep(1.5)
                    FFXC.set_value('AxisLx', 0)
                    FFXC.set_value('AxisLy', 0)
                    stuckCount = 0
                else:
                    FFXC.set_value('AxisLy', 1)
                    FFXC.set_value('AxisLx', 1)
                    time.sleep(0.3)
                    FFXC.set_value('AxisLx', 0)
                    time.sleep(0.3)
                    FFXC.set_value('AxisLy', 0)
                stepCount -= 1
        elif FFX_Screen.Minimap1():
            stepCount += 1
            print("Mi'ihen pathing: ", stepCount)
            if stepCount < 120:
                FFXC.set_value('AxisLy', 1)
                FFXC.set_value('AxisLx', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
                FFXC.set_value('AxisLx', 0)
            elif selfDestruct == 0: #Make sure we learn Self Destruct
                print("Self Destruct not yet learned. Extra pathing until we get it.")
                stepCount -= 1
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLy', -1)
                time.sleep(0.5)
                FFXC.set_value('AxisLy', 0)
            elif stepCount < stepMax:
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.2)
                FFXC.set_value('AxisLy', 0)
            elif stepCount >= stepMax:
                stepCount -= 1
                FFXC.set_value('AxisLy', 1)
                time.sleep(0.5)
                FFXC.set_value('AxisLy', 0)
    print("Highroad North End. Ready to meet Seymour.")
    
def wrapUp():
    print("Now ready to meet Seymour")
    FFXC.set_value('AxisLy', 1)
    #FFXC.set_value('AxisLx', 1)
    #time.sleep(2.5)
    #FFXC.set_value('AxisLx', 0)
    time.sleep(5)
    FFXC.set_value('AxisLy', 0)
    
    FFX_Screen.clickToMap1()
    FFXC.set_value('AxisLy', 1)
    FFX_Xbox.SkipDialog(4.5)
    FFXC.set_value('AxisLy', 0)
    FFX_Xbox.SkipDialog(2.5)
    FFXC.set_value('AxisLy', -1)
    FFX_Xbox.SkipDialog(12)
    FFXC.set_value('AxisLy', 0)
    FFX_Screen.clickToMap1() #Seymour scene
    FFXC.set_value('AxisLy', 1)
    time.sleep(12)
    FFXC.set_value('AxisLy', 0)