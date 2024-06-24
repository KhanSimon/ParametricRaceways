# Parametric Raceways
demo (image clicable):
[![Video link](https://img.youtube.com/vi/sotObIvhX3Q/0.jpg)](https://www.youtube.com/watch?v=sotObIvhX3Q)


Ce projet est un jeu dans lequel l'utilisateur rentre une fonction mathématiques et peut ainsi contrôler une voiture sur la route créée à partir de la fonction mathématique saisie.

**Installation**

Vous aurez besoin de PyOpenGL, GLFW, Rich et Numpy dans votre machine. Pour les installer sasir la commande :

```
pip3 install -r requirements.txt

```

**Lancer l'application** 

Pour lancer le jeu :

```
python3 ./src/viewer.py

```

Ensuite le terminal demandera de saisir la fonction qui devra être de la forme "np.cos(x)" en utilisant la librairie numpy pour les fonctions complexes.

Il faut savoir que toutes les fonctions ne sont pas compatibles, choisir de préférence une fonction telle que f(0) = 0 ou telle que l'ordonnée à l'origine soit proche de 0.

Exemples de fonctions adaptées :

- 0 (straight line)
- np.cos(x)
- np.sqrt(x)
- np.cos(np.power(x, 7/10))
- 1.4*np.cos(x)*np.log(x+0.3)
- 1 - np.exp(np.sin(x/3))

Le terminal proposera le choix entre une route avec dénivelé et sans. Seule la route sans dénivelé fonctionne pour l'instant. Nous n'avons pas eu le temps d'implémenter les dénivelés.

**Jeu**

Lors du jeu vous pouvez vous déplacez avec les touches Z, Q, S, D et accélérer avec espace :

- Z : Avancer
- S : Reculer
- Q : Tourner à gauche
- D : Tourner à droite
- Espace : Accélérer

Le but du jeu est d'arriver au bout de la route.
