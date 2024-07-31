'''
Ce fichier a pour but de former des gifs 3D de la totalite des patterns 
se trouvant dans le fichier testTraining.csv.
Les patrons doivent être de format 100 Lignes X 95 Colonnes tel que dans 
le CSV d'origine.
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

df = pd.read_csv('csv/testTraining.csv', header=None)
num_sets = df.shape[0] // 100 

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def animate(n):
    ax.cla()

    start_row = n * 100 + 1  
    end_row = (n + 1) * 100
    Z = df.iloc[start_row:end_row, :].values
    x = np.linspace(-50, 50, Z.shape[0])  
    y = np.linspace(-47, 47, Z.shape[1]) 


    X, Y = np.meshgrid(y, x)
    ax.set_ylim(-50,50)
    ax.set_xlim(-47,47)
    ax.set_zlabel('Power [dBm]')
    ax.set_ylabel('EL [°]')
    ax.set_xlabel('AZ [°]')
    ax.set_zlim(-40,-5)
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_title('3D plot from 90° to 0°')

    return fig,


anim = FuncAnimation(fig=fig, func=animate, frames=45, interval=0.1, repeat=True)
plt.show()

anim.save('patternsAnim/A.gif',fps=5)