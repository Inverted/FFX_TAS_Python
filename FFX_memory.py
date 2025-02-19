import struct
import FFX_Xbox
import time
import FFX_Screen
FFXC = FFX_Xbox.FFXC

def float_from_integer(integer):
    return struct.unpack('!f', struct.pack('!I', integer))[0]

def start():
    global process
    global xPtr
    global yPtr
    global coordsCounter
    coordsCounter = 0
    from ReadWriteMemory import ReadWriteMemory

    rwm = ReadWriteMemory()
    print("Memory module opened:")
    print(rwm)
    process = rwm.get_process_by_name('FFX.exe')

    print("Process now captured for FFX (reading memory)")
    print(process)
    process.open()
    print(process.__dict__)
    print(process.pid)
    
    global baseValue
    try:
        import FFX_zz_rootMem
        print("Process Modules:")
        baseValue = FFX_zz_rootMem.ListProcessModules(process.pid)
        print("Process Modules complete")
        #testValue = FFX_zz_rootMem.GetBaseAddr(process.pid,b'FFX.exe')
        print("Dynamically determined memory address: ",hex(baseValue))
    except Exception as errCode:
        print("Could not get memory address dynamically. ", errCode)
        baseValue = 0x00FF0000

def battleActive():
    global baseValue
    key = baseValue + 0x00F3C8FC
    if process.readBytes(key,1) == 1:
        return True
    else:
        return False

def battleMenuCursor():
    global baseValue
    key = baseValue + 0x00F3F77B
    if process.readBytes(key,1) == 0:
        return 255
    else:
        key = baseValue + 0x00F3C926
        return process.readBytes(key,1)

def battleScreen():
    if mainBattleMenu():
        global baseValue
        #key = baseValue + 0x00F3C9EF
        #if process.readBytes(key,1) == 0:
        #    return False
        if battleMenuCursor() == 255:
            return False
        else:
            time.sleep(0.05)
            return True
    else:
        return False
    
def battleCursor2():
    global baseValue
    key = baseValue + 0x00F3CA01
    if process.readBytes(key,1) != 0:
        key = baseValue + 0x00F3CA0E
        return process.readBytes(key,1)
    else:
        return 255

def mainBattleMenu():
    global baseValue
    key = baseValue + 0x00F3C911
    if process.readBytes(key,1) > 0:
        return True
    else:
        return False

def otherBattleMenu():
    global baseValue
    key = baseValue + 0x00F3CA01
    if process.readBytes(key,1) > 0:
        return True
    else:
        return False

def battleTargetId():
    global baseValue
    key = baseValue + 0x00F3D1B4
    return process.readBytes(key,1)

def userControl():
    global baseValue
    #Auto updating via reference to the baseValue above
    global xPtr
    global yPtr
    xPtr = baseValue + 0x0084DED0
    yPtr = baseValue + 0x0084DED8
    coord1 = process.get_pointer(xPtr)
    x = float_from_integer(process.read(coord1))
    coord2 = process.get_pointer(yPtr)
    y = float_from_integer(process.read(coord2))
    
    if [x,y] == [0.0,0.0]:
        return False
    else:
        return True

def awaitControl():
    waitCounter = 0
    print("Awaiting control (no clicking)")
    while not userControl():
        waitCounter += 1
        if waitCounter % 100000 == 0:
            print("Awaiting control - ", waitCounter / 100000)
    time.sleep(0.05)
    return True

def clickToControl():
    waitCounter = 0
    print("Awaiting control (clicking)")
    while not userControl():
        FFXC.set_value('BtnB', 1)
        time.sleep(0.04)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.04)
        waitCounter += 1
        if waitCounter % 100 == 0:
            print("Awaiting control - ", waitCounter / 100)
    time.sleep(0.05)
    return True

def clickToControl2():
    waitCounter = 0
    print("Awaiting control (clicking)")
    while not userControl():
        FFXC.set_value('BtnB', 1)
        time.sleep(0.04)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.04)
        waitCounter += 1
        if waitCounter % 100 == 0:
            print("Awaiting control - ", waitCounter / 100)
    time.sleep(0.05)
    return True

def clickToControl3():
    waitCounter = 0
    print("Awaiting control (clicking)")
    while not userControl():
        if battleScreen():
            break
        elif diagSkipPossible():
            FFXC.set_value('BtnB', 1)
            time.sleep(0.04)
            FFXC.set_value('BtnB', 0)
            time.sleep(0.04)
        elif menuOpen():
            FFXC.set_value('BtnB', 1)
            time.sleep(0.04)
            FFXC.set_value('BtnB', 0)
            time.sleep(0.04)
        else:
            time.sleep(0.05)
        waitCounter += 1
        if waitCounter % 100 == 0:
            print("Awaiting control - ", waitCounter / 100)
    time.sleep(0.05)
    return True

def clickToControlSpecial():
    waitCounter = 0
    print("Awaiting control (clicking)")
    while not userControl():
        FFXC.set_value('BtnB', 1)
        FFXC.set_value('BtnY', 1)
        time.sleep(0.035)
        FFXC.set_value('BtnB', 0)
        FFXC.set_value('BtnY', 0)
        time.sleep(0.035)
        waitCounter += 1
        if waitCounter % 100 == 0:
            print("Awaiting control - ", waitCounter / 100)
    time.sleep(0.05)
    return True

def clickToEvent():
    while userControl():
        FFXC.set_value('BtnB', 1)
        time.sleep(0.04)
        FFXC.set_value('BtnB', 0)
        time.sleep(0.04)
    time.sleep(0.2)

def awaitEvent():
    while userControl():
        time.sleep(0.05)

def getCoords():
    global process
    global baseValue
    #Auto updating via reference to the baseValue above
    global xPtr
    global yPtr
    global coordsCounter
    coordsCounter += 1
    xPtr = baseValue + 0x0084DED0
    yPtr = baseValue + 0x0084DED8
    #xPtr = 0x012DDED0
    #yPtr = 0x012DDED8
    coord1 = process.get_pointer(xPtr)
    x = float_from_integer(process.read(coord1))
    coord2 = process.get_pointer(yPtr)
    y = float_from_integer(process.read(coord2))
    #if [x,y] != [0.0,0.0]:
        #if coordsCounter % 1000 == 99:
            #print("Coordinates check: ")
            #print(str(x).format(24), " | ",str(y).format(24))
            #xPtr = baseValue + 0x0084DED0
    
    return [x,y]

