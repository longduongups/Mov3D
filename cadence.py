import matplotlib.pyplot as plt
import numpy as np

def init_graph():
    fig = plt.figure(figsize=(4,4))
    manager = plt.get_current_fig_manager()
    manager.window.setGeometry(5,100,400,450)
    ax = fig.add_subplot(111)

    # Paramètres de visualisation
    ax.grid(True)
    ax.set_autoscalex_on(True)
    ax.set_autoscaley_on(True)
    ax.set_xlabel('Temps en secondes')
    ax.set_ylabel('Nombre de pas par minute')
    return(ax)

def printplt(pt,ptNew,ax):
    ax.plot([pt[0], ptNew[0]], [pt[1], ptNew[1]], 'go-', linewidth=2)

