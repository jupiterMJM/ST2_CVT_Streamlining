## program made for the ST2-CVT Fluid Experimental
## author: Augustin Brun - Maxence Barré - Baptiste Soriano - Simon Desclozeaux
## date: December 2023

# importation of the modules
import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib.patches as plt2


# global variables (will not change)
A, B, n = [1.95541584, 1.0539123, 0.43058145]       # set during the probe calibration


# opening and reading data from csv
tension, x_data, y_data = list(), list(), list()
with open('champ_vitesse_carre_avec_bout_les_plus_arrondis.csv', newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=';')
    for row in spamreader:
        print(row)
        tension.append(float(row["tension"].replace(',', '.')))
        x_data.append(float(row["x"].replace(',', '.')))
        y_data.append(float(row["y"].replace(',', '.')))
        x_data.append(float(row["x"].replace(',', '.')))
        y_data.append(-float(row["y"].replace(',', '.')))
        tension.append(float(row["tension"].replace(',', '.')))
tension = np.array(tension)
x_data = np.array(x_data)
y_data = np.array(y_data)

vitesses = -((tension ** 2 - A) / B) ** (1/n)       # applying King's law to get the spead 

U, V = vitesses, np.zeros((1, len(x_data)))
print(vitesses)
fig, ax = plt.subplots()

# adding the "speed front" in red
abscisses_diff = set(x_data)
coeff = .2
for i, elt in enumerate(abscisses_diff):
    matrice = np.zeros(shape = (np.sum(x_data==elt), 2))
    print(y_data[x_data==elt])
    matrice[:, 0] = y_data[x_data==elt]
    matrice[:, 1] = vitesses[x_data == elt]
    print(matrice)
    matrice = matrice[matrice[:, 0].argsort()]
    print(matrice)
    plt.plot(x_data[x_data==elt] + coeff*matrice[:, 1], np.sort(matrice[:, 0]), "-x"  ,c="red")
    plt.plot([elt]*y_data[np.logical_and(x_data==elt, vitesses < 0)].shape[-1], y_data[np.logical_and(x_data==elt, vitesses < 0)], "-o", c="black")

# setting up the plot details
plt.axis('equal')
plt.scatter(4, 3.9, c="black")
plt.scatter(4-5*coeff, 3.9, marker="x", c="red")
plt.plot((4, 4-5*coeff), (3.9, 3.9), '--')
plt.text(3.1, 3.65, "5m/s")
ax.set_xlabel("Abscissa relative to object (in cm)")
ax.set_ylabel("Ordinate relative to object (in cm)")
plt.title("Velocity field around obstacle: Rounded Square")

# plt.show()

# creating another figure
fig2, ax2 = plt.subplots()

print(x_data.shape, y_data.shape, vitesses.shape)

plt.scatter(x_data, y_data, c=np.abs(vitesses), cmap='viridis')


plt.axis('equal')
plt.colorbar()
plt.title("Velocity field around obstacle: Rounded Square")
plt.xlabel("Abscissa relative to object (in cm)")
plt.ylabel("Ordinate relative to object (in cm)")
plt.show()      # show the graph
