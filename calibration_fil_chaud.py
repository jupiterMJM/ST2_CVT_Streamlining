## CVT - Modélisation
## projet streamlining
## programme de calibration du fil chaud
## auteur: Augustin, Simon, Baptiste, Maxence

# importation des modules
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv

# définition de la fonction modèle
def func(x, A, B, n):
    """
    le modèle de fonction que l'on cherche à fit
    """
    return A + B* x**n

# ouverture et lecture du fichier csv
x_data, y_data = list(), list()
with open('ST_expe_1.csv', newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
        x_data.append(float(row["vitesse"].replace(',', '.')))
        y_data.append(float(row["tensionc"].replace(',', '.')))

# curve_fit de la fonction
popt2, pcov2 = curve_fit(func, x_data[1:], y_data[1:])
# popt contient les paramètres fit / pcov contient les std

# affichage des résultats
print("bis popt", popt2)
print("std", np.sqrt(np.diag(pcov2)))
print("ecart type:", np.sqrt(np.mean((y_data-func(x_data, *popt2))**2)))

# affichage des graphes
plt.scatter(x_data, y_data, label = "Experimental Data")
x_test = np.arange(0, 15, 0.1)
plt.plot(x_test, func(x_test, *popt2), label="curve_fit of the King's law")
plt.xlabel("Air speed (m/s)")
plt.ylabel("Tension squared (V^2)")
plt.title("King's law (experimental)")
plt.legend()
plt.show()