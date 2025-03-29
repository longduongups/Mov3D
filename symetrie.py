import matplotlib.pyplot as plt
import numpy as np

def init_graph():
    fig = plt.figure(figsize=(3, 2))
    manager = plt.get_current_fig_manager()
    manager.window.setGeometry(5,600,302,266)
    ax = fig.add_subplot(111)

    # Paramètres de visualisation
    ax.grid(False)
    ax.set_autoscalex_on(True)
    ax.set_autoscaley_on(True)
    ax.set_title("Symétrie de la longueur des pas")
    return(ax)

def printplt(ax,left,right):
    if(left>0):
        sizes=[left/(left+right)*100,abs(right)/(left+right)*100]
        print(sizes)
    else :
        sizes=[0,100]
    labels = ['Gauche', 'Droite']
    colors = ['lightblue', 'gold']
    ax.clear()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',startangle=90)