def getCamera():
    global baseValue
    angle = baseValue + 0x008A86B8
    z = baseValue + 0x008A86F0
    x = baseValue + 0x008A86F8
    y = baseValue + 0x008A8700
    angle2 = baseValue + 0x008A86C0
    
    key = process.get_pointer(angle)
    angleVal = round(float_from_integer(process.read(key)),2)
    key = process.get_pointer(x)
    xVal = round(float_from_integer(process.read(key)),2)
    key = process.get_pointer(y)
    yVal = round(float_from_integer(process.read(key)),2)
    key = process.get_pointer(z)
    zVal = round(float_from_integer(process.read(key)),2)
    key = process.get_pointer(angle2)
    angleVal2 = round(float_from_integer(process.read(key)),2)
    
    retVal = [angleVal,xVal,yVal,zVal, angleVal2]
    #print("Camera details: ", retVal)
    return retVal

def getHP():
    global baseValue
    #Out of combat HP only
    
    coord = baseValue + 0x00D32078
    HP_Tidus = process.read(coord)

    coord = baseValue + 0x00D3210C
    HP_Yuna = process.read(coord)

    coord = baseValue + 0x00D321A0
    HP_Auron = process.read(coord)

    coord = baseValue + 0x00D32234
    HP_Kimahri = process.read(coord)

    coord = baseValue + 0x00D322C8
    HP_Wakka = process.read(coord)

    coord = baseValue + 0x00D3235C
    HP_Lulu = process.read(coord)

    coord = baseValue + 0x00D323F0
    HP_Rikku = process.read(coord)

    return [HP_Tidus, HP_Yuna, HP_Auron, HP_Kimahri, HP_Wakka, HP_Lulu, HP_Rikku]

def getOrder():
    global baseValue
    #Out of combat HP only
    
    coord = baseValue + 0x00D307E8
    pos1 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307E9
    pos2 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EA
    pos3 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EB
    pos4 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EC
    pos5 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307ED
    pos6 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EE
    pos7 = process.readBytes(coord,1)
    
    formation = [255, pos1, pos2, pos3, pos4, pos5, pos6, pos7]
    print("Party formation: ", formation)
    return formation

def getOrderSix():
    global baseValue
    #Out of combat HP only
    
    coord = baseValue + 0x00D307E8
    pos1 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307E9
    pos2 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EA
    pos3 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EB
    pos4 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EC
    pos5 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307ED
    pos6 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EE
    pos7 = process.readBytes(coord,1)
    
    formation = [pos1, pos2, pos3, pos4, pos5, pos6, pos7]
    while 255 in formation:
        formation.remove(255)
    print("Party formation: ", formation)
    return formation

def getOrderSeven():
    global baseValue
    #Out of combat HP only
    
    coord = baseValue + 0x00D307E8
    pos1 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307E9
    pos2 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EA
    pos3 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EB
    pos4 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EC
    pos5 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307ED
    pos6 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EE
    pos7 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307EF
    pos8 = process.readBytes(coord,1)
    coord = baseValue + 0x00D307F0
    pos9 = process.readBytes(coord,1)
    
    formation = [pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9]
    print("Party formation, non-clean:", formation)
    formation.remove(255)
    formation.remove(255)
    print("Party formation, cleaned: ", formation)
    return formation

def getPhoenix():
    global baseValue
    
    key = getItemSlot(6)
    pDowns = getItemCountSlot(key)
    print("Phoenix Down count: ", pDowns)
    return pDowns

def getPower():
    global baseValue
    
    key = getItemSlot(70)
    power = getItemCountSlot(key)
    print("Power spheres: ", power)
    return power

def setPower(qty):
    global baseValue
    
    slot = getItemSlot(70)
    key = baseValue + itemCountAddr(slot)
    process.writeBytes(key, qty, 1)
    power = getPower()
    return power

def getSpeed():
    global baseValue
    
    key = getItemSlot(72)
    speed = getItemCountSlot(key)
    print("Speed spheres: ", speed)
    return speed

def setSpeed(qty):
    global baseValue
    
    slot = getItemSlot(72)
    key = baseValue + itemCountAddr(slot)
    process.writeBytes(key, qty, 1)
    speed = getSpeed()
    return speed

def getBattleHP():
    global baseValue
    
    key = baseValue + 0x00F3F7A4
    hp1 = process.read(key)
    key = baseValue + 0x00F3F834
    hp2 = process.read(key)
    key = baseValue + 0x00F3F8C4
    hp3 = process.read(key)
    hpArray = [0, hp1, hp2, hp3]
    print("HP values: ", hpArray)
    return hpArray

def getBattleNum():
    global baseValue
    
    key = baseValue + 0x00D2A8EC
    formation = process.read(key)
    
    #print("Battle Number: ", formation)
    return formation

def getActiveBattleFormation():
    global baseValue

    key = baseValue + 0x00F3F76C
    char1 = process.readBytes(key, 1)
    key = baseValue + 0x00F3F76E
    char2 = process.readBytes(key, 1)
    key = baseValue + 0x00F3F770
    char3 = process.readBytes(key, 1)

    battleForm = [char1, char2, char3]
    if 255 in battleForm:
        while 255 in battleForm:
            battleForm.remove(255)
    return battleForm

def getBattleFormation():
    global baseValue
    
    key = baseValue + 0x00F3F76C
    char1 = process.readBytes(key,1)
    key = baseValue + 0x00F3F76E
    char2 = process.readBytes(key,1)
    key = baseValue + 0x00F3F770
    char3 = process.readBytes(key,1)
    key = baseValue + 0x00D2C8A3
    char4 = process.readBytes(key,1)
    key = baseValue + 0x00D2C8A4
    char5 = process.readBytes(key,1)
    key = baseValue + 0x00D2C8A5
    char6 = process.readBytes(key,1)
    key = baseValue + 0x00D2C8A6
    char7 = process.readBytes(key,1)
    
    battleForm = [char1, char2, char3, char4, char5, char6, char7]
    if 255 in battleForm:
        while 255 in battleForm:
            battleForm.remove(255)
    return battleForm

def getBattleCharSlot(charNum):
    battleForm = getBattleFormation()
    try:
        if battleForm[0] == charNum:
            return 1
        if battleForm[1] == charNum:
            return 2
        if battleForm[2] == charNum:
            return 3
        if battleForm[3] == charNum:
            return 4
        if battleForm[4] == charNum:
            return 5
        if battleForm[5] == charNum:
            return 6
        if battleForm[6] == charNum:
            return 7
    except:
        return 0

def getBattleCharTurn():
    global baseValue
    
    key = baseValue + 0x00D36A68
    battleCharacter = process.read(key)
    return battleCharacter

def getSLVLYuna():
    global baseValue
    #Out of combat HP only
    
    coord = baseValue + 0x00D32104
    return process.read(coord)

def getSLVLKim():
    global baseValue
    #Out of combat HP only
    
    coord = baseValue + 0x00D3222C
    return process.read(coord)

