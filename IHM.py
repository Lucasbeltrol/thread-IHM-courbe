from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
import random
from threadSerial import Acquisition

NB_POINTS_MAX = 100
Ymax = 900

class Fenetre(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Fenetre, self).__init__()
        loadUi('IHM.ui', self)
        self.lesX = []
        self.lesY = []
        self.nbPts = 0
        self.genereCourbe()
        self.m_Acquisition = Acquisition()
        self.m_Acquisition.Signal.connect(self.ajoutPoints)
        self.btnArret.clicked.connect(self.FinAcquisition)
        self.btnAcquisition.clicked.connect(self.Demarrage)
        
    def genereCourbe(self):
        # generate the plot
        self.ax = self.graphicsView.canvas.ax
        # set specific limits for X and Y axes
        self.ax.set_xlim(1, NB_POINTS_MAX)
        self.ax.set_ylim(0, Ymax)
        self.ax.set_autoscale_on(False)
        self.courbe, = self.ax.plot(self.lesX, self.lesY,label="ma courbe")
        # generate the canvas to display the plot
        self.graphicsView.canvas.draw()
        
    def Demarrage(self):
        self.nbPts = 0
        self.courbe.set_data([],[]) # On met à jour les nouveaux couples de points à afficher
        self.graphicsView.canvas.draw()
        self.m_Acquisition.start()
        
    def FinAcquisition(self):
        self.m_Acquisition.arret()

    def ajoutPoints(self,voltage):  # Appelée à chaque clic sur le bouton
        print(voltage)
        self.nbPts += 1
        self.lesX.append(self.nbPts)  # Ajout d'une nouvelle abscisse

        self.lesY.append(int(voltage)) # Ajout d'une nouvelle ordonnée
        
        if len(self.lesX) > NB_POINTS_MAX: # Si on dépasse le nb de points à afficher...
            self.lesX = self.lesX[1:] # Suppression du premier élément pour avoir une fenêtre glissante
            self.lesY = self.lesY[1:]
            self.ax.set_xlim(self.nbPts - NB_POINTS_MAX + 1, self.nbPts) # On réajuste l'échelle de l'axe des X
        
        
        
#        
#        if Ymax != int(voltage.split(';')[1]) :
#            Ymax = int(voltage.split(';')[1])
#        
        
        
        
        self.courbe.set_data(self.lesX, self.lesY) # On met à jour les nouveaux couples de points à afficher
        self.graphicsView.canvas.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = Fenetre()
    win.show()
    app.exec_()