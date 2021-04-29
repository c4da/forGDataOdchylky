import numpy as np
import matplotlib.pyplot as plt


def plotGraph(x, y, xname, yname, title, PATH):
    """
    function plots and saves a graph
    :param x:
    :param y:
    :param xname:
    :param yname:
    :param title:
    :return:
    """
    fig = plt.figure()
    plt.title(title)
    plt.xlabel(xname)
    plt.ylabel(yname)

    x = [float(x_) for x_ in x]
    y = [float(y_) for y_ in y]
    x = [0 if np.isnan(x_) else x_ for x_ in x]
    y = [0 if np.isnan(y_) else y_ for y_ in y]

    plt.xticks(np.linspace(min(x), max(x), 10))
    plt.yticks(np.linspace(min(y), max(y), 10))

    plt.plot(x, y)
    plt.grid(True)
    plt.ioff()
    fig.savefig(PATH + title + '_graph.png')
    plt.close(fig)
    return 0


def processData(data):
    return np.array(data)


def makePlots(dataIn: dict, keys: list, path: str, name=''):
    x = dataIn[1]
    for key in keys:
        y = dataIn[key]
        title = 'graph_' + str(key) + "_"+name
        plotGraph(x, y, 'model - long. coord', 'model - height', title, path)
    return 0