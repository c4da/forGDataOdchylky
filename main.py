


import numpy as np
import plotCheck

COL_NAMES = []
SENSORS_LABELS = []


def getSensorsLabels():
    global SENSORS_LABELS
    return SENSORS_LABELS

def setXlsxFileColNames(colNames):
    global COL_NAMES
    COL_NAMES = colNames

def getXlsxFileColNames():
    global COL_NAMES
    return COL_NAMES

def setSensorsLabels(data):
    global SENSORS_LABELS
    SENSORS_LABELS = list(data.keys())[2:]

def addToSensorsLabels(col):
    global SENSORS_LABELS
    SENSORS_LABELS.append(col)
    SENSORS_LABELS.sort()

def getEvalInterval():
    x_eval = np.arange(0.0, 1500.0, 0.1)
    return x_eval

def getLinInterp(x_eval, x, y):
    yinterp = np.interp(x_eval, x, y, left=None, right=None, period=None)
    return yinterp

def readData(filename:str) -> dict:
    data = {}
    with open(filename) as f:
        lines = f.readlines()
        for j, line in enumerate(lines):
            splitted = line.split(";")
            for i, e in enumerate(splitted):
                if j == 0:
                    data[i] = []
                if i == len(splitted):
                    e.replace("\n", "")
                if i == 0:
                    data[i].append(e)
                else:
                    data[i].append(float(e.replace(",",".")))
    return data

def getColumnsNamesList(data):
    return data.keys()

def checkDirection(data):
    if data[1][0] < data[1][1]:
        return data
    for key in list(data.keys()):
        data[key].reverse()
    return data

def interpolate_data(dataDict: dict, savePath: str) -> dict:
    levels = getSensorsLabels()
    x_eval = getEvalInterval()

    for level in levels:
        x = np.array(dataDict[1])
        y = np.array(dataDict[level])
        y_interp = getLinInterp(x_eval, x, y)
        dataDict[level] = y_interp

        f = open(savePath + 'saved_data_format_interp_' + str(level) + '.txt', 'w')

        for i in range(len(getEvalInterval())):
            line = str(round(getEvalInterval()[i], 1)) + '; ' + str(round(y_interp[i], 4)) + '\n'
            f.write(line)

        f.close()
    dataDict[1] = x_eval
    return dataDict

def setZeroes(xMeasured:list, dataInterp:dict) -> dict:
    zeroStart = 0
    zeroEnd = 0
    for i, x in enumerate(dataInterp[1]):
        if x < xMeasured[0]:
            zeroStart = i
        if x > xMeasured[-1]:
            zeroEnd = i
            break
    for key in getSensorsLabels():
        z1 = [0]*zeroStart
        z2 = [0]*(len(dataInterp[key]) - zeroEnd)
        # dataInterp[key] = z1+dataInterp[key][zeroStart:]
        dataInterp[key] = np.insert(dataInterp[key][zeroStart:], 0, np.array(z1))
        # dataInterp[key] = dataInterp[key][:zeroEnd]+z2
        dataInterp[key] = np.insert(dataInterp[key][:zeroEnd],zeroEnd, np.array(z2))

def saveAll(data, savePath):
    """
    x = dataIn[key][-2]
    y = dataIn[key][-1]
    """
    levels = getSensorsLabels()
    x_eval = getEvalInterval()
    f = open(savePath + 'saved_all_data_format_interp.txt', 'w')
    i = 0
    for x in x_eval:
        line = "123; " + str(round(x, 1)) + '; '
        f.write(line)
        dataLine = ""
        for level in levels:
            dataLine += str(round(data[level][i], 4)).replace(".",",")
            if (level != levels[-1]):
                dataLine += "; "
        dataLine += '\n'
        f.write(dataLine)
        i += 1
    f.close()

def addition(src:dict, dst:dict)->dict:
    for key in list(src.keys()):
        if key == 0 or key == 1:
            continue
        dst[key] = np.array(dst[key]) + np.array(src[key])
    return dst

if __name__ == "__main__":
    fileName = "odchylky-do-P2.txt"
    path = ""
    data = readData(path + fileName)
    vzor = readData(path + "vzorUPR.txt")
    setSensorsLabels(data)
    checkDirection(data)
    dataInterp = data.copy()
    dataInterp = interpolate_data(dataInterp, "")
    setZeroes(data[1], dataInterp)
    # saveAll(dataInterp, "")
    # plotCheck.makePlots(dataInterp, getSensorsLabels(), "", "_final")
    dataAdded = addition(vzor, dataInterp)
    saveAll(dataInterp, "addition_vzorUPR_")
    plotCheck.makePlots(dataAdded, getSensorsLabels(), "", "_addition")
    print("done")