def getSLVLWakka():
    global baseValue
    #Out of combat HP only
    
    key = baseValue + 0x00D322E7
    sLvl = process.readBytes(key,1)
    print("Wakka current Slvl", sLvl)
    return sLvl

def itemAddress(num):
    if num == 1:
        return 0x00D3095C
    if num == 2:
        return 0x00D3095E
    if num == 3:
        return 0x00D30960
    if num == 4:
        return 0x00D30962
    if num == 5:
        return 0x00D30964
    if num == 6:
        return 0x00D30966
    if num == 7:
        return 0x00D30968
    if num == 8:
        return 0x00D3096A
    if num == 9:
        return 0x00D3096C
    if num == 10:
        return 0x00D3096E
    if num == 11:
        return 0x00D30970
    if num == 12:
        return 0x00D30972
    if num == 13:
        return 0x00D30974
    if num == 14:
        return 0x00D30976
    if num == 15:
        return 0x00D30978
    if num == 16:
        return 0x00D3097A
    if num == 17:
        return 0x00D3097C
    if num == 18:
        return 0x00D3097E
    if num == 19:
        return 0x00D30980
    if num == 20:
        return 0x00D30982
    if num == 21:
        return 0x00D30984
    if num == 22:
        return 0x00D30986
    if num == 23:
        return 0x00D30988
    if num == 24:
        return 0x00D3098A
    if num == 25:
        return 0x00D3098C
    if num == 26:
        return 0x00D3098E
    if num == 27:
        return 0x00D30990
    if num == 28:
        return 0x00D30992
    if num == 29:
        return 0x00D30994
    if num == 30:
        return 0x00D30996

def getItemsOrder():
    global baseValue
    items = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    for x in range(30):
        address = itemAddress(x + 1)
        key = baseValue + address
        item = process.readBytes(key,1)
        items[x + 1] = item

    print(items)
    return items

def getUseItemsOrder():
    itemArray = getItemsOrder()
    x = 1
    while x < len(itemArray):
        print("x = %d" % x)
        try:
            if itemArray[x] == 20:
                print("Al Bhed pots, disregard.")
                x += 1
            elif itemArray[x] < 23:
                del itemArray[x]
            elif itemArray[x] > 69:
                del itemArray[x]
            else:
                x += 1
        except:
            x += 1
        print(itemArray)
    print("Use command, item order:")
    print(itemArray)
    return itemArray

def getUseItemsSlot(itemNum):
    items = getUseItemsOrder()
    x = 1
    while x < len(items):
        #print(items[x + 1], " | ", itemNum)
        if items[x] == itemNum:
            return x
        x += 1
    return 255

def getThrowItemsOrder():
    itemArray = getItemsOrder()
    x = 1
    while x < len(itemArray):
        try:
            if itemArray[x] > 15:
                itemArray.remove(itemArray[x])
            else:
                x += 1
        except:
            x += 1
    print("Throw Item command, item order:")
    print(itemArray)
    return itemArray

def getThrowItemsSlot(itemNum):
    items = getThrowItemsOrder()
    x = 1
    while x < len(items):
        #print(items[x + 1], " | ", itemNum)
        if items[x] == itemNum:
            print("Desired item ", itemNum, " is in slot ", x)
            return x
        x += 1
    return 255

def getItemSlot(itemNum):
    items = getItemsOrder()
    for x in range(30):
        #print(items[x + 1], " | ", itemNum)
        if items[x + 1] == itemNum:
            return (x + 1)
    return 255

def checkItemsMacalania():
    bombCore = 0
    lMarble = 0
    fScale = 0
    aWind = 0
    grenade = 0
    lunar = 0
    light = 0
    
    bombCore = getItemSlot(27)
    lMarble = getItemSlot(30)
    fScale = getItemSlot(32)
    aWind = getItemSlot(24)
    grenade = getItemSlot(35)
    lunar = getItemSlot(56)
    light = getItemSlot(57)
    
    #Set MaxSpot to one more than the last undesirable item
    if light - lunar != 1:
        maxSpot = light
    elif lunar - grenade != 1:
        maxSpot = lunar
    elif grenade - aWind != 1:
        maxSpot = grenade
    elif aWind - fScale != 1:
        maxSpot = aWind
    elif fScale - lMarble != 1:
        maxSpot = fScale
    elif lMarble - bombCore != 1:
        maxSpot = lMarble
    else:
        maxSpot = bombCore
        
    retVal = [bombCore, lMarble, fScale, aWind, grenade, lunar, light, maxSpot]
    print("Returning values: ", retVal)
    return retVal

def itemCountAddr(num):
    if num == 1:
        return 0x00D30B5C
    if num == 2:
        return 0x00D30B5D
    if num == 3:
        return 0x00D30B5E
    if num == 4:
        return 0x00D30B5F
    if num == 5:
        return 0x00D30B60
    if num == 6:
        return 0x00D30B61
    if num == 7:
        return 0x00D30B62
    if num == 8:
        return 0x00D30B63
    if num == 9:
        return 0x00D30B64
    if num == 10:
        return 0x00D30B65
    if num == 11:
        return 0x00D30B66
    if num == 12:
        return 0x00D30B67
    if num == 13:
        return 0x00D30B68
    if num == 14:
        return 0x00D30B69
    if num == 15:
        return 0x00D30B6A
    if num == 16:
        return 0x00D30B6B
    if num == 17:
        return 0x00D30B6C
    if num == 18:
        return 0x00D30B6D
    if num == 19:
        return 0x00D30B6E
    if num == 20:
        return 0x00D30B6F
    if num == 21:
        return 0x00D30B70
    if num == 22:
        return 0x00D30B71
    if num == 23:
        return 0x00D30B72
    if num == 24:
        return 0x00D30B73
    if num == 25:
        return 0x00D30B74
    if num == 26:
        return 0x00D30B75
    if num == 27:
        return 0x00D30B76
    if num == 28:
        return 0x00D30B77
    if num == 29:
        return 0x00D30B78
    if num == 30:
        return 0x00D30B79

def getItemsCount():
    global baseValue
    itemCounts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    for x in range(30):
        address = itemCountAddr(x + 1)
        key = baseValue + address
        itemCount = process.readBytes(key,1)
        itemCounts[x + 1] = itemCount

    print(itemCounts)
    return itemCounts

def getItemCountSlot(itemSlot):
    items = getItemsCount()
    for x in range(30):
        if itemSlot == x + 1:
            print("Number of this item: ", items[x + 1])
            return items[x + 1]
    return 0

def getGilvalue():
    global baseValue
    key = baseValue + 0x00D307D8
    return process.read(key)

def setGilvalue(newValue):
    global baseValue
    key = baseValue + 0x00D307D8
    return process.write(key, newValue)

