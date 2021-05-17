import sys
import os
import qdarkstyle
from qdarkstyle.dark.palette import DarkPalette  # noqa: E402
from qdarkstyle.light.palette import LightPalette
from PyQt5 import QtWidgets,QtCore,QtGui,uic


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
uic.loadUi(('E:\\Project\\ProCCMTest\\ProCCMTest\\UI\\ui_MainWindow.ui'), window)

style = qdarkstyle.load_stylesheet(palette=DarkPalette)
#style = qdarkstyle.load_stylesheet(palette=LightPalette)
app.setStyleSheet(style)


# run
window.show()
app.exec_()
