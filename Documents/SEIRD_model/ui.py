## Libraries
# Python Libraries
import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt
import math
import sys
import base64

# PyQt libraries
from PyQt5.QtGui import QPixmap, QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
QVBoxLayout)

# Local Libraries
import seird

class ModelDialog(QDialog):
  def __init__(self):
    super(ModelDialog, self).__init__()

    self.setWindowTitle("SEIRD Model Generation")
    self.createMainWindowLayout()

    self.top = 0
    self.left = 0
    self.width = 640
    self.height = 480
    self.setGeometry(self.left, self.top, self.width, self.height)

  def createMainWindowLayout(self):
    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttonBox.accepted.connect(self.runModel)
    buttonBox.rejected.connect(self.reject)

    mainLayout = QVBoxLayout()

    self.createDiagramGroupBox()
    self.createPopulationGroupBox()
    self.createDiseaseGroupBox()
    
    mainLayout.addWidget(self.diagramGroup)
    mainLayout.addWidget(self.populationGroup)
    mainLayout.addWidget(self.diseaseGroup)
    mainLayout.addWidget(buttonBox)
    self.setLayout(mainLayout)

  def createDiagramGroupBox(self):
    self.diagramGroup = QGroupBox("SEIRD Diagram")
    diagramLayout = QFormLayout()

    pixmap = QPixmap("seird.png")
    pixmap = pixmap.scaledToWidth(500)

    labelImage = QLabel(self)
    labelImage.setPixmap(pixmap)
    diagramLayout.addWidget(labelImage)
    
    self.diagramGroup.setLayout(diagramLayout)

  def createPopulationGroupBox(self):
    floatRegExpression = QRegExp("[0-9]+.?[0-9]{,4}")
    integerRegExpression = QRegExp("\d+")

    self.populationGroup = QGroupBox("Population Parameters")
    populationLayout = QFormLayout()

    self.populationLE = QLineEdit()
    populationLayout.addRow(QLabel("Population (N):"))
    inputValidator = QRegExpValidator(integerRegExpression, self.populationLE)
    self.populationLE.setValidator(inputValidator)
    populationLayout.addWidget(self.populationLE)

    self.initialSeedLE = QLineEdit()
    populationLayout.addRow(QLabel("Initial Number of Infected (E[0]):"))
    inputValidator = QRegExpValidator(integerRegExpression, self.initialSeedLE)
    self.initialSeedLE.setValidator(inputValidator)
    populationLayout.addWidget(self.initialSeedLE)

    self.daysModelLE = QLineEdit()
    populationLayout.addRow(QLabel("Number of Days to Model:"))
    inputValidator = QRegExpValidator(integerRegExpression, self.daysModelLE)
    self.daysModelLE.setValidator(inputValidator)
    populationLayout.addWidget(self.daysModelLE)

    self.socDistanceResponseFactorLE = QLineEdit()
    populationLayout.addRow(QLabel("Social Distance Response Factor:"))
    inputValidator = QRegExpValidator(floatRegExpression, self.socDistanceResponseFactorLE)
    self.socDistanceResponseFactorLE.setValidator(inputValidator)
    populationLayout.addWidget(self.socDistanceResponseFactorLE)
    
    self.socDistanceDayLE = QLineEdit()
    populationLayout.addRow(QLabel("Social Distance Day (x):"))
    inputValidator = QRegExpValidator(integerRegExpression, self.socDistanceDayLE)
    self.socDistanceDayLE.setValidator(inputValidator)
    populationLayout.addWidget(self.socDistanceDayLE)

    self.diseaseScalingFactorLE = QLineEdit()
    inputValidator = QRegExpValidator(floatRegExpression, self.diseaseScalingFactorLE)
    self.diseaseScalingFactorLE.setValidator(inputValidator)
    populationLayout.addRow(QLabel("Disease Scaling Factor:"))
    populationLayout.addWidget(self.diseaseScalingFactorLE)

    self.populationGroup.setLayout(populationLayout)   
  def createDiseaseGroupBox(self):
    floatRegExpression = QRegExp("[0-9]+.?[0-9]{,2}")

    self.diseaseGroup = QGroupBox("Disease Parameters")
    diseaseLayout = QFormLayout()

    self.r0LE = QLineEdit()
    inputValidator = QRegExpValidator(floatRegExpression, self.r0LE)
    self.r0LE.setValidator(inputValidator)
    diseaseLayout.addRow(QLabel("Basic Reproductive Number of Disease Before Social Distancing (R0=β0/γ):"))
    diseaseLayout.addWidget(self.r0LE)

    self.r1LE = QLineEdit()
    inputValidator = QRegExpValidator(floatRegExpression, self.r1LE)
    self.r1LE.setValidator(inputValidator)
    diseaseLayout.addRow(QLabel("Basic Reproductive Number of Disease After Social Distancing (Rc=βc/γ):"))
    diseaseLayout.addWidget(self.r1LE)

    self.gammaLE = QLineEdit()
    inputValidator = QRegExpValidator(floatRegExpression, self.gammaLE)
    self.gammaLE.setValidator(inputValidator)
    diseaseLayout.addRow(QLabel("The rate of an infectious person recovering (γ=1/Days):"))
    diseaseLayout.addWidget(self.gammaLE)

    self.alphaLE = QLineEdit()
    inputValidator = QRegExpValidator(floatRegExpression, self.alphaLE)
    self.alphaLE.setValidator(inputValidator)
    diseaseLayout.addRow(QLabel("Probability the disease will kill an infected person (α)"))
    diseaseLayout.addWidget(self.alphaLE)

    self.rhoLE = QLineEdit()
    inputValidator = QRegExpValidator(floatRegExpression, self.rhoLE)
    self.rhoLE.setValidator(inputValidator)
    diseaseLayout.addRow(QLabel("Average Fatality Rate per Day (ρ):"))
    diseaseLayout.addWidget(self.rhoLE)

    self.sigmaLE = QLineEdit()
    inputValidator = QRegExpValidator(floatRegExpression, self.sigmaLE)
    self.sigmaLE.setValidator(inputValidator)
    diseaseLayout.addRow(QLabel("Probability an exposed person becomes an infectious (σ):"))
    diseaseLayout.addWidget(self.sigmaLE)

    self.diseaseGroup.setLayout(diseaseLayout)

  # def validateInputInteger(input):


  # def validateInputInteger(input):
        
  def runModel(self):
    ## Extract values from Input
    population = int(self.populationLE.text())
    inititalInfected = int(self.initialSeedLE.text())
    daysModel = int(self.daysModelLE.text())
    socDistResponseFactor = float(self.socDistanceResponseFactorLE.text())
    thrDay = int(self.socDistanceDayLE.text())
    diseaseScalingFactor = float(self.diseaseScalingFactorLE.text())
    r0 = float(self.r0LE.text())
    r1 = float(self.r1LE.text())
    baseAlpha = float(self.alphaLE.text())
    rho = float(self.rhoLE.text())
    sigma = float(self.sigmaLE.text())
    gamma = float(self.gammaLE.text())

    modelInstance = seird.seird(r0, r1, gamma, sigma,
      baseAlpha, rho, socDistResponseFactor, diseaseScalingFactor)
    X, S, E, I, R, D = modelInstance.solve(population, inititalInfected, thrDay, daysModel)

    # Plot percentages of Population
    fig = plt.figure(dpi=75, figsize=(20,16))
    ax = fig.add_subplot(111)
    ax.plot(X, S/population*100, 'o', color='green', label='Susceptible')
    ax.plot(X, E/population*100, 'o', color='yellow', label='Exposed (realtime)')
    ax.plot(X, I/population*100, 'o', color='red', label='Infected (realtime)')
    ax.plot(X, R/population*100, 'o', color='blue', label='Recovered')
    ax.plot(X, D/population*100, '-', color='grey', label='Dead (Disease)')

    # Plot threshold day
    plt.axvline(x=thrDay, color='black')
    plt.annotate('Social Distancing Threshold Day', xy=(thrDay + 2, 95))

    # Prepare plot for viewing
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('% Of Population' + str(population))
    ax.set_ylim(bottom=0.0, top=100.0)
    legend = ax.legend(title='SEIRD model')

    # Display plot
    plt.show()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  dialog = ModelDialog()
  sys.exit(dialog.exec_())