def rikkuODItems(battle):
    #This function gets the item slots for each item, swaps if they're backwards,
    # and then moves the cursor to each item and presses B when we reach it.
    cursor = 1
    if battle == 'Evrae':
        item1 = getItemSlot(94)
        print("Luck sphere in slot: ", item1)
        item2 = getItemSlot(100)
        print("Map in slot: ", item2)
    elif battle == 'Flux':
        item1 = getItemSlot(35)
        print("Grenade in slot: ", item1)
        item2 = getItemSlot(85)
        print("HP Sphere in slot: ", item2)
    elif battle == 'trio':
        item1 = 108
        item2 = 108
        print("Wings are in slot: ", item1)
    elif battle == 'crawler':
        item1 = getItemSlot(30)
        print("Lightning Marble in slot: ", item1)
        item2 = getItemSlot(85)
        print("Mdef Sphere in slot: ", item2)
    elif battle == 'spherimorph1':
        item1 = getItemSlot(24)
        print("Arctic Wind in slot: ", item1)
        item2 = getItemSlot(90)
        print("Mag Sphere in slot: ", item2)
    elif battle == 'spherimorph2':
        item1 = getItemSlot(32)
        print("Fish Scale in slot: ", item1)
        item2 = getItemSlot(90)
        print("Mag Sphere in slot: ", item2)
    elif battle == 'spherimorph3':
        item1 = getItemSlot(30)
        print("Lightning Marble in slot: ", item1)
        item2 = getItemSlot(90)
        print("Mag Sphere in slot: ", item2)
    elif battle == 'spherimorph4':
        item1 = getItemSlot(27)
        print("Bomb Core in slot: ", item1)
        item2 = getItemSlot(90)
        print("Mag Sphere in slot: ", item2)

    if item1 > item2: #Quick bubble sort
        item3 = item2
        item2 = item1
        item1 = item3
    
    if item1 % 2 == 0: #First item is in the right-hand column
        FFX_Xbox.menuRight()
        cursor += 1
    
    while cursor < item1:
        FFX_Xbox.menuDown()
        cursor += 2
    
    FFX_Xbox.menuB() #We should now have selected the first item.
    
    if item1 % 2 != item2 % 2: #First and second items are on different columns
        print("Items are in opposing columns. Switching columns.")
        if item1 % 2 == 0:
            FFX_Xbox.menuLeft()
            FFX_Xbox.menuDown()
        else:
            FFX_Xbox.menuRight()
        cursor += 1
    
    if cursor == item2:
        FFX_Xbox.menuB() #Cursor starts on item 2. Only occurs if opposite columns.
    else:
        while cursor < item2:
            FFX_Xbox.menuDown()
            cursor += 2
        FFX_Xbox.menuB() #Cursor is now on item 2.


def getOverdriveValue(character):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character) + 0x5BC

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    return retVal


def petrifiedstate(character):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character) + 0x606

    key = basePointerAddress + offset
    retVal = process.readBytes(key, 1)

    if retVal % 8 >= 4:
        print("Character %d is petrified" % character)
        return True
    else:
        print("Character %d is not petrified" % character)
        return False

def confusedState(character):
    global process
    global baseValue
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    offset = (0xf90 * character)+0x607

    key = basePointerAddress + offset
    retVal = process.readBytes(key,1)

    if retVal % 2 == 1:
        print("Character %d is confused" % character)
        return True
    else:
        print("Character %d is not confused" % character)
        return False

def confusedStateByPos(position):
    posArray = getBattleFormation()
    x = 0
    if position in posArray:
        if posArray[x] == position:
            return confusedState(posArray[x])
        else:
            x += 1

def getEnemyCurrentHP():
    global process
    global baseValue
    enemyNum = 20
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    
    while enemyNum < 27:
        offset1 = (0xf90 * enemyNum)+0x594
        key1 = basePointerAddress + offset1
        offset2 = (0xf90 * enemyNum)+0x5D0
        key2 = basePointerAddress + offset2
        if enemyNum == 20:
            maxHP = [process.readBytes(key1,4)]
            currentHP = [process.readBytes(key2,4)]
        else:
            nextHP = process.readBytes(key1,4)
            if nextHP != 0:
                maxHP.append(nextHP)
                currentHP.append(process.readBytes(key2,4))
        enemyNum += 1
    print("Enemy HP max values:")
    print(maxHP)
    print("Enemy HP current values:")
    print(currentHP)
    return currentHP

def setEnemyCurrentHP(numToSet, newHP):
    getEnemyCurrentHP()
    global process
    global baseValue
    numToSet = numToSet + 20
    enemyNum = 20
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    
    while enemyNum < 25:
        offset1 = (0xf90 * enemyNum)+0x594
        key1 = basePointerAddress + offset1
        offset2 = (0xf90 * enemyNum)+0x5D0
        key2 = basePointerAddress + offset2
        if enemyNum == numToSet:
            currentHP = [process.writeBytes(key2, newHP,4)]
            print("HP value has been changed.")
        enemyNum += 1
    getEnemyCurrentHP()

def getEnemyMaxHP():
    global process
    global baseValue
    enemyNum = 20
    basePointer = baseValue + 0xD334CC
    basePointerAddress = process.read(basePointer)
    
    while enemyNum < 25:
        offset1 = (0xf90 * enemyNum)+0x594
        key1 = basePointerAddress + offset1
        offset2 = (0xf90 * enemyNum)+0x5D0
        key2 = basePointerAddress + offset2
        if enemyNum == 20:
            maxHP = [process.readBytes(key1,4)]
            currentHP = [process.readBytes(key2,4)]
        else:
            if maxHP != 0:
                maxHP.append(process.readBytes(key1,4))
                currentHP.append(process.readBytes(key2,4))
        enemyNum += 1
    print("Enemy HP max values:")
    print(maxHP)
    print("Enemy HP current values:")
    print(currentHP)
    return maxHP

def menuOpen():
    global baseValue
    
    key = baseValue + 0x00F407E4
    menuOpen = process.readBytes(key,1)
    if menuOpen == 1:
        return True
    else:
        return False

def closeMenu():
    while menuOpen():
        FFX_Xbox.menuA()

def openMenu():
    FFXC.set_value('AxisLx', 0)
    FFXC.set_value('AxisLy', 0)
    while not userControl(): #Get out of combat or whatever
        FFX_Xbox.menuB()
    while userControl() and not menuOpen():
        FFXC.set_value('BtnY',1)
        time.sleep(0.035)
        FFXC.set_value('BtnY',0)
        time.sleep(0.035)
    time.sleep(0.7)

def sGridActive():
    global baseValue
    
    key = baseValue + 0x0085B30C
    menuOpen = process.readBytes(key,1)
    print(menuOpen)
    if menuOpen == 1:
        return True
    else:
        return False

