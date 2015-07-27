from PyQt4 import QtCore, QtGui
import numpy as np
import sys, math, random

from lib import *

class MainWindow(QtGui.QMainWindow):
    scene = sceneView = zoomToolBar = None
    _rows = 15
    _cols = 15

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Game of Life :)")

#        self.createActions()
#        self.createMenus()
        self.createStatusBar()
#        self.createToolBar()

        self.createScene()

        self.createMainWidget()

        self.showMaximized()
        self.setUnifiedTitleAndToolBarOnMac(True)

    def createMainWidget(self):
        mainWidget = QtGui.QWidget(self)
        hbox = QtGui.QHBoxLayout()

        hbox.addWidget(self.sceneView)

        form = QtGui.QFormLayout()
        formWidget = QtGui.QWidget()
        formWidget.setFixedWidth(200)

        rowBox = QtGui.QHBoxLayout()
        self.run = QtGui.QPushButton("Run")

        rowBox.addWidget(self.run)
        self.stop = QtGui.QPushButton("Stop")
        self.stop.setEnabled(False)
        rowBox.addWidget(self.stop)
        form.addRow(rowBox)
        self.run.clicked.connect(self.runClick)
        self.stop.clicked.connect(self.stopClick)

        groupBox = QtGui.QGroupBox('Zoom', formWidget)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)
        self.slider.setMinimum(1)
        self.slider.setMaximum(20)
        self.slider.setValue(5)
        self.slider.valueChanged.connect(self.zoomChange)

        slidersLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        slidersLayout.addWidget(self.slider)
        groupBox.setLayout(slidersLayout)

        form.addRow(groupBox)

        formWidget.setLayout(form)
        hbox.addWidget(formWidget)

        mainWidget.setLayout(hbox)
        self.setCentralWidget(mainWidget)

        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self._onTimeout)

    def _onTimeout(self):
        self._grid.calcNextState()

    def stopClick(self):
        self.run.setEnabled(True)
        self.stop.setEnabled(False)
        self.timer.stop()

    def runClick(self):
        self.run.setEnabled(False)
        self.stop.setEnabled(True)
        self.timer.start(500)

    def zoomChange(self, value):
        self.sceneView.resetMatrix()
        self.sceneView.scale(value, value)

    def createScene(self):
        self._grid = Grid('square', self._cols, self._rows)
        width, height = self._grid.getSize()

        bg = QtGui.QColor('#ffffff')
        grey = QtGui.QColor('#dddddd')
        self.scene = QtGui.QGraphicsScene(0, 0, width, height)
        self.scene.addRect(QtCore.QRectF(0, 0, width, height), QtGui.QPen(bg), QtGui.QBrush(bg))

        self._grid.createView(self.scene)

        self.sceneView = QtGui.QGraphicsView()
        self.sceneView.setBackgroundBrush(QtGui.QBrush(grey))
        self.sceneView.setRenderHints(QtGui.QPainter.Antialiasing)
        self.sceneView.scale(15, 15)
        self.sceneView.setContentsMargins(0, 0, 0, 0)
        self.sceneView.setEnabled(True)
        self.sceneView.setScene(self.scene)

    def createActions(self):
        self.saveAct = QtGui.QAction('&Save', self, shortcut=QtGui.QKeySequence.Save,
                statusTip="Save the current form letter",
                triggered=self.save)

        self.openAct = QtGui.QAction("&Open...", self, shortcut=QtGui.QKeySequence.Open,
                statusTip="Open an existing file", triggered=self.open)

    """
    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                    "Choose a file name", '.', "Grid (*.grd)")
        if not fileName:
            return

        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.ReadOnly):
            QtGui.QMessageBox.warning(self, "Application",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return

        self._grid.load(file)
        self.statusBar().showMessage("File loaded", 2000)


    def save(self):
        filename = QtGui.QFileDialog.getSaveFileName(self,
                "Choose a file name", '.', "Grid (*.grd)")

        if not filename:
            return

        file = QtCore.QFile(filename)
        if not file.open(QtCore.QFile.WriteOnly):
            QtGui.QMessageBox.warning(self, "Game of Life :)",
                    "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return

        self._grid.save(file)
        self.statusBar().showMessage("Saved '%s'" % filename, 2000)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()

    def createToolBar(self):
        self.fileToolBar = self.addToolBar("file")
    """

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())