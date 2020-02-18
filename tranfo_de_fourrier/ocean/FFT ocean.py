import numpy as np
from numpy.random import *
import matplotlib.pyplot as plt
from numpy.fft import *


def readVectorsFromFile(filename):
    y = np.loadtxt(filename, usecols=(0))
    # print(type(x))
    # x = 2 * x *1.1
    x= np.loadtxt("longeur_d'onde")
    return (x, y)
def graph(x,y,titre):
    plt.plot(x, y)
    plt.title(titre)
    plt.ylabel("Intensite lumineuse [W]")
    plt.xlabel("Longueur d'onde [nm]")
    plt.show()

if __name__ == '__main__':
    path = r'D:\Desktop\Université Raph\Hiver 2020\Optique expérimentale\Michelson'


    (x, y) = readVectorsFromFile("Hg_ocean")
    graph(x,y,"Graphique de l'intensité selon la longeur d'onde de la lampe au mercure par l'interféromètre Ocean Optics")
    print(x[y.argmax()])

    (x, y) = readVectorsFromFile("Na_ocean")
    graph(x,y,"Graphique de l'intensité selon la longeur d'onde de la lampe au sodium par l'interféromètre  Ocean Optics")
    print(x[y.argmax()])

    (x, y) = readVectorsFromFile("Blanc_ocean")
    graph(x,y,"Graphique de l'intensité selon la longeur d'onde de la lumière blanche par l'interféromètre Ocean Optics")
    print(x[y.argmax()])