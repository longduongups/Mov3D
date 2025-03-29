import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import os
# Fonction pour mettre à jour la position des deux bâtons et des articulations en fonction des angles de la hanche et du genou
def update_position(hip_angle, knee_angle, hip_y,hip_z ):
    length_thigh = 3 / 3
    length_calf = 2 / 3
    # Position de la hanche
    hip_x = -1
    hip_z = 1.5

    # Position du genou
    knee_x = hip_x + length_thigh * np.cos(hip_angle)
    knee_y = hip_y + length_thigh * np.sin(hip_angle)
    knee_z = hip_z - length_thigh * np.sin(hip_angle)

    # Calculer les coordonnées des extrémités du premier bâton (cuisse)
    x_thigh = [hip_x, knee_x]
    y_thigh = [hip_y, knee_y]
    z_thigh = [hip_z, knee_z]

    # Position de la cheville
    ankle_x = knee_x + length_calf * np.cos(knee_angle)
    ankle_y = knee_y + length_calf * np.sin(knee_angle)
    ankle_z = knee_z - length_calf * np.sin(knee_angle)

    # Calculer les coordonnées des extrémités du deuxième bâton (mollet)
    x_calf = [knee_x, ankle_x]
    y_calf = [knee_y, ankle_y]
    z_calf = [knee_z, ankle_z]

    return x_thigh, y_thigh, z_thigh, x_calf, y_calf, z_calf, hip_x, hip_y, hip_z, knee_x, knee_y, knee_z, ankle_x, ankle_y, ankle_z

def update_leg(hip_entry1, knee_entry1, hip_entry2, knee_entry2,line_thigh1,line_calf1,hip_joint1,knee_joint1,ankle_joint1,line_thigh2,line_calf2,hip_joint2,knee_joint2,ankle_joint2,line_leg_connector,fig):
    hip_angle1 = float(hip_entry1) * np.pi / 180
    knee_angle1 = float(knee_entry1) * np.pi / 180
    hip_angle2 = float(hip_entry2) * np.pi / 180
    knee_angle2 = float(knee_entry2) * np.pi / 180

    x_thigh1, y_thigh1, z_thigh1, x_calf1, y_calf1, z_calf1, hip_x1, hip_y1, hip_z1, knee_x1, knee_y1, knee_z1, ankle_x1, ankle_y1, ankle_z1 = update_position(hip_angle1, knee_angle1, -1,1)
    x_thigh2, y_thigh2, z_thigh2, x_calf2, y_calf2, z_calf2, hip_x2, hip_y2, hip_z2, knee_x2, knee_y2, knee_z2, ankle_x2, ankle_y2, ankle_z2 = update_position(hip_angle2, knee_angle2, -1/3,1.5)

    line_thigh1.set_xdata(x_thigh1)
    line_thigh1.set_ydata(y_thigh1)
    line_thigh1.set_3d_properties(z_thigh1)

    line_calf1.set_xdata(x_calf1)
    line_calf1.set_ydata(y_calf1)
    line_calf1.set_3d_properties(z_calf1)

    hip_joint1.set_data(hip_x1, hip_y1)
    hip_joint1.set_3d_properties(hip_z1)

    knee_joint1.set_data(knee_x1, knee_y1)
    knee_joint1.set_3d_properties(knee_z1)

    ankle_joint1.set_data(ankle_x1, ankle_y1)
    ankle_joint1.set_3d_properties(ankle_z1)

    line_thigh2.set_xdata(x_thigh2)
    line_thigh2.set_ydata(y_thigh2)
    line_thigh2.set_3d_properties(z_thigh2)

    line_calf2.set_xdata(x_calf2)
    line_calf2.set_ydata(y_calf2)
    line_calf2.set_3d_properties(z_calf2)

    hip_joint2.set_data(hip_x2, hip_y2)
    hip_joint2.set_3d_properties(hip_z2)

    knee_joint2.set_data(knee_x2, knee_y2)
    knee_joint2.set_3d_properties(knee_z2)

    ankle_joint2.set_data(ankle_x2, ankle_y2)
    ankle_joint2.set_3d_properties(ankle_z2)

    # Relier les chevilles des deux jambes par une ligne
    line_leg_connector.set_data([hip_x1, hip_x2], [hip_y1, hip_y2])
    line_leg_connector.set_3d_properties([hip_z1, hip_z2])

    fig.canvas.draw()

def init_jambes():

	# Initialiser la figure 3D
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	# Paramètres de visualisation
	#ax.set_axis_off()  # Désactiver les axes
	ax.grid(True)    # Désactiver la grille
	ax.set_xlim([-2, 2])
	ax.set_ylim([-2, 2])
	ax.set_zlim([0, 3])
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	ax.view_init(elev=-105, azim=-90 ,vertical_axis='y')  # Vue de profil

	# Tracer les bâtons initiaux avec des angles de la hanche et du genou arbitraires
	initial_hip_angle = np.pi / 6  # Angle initial de la hanche
	initial_knee_angle = np.pi / 6  # Angle initial du genou

	x_thigh1, y_thigh1, z_thigh1, x_calf1, y_calf1, z_calf2, hip_x1, hip_y1, hip_z1, knee_x1, knee_y1, knee_z1, ankle_x1, ankle_y1, ankle_z1 = update_position(initial_hip_angle, initial_knee_angle, -1,1)
	x_thigh2, y_thigh2, z_thigh2, x_calf2, y_calf2, z_calf1, hip_x2, hip_y2, hip_z2, knee_x2, knee_y2, knee_z2, ankle_x2, ankle_y2, ankle_z2 = update_position(initial_hip_angle, initial_knee_angle, -1/3,1.5)

	line_thigh1, = ax.plot(x_thigh1, y_thigh1, z_thigh1,color='red')
	line_calf1, = ax.plot(x_calf1, y_calf1, z_calf1,color='red')

	hip_joint1, = ax.plot([hip_x1], [hip_y1], [hip_z1], marker='o', color='red', markersize=8)  # Ajouter une sphère pour la hanche
	knee_joint1, = ax.plot([knee_x1], [knee_y1], [knee_z1], marker='o', color='red', markersize=8)  # Ajouter une sphère pour le genou
	ankle_joint1, = ax.plot([ankle_x1], [ankle_y1], [ankle_z1], marker='o', color='red', markersize=8)  # Ajouter une sphère pour la cheville

	line_thigh2, = ax.plot(x_thigh2, y_thigh2, z_thigh2,color='blue')
	line_calf2, = ax.plot(x_calf2, y_calf2, z_calf2,color='blue')
	hip_joint2, = ax.plot([hip_x2], [hip_y2], [hip_z2], marker='o', color='blue', markersize=8)  # Ajouter une sphère pour la hanche
	knee_joint2, = ax.plot([knee_x2], [knee_y2], [knee_z2], marker='o', color='blue', markersize=8)  # Ajouter une sphère pour le genou
	ankle_joint2, = ax.plot([ankle_x2], [ankle_y2], [ankle_z2], marker='o', color='blue', markersize=8)  # Ajouter une sphère pour la cheville

	# Tracer une ligne reliant les chevilles des deux jambes
	line_leg_connector, = ax.plot([ankle_x1, ankle_x2], [ankle_y1, ankle_y2], [ankle_z1, ankle_z2], color='green')
    
	return(line_thigh1,line_calf1,hip_joint1,knee_joint1,ankle_joint1,line_thigh2,line_calf2,hip_joint2,knee_joint2,ankle_joint2,line_leg_connector,fig)