def sGridMenu():
    global baseValue
    
    key = baseValue + 0x0012AD860
    menuOpen = process.readBytes(key,1)
    return menuOpen

def sGridChar():
    global baseValue
    
    key = baseValue + 0x0012BEE2C
    character = process.readBytes(key,1)
    return character

def cursorLocation():
    global baseValue
    
    key = baseValue + 0x0021D09A4
    menu1 = process.readBytes(key,1)
    key = baseValue + 0x0021D09A6
    menu2 = process.readBytes(key,1)
    
    return [menu1,menu2]

def getMenuCursorPos():
    global baseValue

    key = baseValue + 0x01471508
    pos = process.readBytes(key, 1)

    return pos

def getCharCursorPos():
    global baseValue

    key = baseValue + 0x01441BE8
    pos = process.readBytes(key, 1)

    return pos

def getStoryProgress():
    global baseValue
    
    key = baseValue + 0x00D2D67C
    progress = process.readBytes(key,2)
    #print("Story progress: ", progress)
    return progress

def getMap():
    global baseValue
    
    key = baseValue + 0x00D2CA90
    progress = process.readBytes(key,2)
    return progress

def touchingSaveSphere():
    global baseValue
    
    key = baseValue + 0x0021D09A6
    value = process.readBytes(key,1)
    if value != 0:
        return True
    else:
        return False

def saveMenuCursor():
    global baseValue
    
    key = baseValue + 0x001467942
    value = process.readBytes(key,1)
    if value != 0:
        return True
    else:
        return False

def getYunaSlvl():
    global baseValue
    
    key = baseValue + 0x00D3212B
    sLvl = process.readBytes(key,1)
    return sLvl

def getTidusSlvl():
    global baseValue
    
    key = baseValue + 0x00D32097
    sLvl = process.readBytes(key,1)
    return sLvl

def setTidusSlvl(levels):
    global baseValue
    
    key = baseValue + 0x00D32097
    sLvl = process.writeBytes(key,levels,1)
    return sLvl

def menuControl():
    global baseValue
    
    key = baseValue + 0x0085A03C
    control = process.readBytes(key,1)
    if control == 1:
        time.sleep(0.5)
        return True
    else:
        return False

def diagSkipPossible():
    global baseValue
    
    key = baseValue + 0x0085A03C
    control = process.readBytes(key,1)
    if control == 1:
        time.sleep(0.035)
        return True
    else:
        return False

def specialTextOpen():
    global baseValue
    
    key = baseValue + 0x01466D30
    control = process.readBytes(key,1)
    if control == 1:
        time.sleep(0.035)
        return True
    else:
        key = baseValue + 0x01476988
        control = process.readBytes(key,1)
        if control == 1:
            time.sleep(0.035)
            return True
        else:
            return False

def awaitMenuControl():
    counter = 0
    while not menuControl():
        counter += 1
        if counter % 100000 == 0:
            print("Waiting for menu control. ", counter)

def clickToStoryProgress(destination):
    counter = 0
    currentState = getStoryProgress()
    print("Story goal: ", destination," | Awaiting progress state: ", currentState)
    while currentState < destination:
        if menuControl():
            FFXC.set_value('BtnB',1)
            FFXC.set_value('BtnA',1)
            time.sleep(0.035)
            FFXC.set_value('BtnB',0)
            FFXC.set_value('BtnA',0)
            time.sleep(0.035)
        if counter % 10000 == 0:
            print("Story goal: ", destination," | Awaiting progress state: ", currentState, " | counter: ", counter / 10000)
        counter += 1
        currentState = getStoryProgress()
    print("Story progress has reached destination. Value: ", destination)

def changeStory(newGameState):
    global baseValue
    
    print("Changing story flag to ", newGameState)
    key = baseValue + 0x00D2D67C
    progress = process.writeBytes(key,newGameState,2)

def itemHack(ver):
    global baseValue
    
    # I tried giving Rikku extra powerful items, but the game just wasn't having it.
    #key = baseValue + 0x00D30960 #Item in slot 3
    #progress = process.writeBytes(key,31,1)
    #key = baseValue + 0x00D30B5E #Item count in slot 3
    #progress = process.writeBytes(key,68,1)
    if ver == 1:
        #But at least these ones work.
        key = baseValue + 0x00D3095C #Change potions to Master Sphere
        progress = process.writeBytes(key,80,1)
        key = baseValue + 0x00D30B5C #Might as well have a lot of those.
        progress = process.writeBytes(key,90,1)
    elif ver == 2:
        key = baseValue + 0x00D3095C #Purifying Salts (no encounters)
        progress = process.writeBytes(key,63,1)
        key = baseValue + 0x00D30B5C
        progress = process.writeBytes(key,99,1)
        key = baseValue + 0x00D3095E #Chocobo Feathers
        progress = process.writeBytes(key,55,1)
        key = baseValue + 0x00D30B5D
        progress = process.writeBytes(key,99,1)
        key = baseValue + 0x00D30960 #Return Spheres for First Strike
        progress = process.writeBytes(key,96,1)
        key = baseValue + 0x00D30B5E
        progress = process.writeBytes(key,99,1)
        key = baseValue + 0x00D30962 #Lightning Gems
        progress = process.writeBytes(key,31,1)
        key = baseValue + 0x00D30B5F
        progress = process.writeBytes(key,99,1)
        key = baseValue + 0x00D30964 #Dark Matter
        progress = process.writeBytes(key,53,1)
        key = baseValue + 0x00D30B60
        progress = process.writeBytes(key,99,1)
        key = baseValue + 0x00D30966 #Wings
        progress = process.writeBytes(key,108,1)
        key = baseValue + 0x00D30B61
        progress = process.writeBytes(key,99,1)
        key = baseValue + 0x00D30968 #P.down
        progress = process.writeBytes(key,6,1)
        key = baseValue + 0x00D30B62
        progress = process.writeBytes(key,99,1)
        key = baseValue + 0x00D3240D #Rikku charge value
        progress = process.writeBytes(key,100,1)
    
def changeGold(value):
    global baseValue
    key = baseValue + 0x00D307D8
    progress = process.writeBytes(key,9999999,4)

def blitzOwnScore():
    global baseValue
    
    key = baseValue + 0x0151728C
    score = process.readBytes(key, 1)
    return score

def blitzOppScore():
    global baseValue
    
    key = baseValue + 0x0151644C
    score = process.readBytes(key, 1)
    return score

def blitzClockMenu():
    global baseValue
    
    key = baseValue + 0x014765FA
    status = process.readBytes(key, 1)
    return status

