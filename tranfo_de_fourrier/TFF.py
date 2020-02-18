import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import *

""" Ce script genere des interferogrammes tels qu'obtenus avec un interferometre
de Michelson dans le but d'etudier la transformée de Fourier et de comprendre 
comment la resolution spectrale est déterminée.
"""


def read_from_file(filename):
	file = np.genfromtxt(filename, skip_header=18, skip_footer=1)
	x = file[:, 1]
	y = file[:, 2]
	return (x, y)  # J: J'ai chamgé la fonction np.loadtxt par la fonction np.genfromtxt (plus efficace)

def readVectorsFromFile(filename):
    y = np.loadtxt(filename, usecols=(0))
    # print(type(x))
    # x = 2 * x *1.1
    x= np.loadtxt("longeur_d'onde")
    return (x, y)

# def generateHeNeInterferogram(xMin, xMax, N):
# 	""" Genere un tableau de N valeurs equidistantes enntre xMin et xMax.
# 	Ensuite, genere un tableau de N valeurs qui representent un interferogramme
# 	d'un laser He-Ne a 0.6328 microns. On ajoute du bruit pour rendre le tout
# 	plus realiste.
# 	"""
# 	dx = (xMax - xMin)/N
# 	x = np.linspace(xMin, xMax, N)
# 	noise = random(len(x))*0.05
# 	y = 1+np.cos(2 * np.pi / 0.6328 * x)+noise
# 	return (x,y)
#
# def generateWhiteLightInterferogram(xMin, xMax, N):
# 	""" Genere un tableau de N valeurs equidistantes enntre xMin et xMax.
# 	Ensuite, genere un tableau de N valeurs qui representent un interferogramme
# 	d'une source blanche visible. On ajoute du bruit pour rendre le tout
# 	plus realiste.
# 	"""
# 	dx = (xMax - xMin)/N
# 	x = np.linspace(xMin, xMax, N)
# 	noise = random(len(x))*0.05
# 	k1 = 1/0.4
# 	k2 = 1/0.8
# 	y = 1+np.exp(-x*x/4)*(np.sin(2 * np.pi * (k1+k2)*x/2)/x * np.sin(2 * np.pi * (k1-k2)*x/2)+ noise)
# 	return (x,y)

def fourierTransformInterferogram(x, y):
    """ A partir du tableau de valeurs Y correspondant a l'abscisse X,
    la transformée de Fourier est calculée et l'axes des fréquences (f en
    µm^-1) et des wavelengths (1/f en microns) est retournée.
    Le spectre est un ensemble de valeurs complexes pour lesquelles l'amplitude
    et la phase sont pertinentes: l'ordre des valeurs commence par la valeur DC (0)
    et monte jusqu'a f_max=1/2/∆x par resolution de ∆f = 1/N/∆x. A partir de la
    (N/2) ieme valeur, la frequence est negative jusqu'a -∆f dans la N-1 case.
    Voir
    https://github.com/dccote/Enseignement/blob/master/HOWTO/HOWTO-Transformes%20de%20Fourier%20discretes.pdf
    """
    spectrum = fft(y)
    dx = x[1] - x[0]  # on obtient dx, on suppose equidistant
    N = len(x)  # on obtient N directement des données
    frequencies = fftfreq(N, dx)  # Cette fonction est fournie par numpy
    wavelengths = 1 / frequencies  # Les fréquences en µm^-1 sont moins utiles que lambda en µm
    return (wavelengths, frequencies, spectrum)


def plotCombinedFigures(x, y, w, s, title="", left=400, right=800):
    """"
    On met l'interferogramme et le spectre sur la meme page.
    """
    fig, (axes, axesFFT) = plt.subplots(2, 1, figsize=(10, 7))
    plt.subplots_adjust(hspace=0.60)
    axes.plot(x, y, '-', color='gold')
    axes.set_title("Interferogramme")
    axes.set_xlabel('Distance en micron')
    axes.set_ylabel('Tension [mV]')
    axesFFT.plot(w * 1000, abs(s),color='r')
    axesFFT.set_xlim(left=left, right=right)
    axesFFT.set_xlabel("Longueur d'onde [nm]")
    axesFFT.set_ylabel('Tension [mV]')
    axesFFT.set_title(title)
    plt.show()
def plotCombinedFigures_2(x, y, w, s,u,v, title="", left=400, right=800):
    """"
    On met l'interferogramme et le spectre sur la meme page.
    """
    fig, (axes, axesFFT) = plt.subplots(2, 1, figsize=(10, 7))
    plt.subplots_adjust(hspace=0.60)
    axes.plot(x, y, '-',color='gold')
    axes.set_title("Interferogramme")
    axes.set_xlabel('Distance en micron')
    axes.set_ylabel('Tension [mV]')
    axesFFT.plot(w * 1000, abs(s),label="spectre de l'interféromètre", color='c')
    axesFFT.plot(u,v, label="spectre de l'interféromètre Ocean Optics",color='m')
    axesFFT.set_xlim(left=left, right=right)
    axesFFT.set_xlabel("Longueur d'onde [nm]")
    axesFFT.set_ylabel('Tension [mV]')
    axesFFT.set_title(title)
    axesFFT.legend()
    plt.show()

