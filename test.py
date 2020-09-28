from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent, pyqtSlot, pyqtSignal)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
import sys
import os
import ntpath
import json


def opendlg():

    dlg = qtw.QColorDialog()
    #dlg.setOption(QColorDialog.DontUseNativeDialog)
    dlg.setStyleSheet("""QPushButton{
    background-color: rgb(221, 51, 34);
    color: rgb(29, 29, 29);
    border: 0px solid;
    border-radius: 6px;
    }
    QPushButton:hover{
    background-color: rgb(255, 85, 68);
    }
    QPushButton:pressed{
    border: 1px solid rgb(32, 32, 32);
    }



    QLineEdit{
    color: rgb(221, 221, 221);
    background-color: rgb(48, 48, 48);
    border: 2px solid rgb(64, 64, 64);
    border-radius: 10px;
    selection-color: rgb(16, 16, 16);
    selection-background-color: rgb(221, 51, 34);
    }
    QLineEdit::focus{
    border-color: rgb(221, 51, 34);
    }""")
    dlg.exec_()



if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    #app.setWindowIcon(QIcon("D:\Files\Code\Python\RtGUI\se_logo.ico"))
    mainWindow = qtw.QMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