def blitzMenuNum():
    global baseValue
    #20 = Movement menu (auto, type A, or type B)
    #29 = Formation menu
    #38 = Breakthrough
    #24 = Pass To menu (other variations are set to 24)
    #Unsure about other variations, would take more testing.
    
    key = baseValue + 0x0146770A
    status = process.readBytes(key, 1)
    if status == 17 or status == 27:
        status = 24
    return status

def blitzTargetPlayer():
    global baseValue
    
    key = baseValue + 0x00D3761C
    player = process.readBytes(key, 1)
    print("Target Player number: ", player)
    print("12 = Opposing team")
    print("18 = non-controlled ball (shot or pass)")
    return player

def blitzCoords():
    global baseValue
    
    key = baseValue + 0x00D37698
    xVal = process.readBytes(key, 1)
    xVal = xVal * -1
    key = baseValue + 0x00D37690
    yVal = process.readBytes(key, 1)
    return [xVal,yVal]

def blitzGameActive():
    if getMap() == 62:
        return True
    else:
        return False

def blitzBallControl():
    try:
        if blitzClockMenu() == 24:
            if blitzCurrPlayer() >= 2 and blitzCurrPlayer <= 6:
                return True
            else:
                return False
        else:
            return False
    except:
        return False

def blitzClock():
    global baseValue
    
    key = baseValue + 0x012C64B14
    clock = process.readBytes(key, 1)
    return clock

def blitzballPatriotsStyle():
    global baseValue
    
    key = baseValue + 0x00D2E0CE
    progress = process.writeBytes(key,50,1)
    key = baseValue + 0x00D2E131
    progress = process.writeBytes(key,50,1)

def desertFormat(rikkuCharge):
    order = getOrderSix()
    if order == [0,3,2,4,6,5]:
        print("Formation is fine, moving on.")
    elif rikkuCharge == False:
        fullPartyFormat('desert1')
    else:
        fullPartyFormat('desert2')

def partySize():
    return len(getBattleFormation())

def activepartySize():
    return len(getActiveBattleFormation())