if __name__=='__main__':

    (a, b) = read_from_file("laser_hene_long.txt")
    ( x , y) = (a/10 , b)
    (w, f, s) = fourierTransformInterferogram(x, y)
    df = f[1] - f[0]
    dl = 0.500 * 0.500 * df * 1000
    plotCombinedFigures(10*x, y, 2*w, s, left=300, right=800, title="Laser He-Ne, resolution {0:0.2f} nm".format(dl))
    print(-w[s.argmin(axis=0)] * 1000 * 2)

    (u, v) = readVectorsFromFile("ocean/Blanc_ocean")
    (x, y) = read_from_file("lumiere_blanche_6.txt")
    (w, f, s) = fourierTransformInterferogram(x, y)
    df = f[1] - f[0]
    dl = 0.500 * 0.500 * df * 1000
    plotCombinedFigures_2(10*x, y, 2*w, s,u,v, left=0, right=1300, title="Lumière blanche, resolution {0:0.2f} nm".format(dl))
    print(-w[s.argmin(axis=0)] * 1000 * 2)

    (u, v) = readVectorsFromFile("ocean/Na_ocean")
    (x, y) = read_from_file("Na_moy20_long.txt")
    (w, f, s) = fourierTransformInterferogram(x, y)
    df = f[1] - f[0]
    dl = 0.500 * 0.500 * df * 1000
    plotCombinedFigures_2(10*x, y, 2*w, s,u,v, left=300, right=1000, title="Lumière sodium 1, resolution {0:0.2f} nm".format(dl))
    print(-w[s.argmin(axis=0)] * 1000 * 2)

    (x, y) = read_from_file("Na_vrai_batte_moy20.txt")
    (w, f, s) = fourierTransformInterferogram(x, y)
    df = f[1] - f[0]
    dl = 0.500 * 0.500 * df * 1000
    plotCombinedFigures(10*x, y, w, s, left=400, right=900, title="Lumière sodium, resolution {0:0.2f} nm".format(dl))
    print(w[s.argmin(axis=0)] * 1000)

    (c, d) = readVectorsFromFile("ocean/Hg_ocean")
    (u,v)=(c,d/50)
    # print(x[y.argmax()])
    (x, y) = read_from_file("Hg_moyen_20_bat.txt")
    (w, f, s) = fourierTransformInterferogram(x, y)
    df = f[1] - f[0]
    dl = 0.500 * 0.500 * df * 1000
    plotCombinedFigures_2(10*x, y, 2*w, s,u,v, left=100, right=1000, title="Lumière au mercure, resolution {0:0.2f} nm".format(dl))
    print(-w[s.argmin(axis=0)] * 1000 * 2)

    # (a, b) = readVectorsFromFile( 'laser_hene_long.txt')  # en microns
    # ( x , y) = (a/10 , b)
    # (w, f, s) = fourierTransformInterferogram(x, y)
    # df = f[1] - f[0]
    # dl = 0.6328 * 0.6328 * df * 1000  # x 1000 pour nm
    # plotCombinedFigures(x, y, 2*w, s, left=500 - 5 * dl, right=1000 - 5 * dl,
    # title="Spectre He-Ne, resolution resolution {0:0.2f} nm".format(dl))
    # print(-w[s.argmin(axis=0)] * 1000 *np.sqrt(2)) # affiche le max de longueur d'onde
    #
    # (x, y) = readVectorsFromFile('lumiere_blanche_6.txt')  # en microns
    # (w, f, s) = fourierTransformInterferogram(x, y)
    # df = f[1] - f[0]
    # dl = 0.6328 * 0.6328 * df * 1000  # x 1000 pour nm
    # plotCombinedFigures(x, y, np.sqrt(2)*w, s, left=500 - 5 * dl, right=1000 - 5 * dl,
    #                     title="Spectre lumière blanche, resolution resolution {0:0.2f} nm".format(dl))
    # print(-w[s.argmin()]*1000*np.sqrt(2))  # affiche le max de longueur d'onde
    #
    # (a, b) = readVectorsFromFile('Na_moy20_long.txt')  # en microns
    # (x, y) = (a , b)
    # (w, f, s) = fourierTransformInterferogram(x, y)
    # # df = f[1] - f[0]
    # # dl = 0.6328 * 0.6328 * df * 1000  # x 1000 pour nm
    # # plotCombinedFigures(x, y, 2 * w, s, left=500 - 5 * dl, right=1000 - 5 * dl,
    # # title="Spectre lampe au sodium, sans battement , resolution resolution {0:0.2f} nm".format(dl))
    # print(-w[s.argmin(axis=0)] * 1000 *2  ) # affiche le max de longueur d'onde
    #
    # (x, y) = readVectorsFromFile('Na_vrai_batte_moy20.txt')  # en microns
    # (w, f, s) = fourierTransformInterferogram(x, y)
    # # df = f[1] - f[0]
    # # dl = 0.6328 * 0.6328 * df * 1000  # x 1000 pour nm
    # # plotCombinedFigures(x, y, w, s, left=500 - 5 * dl, right=1000 - 5 * dl,
    # #                     title="Spectre lampe au sodium, avec battement , resolution resolution {0:0.2f} nm".format(dl))
    # print(-w[s.argmin(axis=0)] * 1000 )  # affiche le max de longueur d'onde
    #
    #
    # (x, y) = readVectorsFromFile('Hg_moyen_20_bat.txt')  # en microns
    # (w, f, s) = fourierTransformInterferogram(x, y)
    # # df = f[1] - f[0]
    # # dl = 0.6328 * 0.6328 * df * 1000  # x 1000 pour nm
    # # plotCombinedFigures(x, y, 2*w, s, left=500 - 5 * dl, right=1000 - 5 * dl,
    # #                     title="Spectre lampe au mercure, resolution resolution {0:0.2f} nm".format(dl))
    # print(-w[s.argmin(axis=0)] * 1000 * 2)  # affiche le max de longueur d'onde
