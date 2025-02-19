import pyxinput
import time
import FFX_Xbox
import FFX_Battle
import FFX_Screen
import FFX_core
import FFX_memory
import FFX_Logs

FFXC = FFX_Xbox.FFXC

def engage():
    print("Start egg hunt")
    startTime = time.time()
    checkpoint = 0
    battleCount = 0
    lookingCount = 0
    camCount = 0
    print("Generating Plot file (the X/Y kind)")
    #FFX_Logs.nextPlot()
    #time.sleep(3)
    while FFX_memory.getStoryProgress() < 3251:
        if FFX_Screen.BattleScreen():
            print("Battle engaged - using flee.")
            FFX_Battle.fleeLateGame()
            battleCount += 1
        elif FFX_memory.menuOpen():
            print("Clicking to control.")
            FFXC.set_value('BtnB',1)
            time.sleep(0.035)
            FFXC.set_value('BtnB',0)
            time.sleep(0.035)
        else:
            
            #Move to first egg, while in control.
            complete = 0
            activeEgg = 99
            target = [10,-10]
            moveVersion = 0
            while complete == 0:
            
                if activeEgg == 99:
                    if lookingCount % 200 < 100:
                        target = [20,-20]
                    else:
                        target = [-20,20]
                #print("Building egg array")
                eggArray = FFX_memory.buildEggs()
                currentTime = time.time()
                if activeEgg == 99:
                    for marker in range(10): #Only print active eggs/icicles
                        if activeEgg == 99 and eggArray[marker].goForEgg == True and eggArray[marker].eggLife < 150:
                            activeEgg = marker
                            target = [eggArray[marker].x, eggArray[marker].y]
                            clickTimer = currentTime + 8 #We will hunt for this egg for this many seconds.
                            print("New target egg: ", target)
                elif eggArray[activeEgg].goForEgg == False:
                    activeEgg = 99
                    if lookingCount % 200 < 100:
                        target = [20,-20]
                    else:
                        target = [-20,20]
                elif eggArray[activeEgg].eggLife == 150:
                    activeEgg = 99
                    if lookingCount % 200 < 100:
                        target = [20,-20]
                    else:
                        target = [-20,20]
                if FFX_Screen.BattleScreen():
                    print("Battle engaged - using flee. (Loop break)")
                    complete = 1
                elif FFX_memory.getStoryProgress() > 3250:
                    print("Story progress trigger. Moving on. (loop break)")
                    complete = 1
                else:
                    #print("Movement happening.")
                    #target = [-70,-70]
                    player = FFX_memory.getCoords()
                    cam = FFX_memory.getCamera()
                    #camCount += 1
                    #print(camCount)
                    #if camCount % 20 == 0:
                    #    FFX_Logs.writePlot("TEST")
                    
                    if cam[0] > 1.1:
                        moveVersion = 1
                        if player[0] < target[0] - 2:
                            FFXC.set_value('AxisLy', -1)
                        elif player[0] > target[0] + 2:
                            FFXC.set_value('AxisLy', 1)
                        else:
                            FFXC.set_value('AxisLy', 0)
                        
                        if cam[2] < player[1]:
                            if player[1] < target[1] - 2:
                                FFXC.set_value('AxisLx', 1)
                            elif player[1] + target[1] + 2:
                                FFXC.set_value('AxisLx', -1)
                            else:
                                FFXC.set_value('AxisLx', 0)
                        else:
                            if player[1] < target[1] - 2:
                                FFXC.set_value('AxisLx', -1)
                            elif player[1] + target[1] + 2:
                                FFXC.set_value('AxisLx', 1)
                            else:
                                FFXC.set_value('AxisLx', 0)
                    elif cam[0] < -1:
                        moveVersion = 2
                        if player[0] < target[0] - 2:
                            FFXC.set_value('AxisLy', 1)
                        elif player[0] > target[0] + 2:
                            FFXC.set_value('AxisLy', -1)
                        else:
                            FFXC.set_value('AxisLy', 0)
                        
                        if cam[2] < player[1]:
                            if player[1] < target[1] - 2:
                                FFXC.set_value('AxisLx', -1)
                            elif player[1] + target[1] + 2:
                                FFXC.set_value('AxisLx', 1)
                            else:
                                FFXC.set_value('AxisLx', 0)
                        else:
                            if player[1] < target[1] - 2:
                                FFXC.set_value('AxisLx', 1)
                            elif player[1] + target[1] + 2:
                                FFXC.set_value('AxisLx', -1)
                            else:
                                FFXC.set_value('AxisLx', 0)
                    elif cam[4] < -0.88:
                        moveVersion = 3
                        if player[1] > target[1] + 1.5:
                            FFXC.set_value('AxisLy', 1)
                        elif player[1] < target[1] - 1.5:
                            FFXC.set_value('AxisLy', -1)
                        else:
                            FFXC.set_value('AxisLx', 0)
                        
                        if player[0] < target[0] - 1.5:
                            FFXC.set_value('AxisLx', -1)
                        elif player[0] + target[0] + 1.5:
                            FFXC.set_value('AxisLx', 1)
                        else:
                            FFXC.set_value('AxisLx', 0)
                    elif cam[4] > 0.9:
                        moveVersion = 4
                        if player[1] > target[1] + 1.5:
                            FFXC.set_value('AxisLy', -1)
                        elif player[1] < target[1] - 1.5:
                            FFXC.set_value('AxisLy', 1)
                        else:
                            FFXC.set_value('AxisLx', 0)
                        
                        if player[0] < target[0] - 1.5:
                            FFXC.set_value('AxisLx', 1)
                        elif player[0] + target[0] + 1.5:
                            FFXC.set_value('AxisLx', -1)
                        else:
                            FFXC.set_value('AxisLx', 0)
                    elif cam[0] > 0.01 and cam[4] > 0.01:
                        moveVersion = 5
                        if player[1] - target[1] < player[0] - target[0]:
                            FFXC.set_value('AxisLy', 1)
                        elif player[1] - target[1] > player[0] - target[0]:
                            FFXC.set_value('AxisLy', -1)
                        else:
                            FFXC.set_value('AxisLy', 0)
                        
                        if player[0] + target[0] < player[1] + target[1]:
                            FFXC.set_value('AxisLx', -1)
                        elif player[0] + target[0] + player[1] + target[1]:
                            FFXC.set_value('AxisLx', 1)
                        else:
                            FFXC.set_value('AxisLx', 0)
                    elif cam[0] < 0.01 and cam[4] < 0.01:
                        moveVersion = 6
                        if player[1] - target[1] < player[0] - target[0]:
                            FFXC.set_value('AxisLy', -1)
                        elif player[1] - target[1] > player[0] - target[0]:
                            FFXC.set_value('AxisLy', 1)
                        else:
                            FFXC.set_value('AxisLy', 0)
                        
                        if player[0] + target[0] < player[1] + target[1]:
                            FFXC.set_value('AxisLx', 1)
                        elif player[0] + target[0] + player[1] + target[1]:
                            FFXC.set_value('AxisLx', -1)
                        else:
                            FFXC.set_value('AxisLx', 0)
                    elif cam[0] > 0.01 and cam[4] < 0.01:
                        moveVersion = 7
                        if player[1] - target[1] < player[0] - target[0]:
                            FFXC.set_value('AxisLx', 1)
                        elif player[1] - target[1] > player[0] - target[0]:
                            FFXC.set_value('AxisLx', -1)
                        else:
                            FFXC.set_value('AxisLx', 0)
                        
                        if player[0] + target[0] < player[1] + target[1]:
                            FFXC.set_value('AxisLy', -1)
                        elif player[0] + target[0] + player[1] + target[1]:
                            FFXC.set_value('AxisLy', 1)
                        else:
                            FFXC.set_value('AxisLy', 0)
                    elif cam[0] < 0.01 and cam[4] > 0.01:
                        moveVersion = 8
                        if player[1] - target[1] < player[0] - target[0]:
                            FFXC.set_value('AxisLx', -1)
                        elif player[1] - target[1] > player[0] - target[0]:
                            FFXC.set_value('AxisLx', 1)
                        else:
                            FFXC.set_value('AxisLx', 0)
                        
                        if player[0] + target[0] < player[1] + target[1]:
                            FFXC.set_value('AxisLy', 1)
                        elif player[0] + target[0] + player[1] + target[1]:
                            FFXC.set_value('AxisLy', -1)
                        else:
                            FFXC.set_value('AxisLy', 0)
                    else:
                        moveVersion = 0
                        FFXC.set_value('AxisLx', 0)
                        FFXC.set_value('AxisLy', 0)
                        print("In-between.")
                    
                    #Now if we're close, we want to slow down a bit.
                    if activeEgg != 99 and eggArray[activeEgg].distance < 15 and eggArray[activeEgg].eggLife < 130:
                        time.sleep(0.15)
                        FFXC.set_value('AxisLx', 0)
                        FFXC.set_value('AxisLy', 0)
                        time.sleep(0.15)
                    elif activeEgg == 99:
                        print("Looking for a new egg. Move version: ", moveVersion," | ",lookingCount)
                        lookingCount += 1
                    else:
                        print("Targetting egg: ", moveVersion," | ",target)
                if FFX_memory.userControl() == False:
                    if FFX_Screen.Minimap2():
                        FFX_Xbox.menuB()
                    else:
                        FFXC.set_value('AxisLx', 0)
                        FFXC.set_value('AxisLy', 0)
    endTime = time.time()
    print("End egg hunt")
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    duration = endTime - startTime
    print("Duration: ", str(duration))
    print("Battle count: ", battleCount)
    try:
        FFX_Logs.writeStats("Egg hunt duration in seconds:")
        FFX_Logs.writeStats(str(round(duration,2)))
        FFX_Logs.writeStats("Egg hunt battles:")
        FFX_Logs.writeStats(str(battleCount))
    except:
        print("No log file.")