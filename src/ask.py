import numpy as np
from rich.console import Console
from rich.markdown import Markdown




def parseFunction(stringFunction):
    local_namespace = {}
    try:
        stringExec = f"def user_func(x): return {stringFunction}"

        # Exécution dans un espace de noms local avec numpy pour la vectorisation
        exec(stringExec, {"__builtins__": None, "np": np}, local_namespace)
        # On récupère de la fonction créée
        function = local_namespace['user_func']
        # Test de la fonction avec un tableau NumPy
        test_val = np.array([0])  
        function(test_val)
        return function
    
    except Exception as e:
        return f"Erreur dans la fonction fournie : {e}"
    
def ask():
    console = Console()
    with open("introduction.md") as readme:
        markdown = Markdown(readme.read())
    console.print(markdown)
    

    string = input("f(x) = ")
    function = parseFunction(string)

    # Vérifie si la fonction est exécutable, sinon, affiche l'exception (par exemple : divided by 0)

    if not callable(function):
        print(function)
        return
    '''
    print("Do you want to generate a gradient for this track?")
    print("0. No")
    print("1. Yes")
    deniv = int(input())'''
    deniv = 0
    if deniv == 1:
        deniv = True
    else:
        deniv = False



    return function, deniv