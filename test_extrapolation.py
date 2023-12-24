## program made for the ST2-CVT Fluid Experimental
## author: Augustin Brun - Maxence Barré - Baptiste Soriano - Simon Desclozeaux
## date: December 2023

# importation of the modules
import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.spatial import cKDTree

# global variables
A, B, n = [1.95541584, 1.0539123, 0.43058145]


# opening and reading the csv file
tension, x_data, y_data = list(), list(), list()
with open('champ_vitesse_carre_plat.csv', newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=';')
    for row in spamreader:
        tension.append(float(row["tension"].replace(',', '.')))
        x_data.append(float(row["x"].replace(',', '.')))
        y_data.append(float(row["y"].replace(',', '.')))
        x_data.append(float(row["x"].replace(',', '.')))
        y_data.append(-float(row["y"].replace(',', '.')))
        tension.append(float(row["tension"].replace(',', '.')))
tension = np.array(tension)
x_data = np.array(x_data)
y_data = np.array(y_data)

vitesses = -((tension ** 2 - A) / B) ** (1/n)

# The heart of this program: the extrapolation of the data
# this part of the algorithm (and only this part) has been inspired by using the ChatGPT tool
# creating a regular grid of points used to extrapolate the data
x_min, x_max = min(x_data), max(x_data)
y_min, y_max = min(y_data), max(y_data)
x_range = np.linspace(x_min, x_max, 100)
y_range = np.linspace(y_min, y_max, 100)
x_grid, y_grid = np.meshgrid(x_range, y_range)

# grouping the coordinates (x,y) of the experimental data into a 2 dimensions array
data_points = np.column_stack((x_data, y_data))
tree = cKDTree(data_points)     # creation of a tree to look to the nearest neighboors

nb_voisins = 2  # number of neighboors considered to the extrapolation
# parameter set up to have the most usesful graph

distances, indices = tree.query(np.column_stack((x_grid.ravel(), y_grid.ravel())), k=nb_voisins)  # look to the nearest neighboors for every point
vitesses_extrapolees = np.mean(vitesses[indices], axis=1)   # calculing the extrapolated speed
vitesses_extrapolees = vitesses_extrapolees.reshape(x_grid.shape)

# plotting
plt.scatter(x_data, y_data, c=np.abs(vitesses), cmap='viridis', label='Experimental Data')
plt.colorbar(label='Air speed (in m/s)')
plt.scatter(x_grid, y_grid, c=np.abs(vitesses_extrapolees), cmap='viridis', marker='s', alpha=.2, label='Extrapolation')
plt.xlabel("Abscissa relative to object (in cm)")
plt.ylabel("Ordinate relative to object (in cm)")
plt.title("Velocity colormap (extrapolated) around obstacle: Square")
plt.grid(True)
plt.axis("equal")
plt.legend()
plt.show()