def fullPartyFormat_New(frontLine, menusize):
    partyMembers = 7
    frontLine = frontLine.lower()
    if frontLine == 'kimahri':
        order = getOrderSeven()
        orderFinal = [0, 3, 2, 6, 4, 5, 1]
    if frontLine == 'rikku':
        order = getOrderSeven()
        orderFinal = [0, 6, 2, 3, 4, 5, 1]
    if frontLine == 'yuna':
        order = getOrderSeven()
        orderFinal = [0, 1, 2, 6, 4, 5, 3]
    if frontLine == 'gauntlet':
        order = getOrderSeven()
        orderFinal = [0, 1, 3, 2, 4, 5, 6]
    if frontLine == 'postbunyip':
        order = getOrderSeven()
        orderFinal = [0, 4, 2, 6, 1, 3, 5]
    if frontLine == 'mwoodsneedcharge':
        order = getOrderSeven()
        orderFinal = [0, 6, 2, 4, 1, 3, 5]
    if frontLine == 'mwoodsgotcharge':
        order = getOrderSeven()
        orderFinal = [0, 4, 2, 6, 1, 3, 5]
    if frontLine == 'mwoodsdone':
        order = getOrderSeven()
        orderFinal = [0, 3, 2, 4, 1, 6, 5]
    if frontLine == 'macalaniaescape':
        order = getOrderSeven()
        orderFinal = [0, 1, 6, 2, 4, 3, 5]
    if frontLine == 'desert1':
        partyMembers = 6
        order = getOrderSix()
        orderFinal = [0, 6, 2, 3, 4, 5]
    if frontLine == 'desert2':
        partyMembers = 6
        order = getOrderSix()
        orderFinal = [0, 3, 2, 6, 4, 5]
    if frontLine == 'guards':
        partyMembers = 6
        order = getOrderSix()
        orderFinal = [0, 2, 3, 6, 4, 5]
    if frontLine == 'evrae':
        partyMembers = 6
        order = getOrderSix()
        orderFinal = [0, 6, 3, 2, 4, 5]
    if frontLine == 'spheri':
        order = getOrderSeven()
        orderFinal = [0, 3, 1, 4, 2, 6, 5]
    if frontLine == 'crawler':
        order = getOrderSeven()
        orderFinal = [0, 3, 5, 4, 2, 6, 1]
    if frontLine == 'besaid1':
        order = getOrderSix()  # Should work the same way
        orderFinal = [0, 1, 5, 3, 5]
    if frontLine == 'djose':
        partyMembers = 6
        order = getOrderSix()
        orderFinal = [0,4,2,6,3,5]
    if frontLine == 'kilika':
        order = getOrderSix()  # Should work the same way
        orderFinal = [0, 1, 4, 3, 5]
        partyMembers = 5
    if order == orderFinal:
        print("Good to go, no action taken.")
    else:
        print("Converting from formation:")
        print(order)
        print("Into formation:")
        print(orderFinal)
        while not menuOpen():
            openMenu()

        currentmenuposition = getMenuCursorPos()

        targetmenuposition = 7
        menudistance = abs(targetmenuposition - currentmenuposition)

        if menudistance < (menusize / 2 - 1):
            for i in range(menudistance):
                if targetmenuposition > currentmenuposition:
                    FFX_Xbox.menuDown()
                else:
                    FFX_Xbox.menuUp()
        else:
            for i in range(menusize - menudistance):
                if targetmenuposition > currentmenuposition:
                    FFX_Xbox.menuUp()
                else:
                    FFX_Xbox.menuDown()

        FFX_Xbox.menuB()

        if order[0] != orderFinal[0]:
            print("Looking for ", nameFromNumber(orderFinal[0]))
            if order[1] == orderFinal[0]:
                print("Tidus in Second slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[1] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif order[2] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0]), " in Third slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                order[2] = order[0]
                order[0] = orderFinal[0]
                FFX_Xbox.menuUp()
            elif order[3] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0]), " in Fourth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[3] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
            elif order[4] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0]), " in Fifth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                order[4] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
            elif partyMembers > 5 and order[5] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0]), " in Sixth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                order[5] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
            elif partyMembers == 7 and order[6] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0]), " in seventh slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                order[6] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
        else:
            print(nameFromNumber(order[0]), " seems fine.")
            FFX_Xbox.menuDown()
        if order[1] != orderFinal[1]:
            print("Looking for ", nameFromNumber(orderFinal[1]))
            if order[2] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1]), " in Third slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[2] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif order[3] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1]), " in Fourth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[3] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
            elif order[4] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1]), " in Fifth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[4] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
            elif partyMembers > 5 and order[5] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1]), " in Sixth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[5] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
            elif partyMembers == 7 and order[6] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1]), " in Seventh slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[6] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
        else:
            print(nameFromNumber(order[1]), " seems fine.")
            FFX_Xbox.menuDown()
        if order[2] != orderFinal[2]:
            print("Looking for ", nameFromNumber(orderFinal[2]))
            if order[3] == orderFinal[2]:
                print(nameFromNumber(orderFinal[2]), " in fourth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[3] = order[2]
                order[2] = orderFinal[2]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif order[4] == orderFinal[2]:
                print(nameFromNumber(orderFinal[2]), " in fifth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[4] = order[2]
                order[2] = orderFinal[2]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
            elif partyMembers > 5 and order[5] == orderFinal[2]:
                print(nameFromNumber(orderFinal[2]), " in sixth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[5] = order[2]
                order[2] = orderFinal[2]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
            elif partyMembers == 7 and order[6] == orderFinal[2]:
                print(nameFromNumber(orderFinal[2]), " in seventh slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[6] = order[2]
                order[2] = orderFinal[2]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
        else:
            print(nameFromNumber(order[2]), " seems fine.")
            FFX_Xbox.menuDown()
        if order[3] != orderFinal[3]:
            print("Looking for ", nameFromNumber(orderFinal[3]))
            if order[4] == orderFinal[3]:
                print(nameFromNumber(orderFinal[3]), " in fifth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[4] = order[3]
                order[3] = orderFinal[3]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif partyMembers > 5 and order[5] == orderFinal[3]:
                print(nameFromNumber(orderFinal[3]), " in sixth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[5] = order[3]
                order[3] = orderFinal[3]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
            elif partyMembers == 7 and order[6] == orderFinal[3]:
                print(nameFromNumber(orderFinal[3]), " in seventh slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[6] = order[3]
                order[3] = orderFinal[3]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
        else:
            print(nameFromNumber(order[3]), " seems fine.")
            FFX_Xbox.menuDown()
        if partyMembers > 5 and order[4] != orderFinal[4]:
            print("Looking for ", nameFromNumber(orderFinal[4]))
            if order[5] == orderFinal[4]:
                print(nameFromNumber(orderFinal[4]), " in Sixth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[5] = order[4]
                order[4] = orderFinal[4]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif partyMembers == 7 and order[6] == orderFinal[4]:
                print(nameFromNumber(orderFinal[4]), " in Seventh slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[6] = order[4]
                order[4] = orderFinal[4]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
        else:
            print(nameFromNumber(order[4]), " seems fine.")
            FFX_Xbox.menuDown()
        if partyMembers == 7 and order[5] != orderFinal[5]:
            print(nameFromNumber(order[5]), " and ", nameFromNumber(order[6]),
                  "are swapped. Flipping them back.")
            print("Expected order: ", orderFinal[5], " | ", orderFinal[6])
            FFX_Xbox.menuB()
            FFX_Xbox.menuDown()
            FFX_Xbox.menuB()
        elif partyMembers == 7:
            print(nameFromNumber(orderFinal[5]), " and ", nameFromNumber(orderFinal[6]), " seem fine.")

        # time.sleep(120) #For testing only. Allows us to see what's going on.
        FFX_Xbox.menuA()
        #closeMenu()

def fullPartyFormat(frontLine):
    partyMembers = 7
    frontLine = frontLine.lower()
    if frontLine == 'kimahri':
        order = getOrderSeven()
        orderFinal = [0,3,2,6,4,5,1]
    elif frontLine == 'rikku':
        order = getOrderSeven()
        orderFinal = [0,6,2,3,4,5,1]
    elif frontLine == 'yuna':
        order = getOrderSeven()
        orderFinal = [0,1,2,6,4,5,3]
    elif frontLine == 'gauntlet':
        order = getOrderSeven()
        orderFinal = [0,1,3,2,4,5,6]
    elif frontLine == 'macalaniaescape':
        order = getOrderSeven()
        orderFinal = [0,1,6,2,4,3,5]
    elif frontLine == 'desert1':
        partyMembers = 6
        order = getOrderSix()
        orderFinal = [0,6,2,3,4,5]
    elif frontLine == 'desert2':
        partyMembers = 6
        order = getOrderSix()
        orderFinal = [0,3,2,6,4,5]
    elif frontLine == 'guards':
        partyMembers = 6
        order = getOrderSix()
        orderFinal = [0,2,3,6,4,5]
    elif frontLine == 'evrae':
        partyMembers = 6
        order = getOrderSix()
        orderFinal = [0,6,3,2,4,5]
    elif frontLine == 'djose':
        partyMembers = 6
        order = getOrderSix()
        orderFinal = [0,4,2,6,3,5]
    elif frontLine == 'spheri':
        order = getOrderSeven()
        orderFinal = [0,3,1,4,2,6,5]
    elif frontLine == 'crawler':
        order = getOrderSeven()
        orderFinal = [0,3,5,4,2,6,1]
    elif frontLine == 'besaid1':
        order = getOrderSix() #Should work the same way
        partyMembers = 5
        orderFinal = [0,1,5,3,4]
    elif frontLine == 'kilika':
        order = getOrderSix() #Should work the same way
        orderFinal = [0,1,4,3,5]
        partyMembers = 5
    if order == orderFinal:
        print("Good to go, no action taken.")
    else:
        print("Converting from formation:")
        print(order)
        print("Into formation:")
        print(orderFinal)
        while not menuOpen():
            openMenu()
        
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuUp()
        FFX_Xbox.menuB()
        
        if order[0] != orderFinal[0]:
            print("Looking for ",nameFromNumber(orderFinal[0]))
            if order[1] == orderFinal[0]:
                print("Tidus in Second slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[1] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif order[2] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0])," in Third slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                order[2] = order[0]
                order[0] = orderFinal[0]
                FFX_Xbox.menuUp()
            elif order[3] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0])," in Fourth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[3] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
            elif order[4] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0])," in Fifth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                order[4] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
            elif partyMembers > 5 and order[5] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0])," in Sixth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                order[5] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
            elif partyMembers == 7 and order[6] == orderFinal[0]:
                print(nameFromNumber(orderFinal[0])," in seventh slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuB()
                order[6] = order[0]
                order[0] = orderFinal[0]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
        else:
            print(nameFromNumber(order[0])," seems fine.")
            FFX_Xbox.menuDown()
        if order[1] != orderFinal[1]:
            print("Looking for ",nameFromNumber(orderFinal[1]))
            if order[2] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1])," in Third slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[2] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif order[3] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1])," in Fourth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[3] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
            elif order[4] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1])," in Fifth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[4] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
            elif partyMembers > 5 and order[5] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1])," in Sixth slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[5] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
            elif partyMembers == 7 and order[6] == orderFinal[1]:
                print(nameFromNumber(orderFinal[1])," in Seventh slot. Swapping")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[6] = order[1]
                order[1] = orderFinal[1]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
        else:
            print(nameFromNumber(order[1])," seems fine.")
            FFX_Xbox.menuDown()
        if order[2] != orderFinal[2]:
            print("Looking for ",nameFromNumber(orderFinal[2]))
            if order[3] == orderFinal[2]:
                print(nameFromNumber(orderFinal[2])," in fourth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[3] = order[2]
                order[2] = orderFinal[2]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif order[4] == orderFinal[2]:
                print(nameFromNumber(orderFinal[2])," in fifth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[4] = order[2]
                order[2] = orderFinal[2]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
            elif partyMembers > 5 and order[5] == orderFinal[2]:
                print(nameFromNumber(orderFinal[2])," in sixth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[5] = order[2]
                order[2] = orderFinal[2]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
            elif partyMembers == 7 and order[6] == orderFinal[2]:
                print(nameFromNumber(orderFinal[2])," in seventh slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[6] = order[2]
                order[2] = orderFinal[2]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
        else:
            print(nameFromNumber(order[2])," seems fine.")
            FFX_Xbox.menuDown()
        if order[3] != orderFinal[3]:
            print("Looking for ",nameFromNumber(orderFinal[3]))
            if order[4] == orderFinal[3]:
                print(nameFromNumber(orderFinal[3])," in fifth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[4] = order[3]
                order[3] = orderFinal[3]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif partyMembers > 5 and order[5] == orderFinal[3]:
                print(nameFromNumber(orderFinal[3])," in sixth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[5] = order[3]
                order[3] = orderFinal[3]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
            elif partyMembers == 7 and order[6] == orderFinal[3]:
                print(nameFromNumber(orderFinal[3])," in seventh slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[6] = order[3]
                order[3] = orderFinal[3]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
                FFX_Xbox.menuUp()
        else:
            print(nameFromNumber(order[3])," seems fine.")
            FFX_Xbox.menuDown()
        if partyMembers > 5 and order[4] != orderFinal[4]:
            print("Looking for ",nameFromNumber(orderFinal[4]))
            if order[5] == orderFinal[4]:
                print(nameFromNumber(orderFinal[4])," in Sixth slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[5] = order[4]
                order[4] = orderFinal[4]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
            elif partyMembers == 7 and order[6] == orderFinal[4]:
                print(nameFromNumber(orderFinal[4])," in Seventh slot. Swapping.")
                FFX_Xbox.menuB()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuDown()
                FFX_Xbox.menuB()
                order[6] = order[4]
                order[4] = orderFinal[4]
                print(order)
                if order == orderFinal:
                    print("Order is good (early). Return.")
                    closeMenu()
                    return
                FFX_Xbox.menuUp()
        else:
            print(nameFromNumber(order[4])," seems fine.")
            FFX_Xbox.menuDown()
        if partyMembers == 7 and order[5] != orderFinal[5]:
            print(nameFromNumber(order[5])," and ",nameFromNumber(order[6]), \
            "are swapped. Flipping them back.")
            print("Expected order: ", orderFinal[5], " | ", orderFinal[6])
            FFX_Xbox.menuB()
            FFX_Xbox.menuDown()
            FFX_Xbox.menuB()
        elif partyMembers == 7:
            print(nameFromNumber(orderFinal[5])," and ",nameFromNumber(orderFinal[6])," seem fine.")
        
        #time.sleep(120) #For testing only. Allows us to see what's going on.
        closeMenu()

def nameFromNumber(charNum):
    if charNum == 0:
        return "Tidus"
    if charNum == 1:
        return "Yuna"
    if charNum == 2:
        return "Auron"
    if charNum == 3:
        return "Kimahri"
    if charNum == 4:
        return "Wakka"
    if charNum == 5:
        return "Lulu"
    if charNum == 6:
        return "Rikku"

def end():
    global process
    process.close()
    print("Memory reading process is now closed.")

#-------------------------------------------------------
#Egg hunt section


def eggX(eggNum):
    global process
    global baseValue
    eggNum += 23
    basePointer = baseValue + 0x1FC44E4    # equivalent to the pointer FFX.exe+EA22A0
    basePointerAddress = process.read(basePointer)    # pseudocode function to get the hex value from basePointer to figure out the address of the start of the actor array
    key = basePointerAddress + (0x880 * eggNum) + 0x0C
    retVal = float_from_integer(process.read(key))
    #print("Egg ", eggNum," X value: ", retVal)
    return retVal

def eggY(eggNum):
    global process
    global baseValue
    eggNum += 23
    basePointer = baseValue + 0x1FC44E4    # equivalent to the pointer FFX.exe+EA22A0
    basePointerAddress = process.read(basePointer)    # pseudocode function to get the hex value from basePointer to figure out the address of the start of the actor array
    key = basePointerAddress + (0x880 * eggNum) + 0x14
    retVal = float_from_integer(process.read(key))
    #print("Egg ", eggNum," Y value: ", retVal)
    return retVal

def getEggDistance(eggNum):
    global process
    global baseValue
    basePointer = baseValue + 0xF270B8
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x1C4CC + (0x40 * eggNum)
    retVal = float_from_integer(process.read(key))
    return retVal

def getEggLife(eggNum):
    global process
    global baseValue
    basePointer = baseValue + 0xF270B8
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x1C4CC + (0x40 * eggNum) + 4
    retVal = process.readBytes(key,1)
    return retVal

def getEggPicked(eggNum):
    global process
    global baseValue
    basePointer = baseValue + 0xF270B8
    basePointerAddress = process.read(basePointer)
    key = basePointerAddress + 0x1C4CC + (0x40 * eggNum) + 5
    retVal = process.readBytes(key,1)
    return retVal

class egg:
    def __init__(self, eggnum):
        self.num = eggnum
        self.x = eggX(self.num)
        self.y = eggY(self.num)
        self.distance = getEggDistance(self.num)
        self.eggLife = getEggLife(eggnum)
        self.eggPicked = getEggPicked(eggnum)
        
        if self.distance != 0 and self.eggPicked == 0:
            self.isActive = True
        else:
            self.isActive = False
        
        if self.eggPicked == 1:
            self.goForEgg = False
        elif self.eggLife > 100 and self.distance > 100:
            self.goForEgg = False
        elif self.distance > 250:
            self.goForEgg = False
        elif self.distance == 0:
            self.goForEgg = False
        else:
            self.goForEgg = True
    
    def reportVars(self):
        varArray = [self.num, self.isActive, self.x, self.y, 150 - self.eggLife, self.eggPicked, self.distance]
        print("Egg_num, Is_Active, X, Y, Egg Life, Picked up, distance")
        print(varArray)

def buildEggs():
    retArray = [0,0,0,0,0,0,0,0,0,0]
    for x in range(10):
        retArray[x] = egg(x)
    return retArray