import numpy as np
import matplotlib.pyplot as plt
import math

longueurCircuit = 100

def getXYvectors(f, N):
    X = np.linspace(0,longueurCircuit,N)
    Y = f(X)
    return X,Y

def printFunction(X, Y):
    plt.plot(X,Y, linewidth = 9.0)
    axes = plt.gca()
    axes.set_ylim(-50, 50)
    plt.grid()
    plt.show()


#plus k est élevé, moins le cictuit a de dénivelés
def denivMax(N, k):
    return longueurCircuit/k

def generationVecteurDenivele(N, nbExtremumLocaux):
    deniv = np.zeros((N))
    dMax = denivMax(N, 20)
    positions = []
    for i in range(nbExtremumLocaux):
        pos = ((i+1)*N)//(nbExtremumLocaux+1)
        positions.append(pos)
        if (i % 2 == 0):
            deniv[pos] = dMax
        else:
            deniv[pos] = -dMax
    
    # Ajout des valeurs réelles entre les extrémums avec la méthode des interpolations linéaires (formule de Taylor Young)
    for i in range(0, positions[0]):
        deniv[i] = 0 + (i - 0) * (deniv[positions[0]] - 0) / (positions[0] - 0)

    for i in range(positions[-1], N):
        deniv[i] = deniv[positions[-1]] + (i - positions[-1]) * (deniv[N-1] - deniv[positions[-1]]) / (N - 1 - positions[-1])

    for i in range(len(positions)-1):
        start = positions[i]
        end = positions[i+1]
        for j in range(start+1, end):
            deniv[j] = deniv[start] + (j - start) * (deniv[end] - deniv[start]) / (end - start)

    
    
    # Assurez-vous de compléter cette partie avec la logique appropriée pour les segments avant le premier et après le dernier extrémum si nécessaire

    return - deniv
