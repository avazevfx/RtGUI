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

# UI Elements
from ui.ui_main import Ui_MainWindow
from ui.dialog_yn import Ui_Dialog as Dlg_yn
from ui.settings import Ui_Settings

#Custom Widgets
from colorpicker import ColorPicker

DGREY = "#202020"
LGREY = "#303030"
GREY = "#272727"

DRED = "#3c2020"
LRED = "#ff5544"
RED = "#dd3322"



class RtGui(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.rhost = RenderHost()
        self.rhost.outputSignal.connect(self.onOutput)

        # Make frameless & add drop shadow
        self.setWindowTitle("Scene Editor")
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        set_frameless_attrs(self, self.ui.drop_shadow_frame)
        self.setAttribute(qtc.Qt.WA_TranslucentBackground)

        # Initialize Blur Effect
        self.blur = qtw.QGraphicsBlurEffect(self)
        self.blur.setBlurRadius(7)
        self.blur.setBlurHints(qtw.QGraphicsBlurEffect.QualityHint)
        self.ui.centralwidget.setGraphicsEffect(self.blur)
        self.blur.setEnabled(False)

        self.ui.progressBar.setValue(0)

        # Initialize Settings
        self.settings = QWidget()
        self.settings.setWindowTitle("Settings")
        self.settings.ui = Ui_Settings()
        self.settings.ui.setupUi(self.settings)
        self.settings.ui.exitSettingsBtn.clicked.connect(self.exitsettings)
        set_frameless_attrs(self.settings, self.settings.ui.drop_shadow_frame)

        # Drag function bindings
        self.ui.title_bar.mouseMoveEvent = self.moveWindow
        self.ui.title_bar.mousePressEvent = self.setDragPos
        self.ui.label_title.mouseMoveEvent = self.moveWindow
        self.ui.label_title.mousePressEvent = self.setDragPos

        # Color Preview
        self.ui.difx.textChanged.connect(self.updateVis)
        self.ui.dify.textChanged.connect(self.updateVis)
        self.ui.difz.textChanged.connect(self.updateVis)
        self.ui.specx.textChanged.connect(self.updateVis)
        self.ui.specy.textChanged.connect(self.updateVis)
        self.ui.specz.textChanged.connect(self.updateVis)
        self.ui.emisx.textChanged.connect(self.updateVis)
        self.ui.emisy.textChanged.connect(self.updateVis)
        self.ui.emisz.textChanged.connect(self.updateVis)

        # Color Picking
        self.ui.diffusevis.clicked.connect(lambda: self.pick_color("diffuse"))

        # Connect Buttons to Functions
        self.ui.btn_close.clicked.connect(self.exit)
        self.ui.btn_minimize.clicked.connect(self.showMinimized)
        self.ui.addobj.clicked.connect(self.addobj)
        self.ui.delobj.clicked.connect(self.delobj)
        self.ui.applyobj.clicked.connect(self.applyobj)
        self.ui.clearobj.clicked.connect(self.clearobj)
        self.ui.obj_list.itemClicked.connect(self.loadobj)
        self.ui.addmat.clicked.connect(self.addmat)
        self.ui.delmat.clicked.connect(self.delmat)
        self.ui.applymat.clicked.connect(self.applymat)
        self.ui.clearmat.clicked.connect(self.clearmat)
        self.ui.mat_list.itemClicked.connect(self.loadmat)
        self.ui.diffusemap.clicked.connect(self.loadDiffuse)
        self.ui.specularmap.clicked.connect(self.loadSpecular)
        self.ui.normalmap.clicked.connect(self.loadNormal)
        self.ui.openbtn.clicked.connect(self.openScene)
        self.ui.savebtn.clicked.connect(self.saveScene)
        self.ui.renderbtn.clicked.connect(self.renderScene)
        self.ui.settingsbtn.clicked.connect(self.opensettings)

        # Select first input
        self.ui.objname.setFocus(True)

        #Data Variables
        self.scenepath = None
        self.savetoexit = True
        self.rrtloc = '"D:/Files/Code/Ruby Raytracer/rrt_render.rb"'
        #self.rrtloc = '"C:/Users/Avaze/Desktop/Ruby Raytracer2/rrt_render.rb"'

        self.DEFAULTMAT = {"name": "default", "difx": 200, "dify": 200, "difz": 200, "specx": 255, "specy": 255, "specz": 255, "reflectivity": 0, "emisx": 0, "emisy": 0, "emisz": 0, "diftex": None, "spectex": None, "normaltex": None, "normalstrength": 1}
        self.diffuse = None
        self.specular = None
        self.normal = None

        self.lastobjindex = None
        self.lastmatindex = None

        self.objects = []
        self.materials = [self.DEFAULTMAT]
        self.vis_materials()



    # UI Functions
    def openScene(self):
        dialog = qtw.QFileDialog()
        dialog.setNameFilter("Scene Files (*.sc)")
        dialog.setWindowTitle("Open Scene")

        if(dialog.exec_()):
            self.scenepath = str(dialog.selectedFiles()[0])
            self.ui.path_label.setText(self.scenepath)
            file = open(self.scenepath)
            data = json.load(file)

            self.objects = data["objects"]
            self.materials = data["materials"]
            sets = data["settings"]
            self.settings.ui.width.setText(str(sets["width"]))
            self.settings.ui.height.setText(str(sets["height"]))
            self.settings.ui.reflection_depth.setText(str(sets["reflection_depth"]))

            file.close()
            self.vis_objects()
            self.vis_materials()

    def saveScene(self):

        if self.scenepath == None: dialog = qtw.QFileDialog.getSaveFileName(self, "Save Scene", "C:/Users/new_scene.sc", "Scene Files (*.sc)")
        else: dialog = (self.scenepath, "")

        if(dialog != ('', '')):
            self.scenepath = dialog[0]
            self.ui.path_label.setText(self.scenepath)
            file = open(self.scenepath, "w")

            data = {"objects": self.objects, "materials": self.materials, "settings": {"width": int(self.settings.ui.width.text()), "height": int(self.settings.ui.height.text()), "reflection_depth": int(self.settings.ui.reflection_depth.text())}}

            file.write(json.dumps(data, indent=2))
            file.close()
            self.savetoexit = True

    def opensettings(self):
        self.blur.setEnabled(True)
        self.settings.show()

    def exitsettings(self):
        self.settings.close()
        self.blur.setEnabled(False)

    def renderScene(self):
        self.saveScene()
        cmd = f'ruby {self.rrtloc} ' + str(self.scenepath)
        self.ui.label_status.setText("Rendering")
        self.rhost.run(cmd)

    def exit(self):

        if self.savetoexit:
            self.close()
        else:
            self.blur.setEnabled(True)
            dialog = QDialog()
            ui = Dlg_yn()
            ui.setupUi(dialog)
            ui.title.setText("Exit App?")
            ui.title.setStyleSheet('font-size: 25pt; color: #dd3322')
            ui.description.setText("All unsaved changes will be lost")
            set_frameless_attrs(dialog, ui.dropshadow_frame)
            # Show in Middle
            w, h = dialog.frameGeometry().width(), dialog.frameGeometry().height()
            ww, wh = self.frameGeometry().width(), self.frameGeometry().height()
            dialog.setGeometry(self.pos().x() + ww/2 - w/2, self.pos().y() + wh/2 - h/2, w, h)

            if dialog.exec_():
                self.close()

            self.blur.setEnabled(False)


    # Utility
    def checkBtn(self, b):
        if b.isCheckable():
            if not b.isChecked():
                b.toggle()

    def uncheckBtn(self, b):
        if b.isCheckable():
            if b.isChecked():
                b.toggle()

    def updateVis(self):
        difx, dify, difz, specx, specy, specz, emisx, emisy, emisz = 0, 0, 0, 0, 0, 0, 0, 0, 0
        if len(self.ui.difx.text()) != 0: difx = self.ui.difx.text()
        if len(self.ui.dify.text()) != 0: dify = self.ui.dify.text()
        if len(self.ui.difz.text()) != 0: difz = self.ui.difz.text()
        if len(self.ui.specx.text()) != 0: specx = self.ui.specx.text()
        if len(self.ui.specy.text()) != 0: specy = self.ui.specy.text()
        if len(self.ui.specz.text()) != 0: specz = self.ui.specz.text()
        if len(self.ui.emisx.text()) != 0: emisz = self.ui.emisx.text()
        if len(self.ui.emisy.text()) != 0: emisy = self.ui.emisy.text()
        if len(self.ui.emisz.text()) != 0: emisz = self.ui.emisz.text()
        self.ui.diffusevis.setStyleSheet("QPushButton{border: 2px solid rgb(64, 64, 64);border-radius: 10px;" + f"background-color: rgb({difx}, {dify}, {difz});" + "}QPushButton:hover{border-color: rgb(221, 51, 34);}QPushButton:pressed{border-color: rgb(255, 102, 85);}")
        self.ui.specularvis.setStyleSheet("QPushButton{border: 2px solid rgb(64, 64, 64);border-radius: 10px;" + f"background-color: rgb({specx}, {specy}, {specz});" + "}QPushButton:hover{border-color: rgb(221, 51, 34);}QPushButton:pressed{border-color: rgb(255, 102, 85);}")
        self.ui.emissionvis.setStyleSheet("QPushButton{border: 2px solid rgb(64, 64, 64);border-radius: 10px;" + f"background-color: rgb({emisx}, {emisy}, {emisz});" + "}QPushButton:hover{border-color: rgb(221, 51, 34);}QPushButton:pressed{border-color: rgb(255, 102, 85);}")

    def onOutput(self, str):
        #self.ui.progressBar.setValue(10 * int(str.strip()[-3:-1]))
        value = int(str.strip())
        self.ui.progressViewer.setStyleSheet(f"border-radius: 10px;background-color:qconicalgradient(cx:0.5,cy:0.5,angle:90,stop:0 #272727,stop:{0.99 - value / 100.0} #272727, stop:{1 - value / 100.0} rgba(221, 51, 34, 255));")
        if value >= 10:
            if value == 100: self.ui.label_status.setText("Finished")
            self.ui.progressBar.setValue(value)
        else:
            self.ui.progressBar.setValue(0)
        self.ui.progressBar.update()

    def pick_color(self, mode):

        cp = ColorPicker()
        self.blur.setEnabled(True)


        if mode == "diffuse":
            try:
                oldr,oldg,oldb = (int(self.ui.difx.text()), int(self.ui.dify.text()), int(self.ui.difz.text()))
            except:
                oldr,oldg,olb = (0,0,0)
            r,g,b = cp.getColor((oldr,oldg,olb))
            self.ui.difx.setText(str(int(r)))
            self.ui.dify.setText(str(int(g)))
            self.ui.difz.setText(str(int(b)))

        self.blur.setEnabled(False)



    # Dragging Functions
    def setDragPos(self, event):
        self.dragPos = event.globalPos()

    def moveWindow(self, event):
        # MOVE WINDOW
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()


    # Object Functions
    def addobj(self):

        for i in range(0,99999):
            found = False
            for obj in self.objects:
                if obj["name"] == ("sphere" + str(i)):
                    found = True
                    break
            if not found:
                newname = "sphere" + str(i)
                self.objects.append({"name": newname, "posx": 0, "posy": 0, "posz": 0, "radius": 1, "material": "default"})
                break
        self.vis_objects()
        self.loadobj(len(self.objects) - 1)
        self.savetoexit = False

    def delobj(self):
        itms = self.ui.obj_list.selectedItems()
        if itms != []:
            index = self.ui.obj_list.row(itms[0])
            del self.objects[index]
            self.ui.obj_list.takeItem(index)
            self.ui.objname.clear()
            self.ui.posx.clear()
            self.ui.posy.clear()
            self.ui.posz.clear()
            self.ui.radius.clear()
            self.ui.objmat.clear()
            self.savetoexit = False

    def loadobj(self, index):

        self.ui.objname.setFocus(True)
        if type(index) == QListWidgetItem:
            indx = self.ui.obj_list.row(index)
        else:
            indx = index

        self.lastobjindex = indx
        objname = self.objects[indx]["name"]
        for obj in self.objects:
            if objname == obj["name"]:
                o = obj
                break

        self.ui.objname.setText(str(o["name"]))
        self.ui.posx.setText(str(o["posx"]))
        self.ui.posy.setText(str(o["posy"]))
        self.ui.posz.setText(str(o["posz"]))
        self.ui.radius.setText(str(o["radius"]))
        self.ui.objmat.setText(str(o["material"]))

    def applyobj(self):
        objname = self.ui.objname.text()
        if objname == "" or len(self.objects) == 0:
            return
        index = None
        for obj in self.objects:
            if objname == obj["name"]:
                index = self.objects.index(obj)

        if index == None:
            index = self.lastobjindex

        self.objects[index] = {"name": objname, "posx": self.ui.posx.text(), "posy": self.ui.posy.text(), "posz": self.ui.posz.text(), "radius": self.ui.radius.text(), "material": self.ui.objmat.text()}

        self.vis_objects()
        self.savetoexit = False

    def clearobj(self):
        self.objects = []
        self.ui.objname.clear()
        self.ui.posx.clear()
        self.ui.posy.clear()
        self.ui.posz.clear()
        self.ui.radius.clear()
        self.ui.objmat.clear()
        self.vis_objects()
        self.savetoexit = False

    def vis_objects(self):
        self.ui.obj_list.clear()
        for obj in self.objects:
            self.ui.obj_list.addItem(obj["name"])


    ## Material Functions
    def addmat(self):

        for i in range(0,99999):
            found = False
            for mat in self.materials:
                if mat["name"] == ("mat" + str(i)):
                    found = True
                    break
            if not found:
                self.materials.append({"name": "mat" + str(i), "difx": 200, "dify": 200, "difz": 200, "specx": 255, "specy": 255, "specz": 255, "reflectivity": 0, "emisx": 0, "emisy": 0, "emisz": 0, "diftex": None, "spectex": None, "normaltex": None, "normalstrength": 1})

                break
        self.vis_materials()
        self.loadmat(len(self.materials) - 1)
        self.savetoexit = False

    def delmat(self):
        itms = self.ui.mat_list.selectedItems()
        if itms != []:
            index = self.ui.mat_list.row(itms[0])
            del self.materials[index]
            self.ui.mat_list.takeItem(index)
            self.ui.matname.clear()
            self.ui.difx.clear()
            self.ui.dify.clear()
            self.ui.difz.clear()
            self.ui.specx.clear()
            self.ui.specy.clear()
            self.ui.specz.clear()
            self.ui.emisx.clear()
            self.ui.emisy.clear()
            self.ui.emisz.clear()
            self.ui.reflectivity.clear()
            self.ui.normalstrength.clear()
            self.diffuse = None
            self.specular = None
            self.normal = None
            self.savetoexit = False

    def loadmat(self, index):

        self.ui.matname.setFocus(True)
        if type(index) == QListWidgetItem:
            indx = self.ui.mat_list.row(index)
        else:
            indx = index

        self.lastmatindex = indx
        matname = self.materials[indx]["name"]
        for mat in self.materials:
            if matname == mat["name"]:
                m = mat
                break

        self.ui.matname.setText(str(m["name"]))
        self.ui.difx.setText(str(m["difx"]))
        self.ui.dify.setText(str(m["dify"]))
        self.ui.difz.setText(str(m["difz"]))
        self.ui.specx.setText(str(m["specx"]))
        self.ui.specy.setText(str(m["specy"]))
        self.ui.specz.setText(str(m["specz"]))
        self.ui.emisx.setText(str(m["emisx"]))
        self.ui.emisy.setText(str(m["emisy"]))
        self.ui.emisz.setText(str(m["emisz"]))
        self.ui.reflectivity.setText(str(m["reflectivity"]))
        self.ui.normalstrength.setText(str(m["normalstrength"]))
        self.diffuse = m["diftex"]
        self.specular = m["spectex"]
        self.normal = m["normaltex"]
        self.checkBtn(self.ui.diffusemap) if self.diffuse != None else self.uncheckBtn(self.ui.diffusemap)
        self.checkBtn(self.ui.specularmap) if self.specular != None else self.uncheckBtn(self.ui.specularmap)
        self.checkBtn(self.ui.normalmap) if self.normal != None else self.uncheckBtn(self.ui.normalmap)

    def applymat(self):
        matname = self.ui.matname.text()
        if matname == "":
            return
        index = None
        for mat in self.materials:
            if matname == mat["name"]:
                index = self.materials.index(mat)

        if index == None:
            index = self.lastmatindex

        self.materials[index] = {
            "name": matname,
            "difx": str(self.ui.difx.text()),
            "dify": str(self.ui.dify.text()),
            "difz": str(self.ui.difz.text()),
            "specx": str(self.ui.specx.text()),
            "specy": str(self.ui.specy.text()),
            "specz": str(self.ui.specz.text()),
            "reflectivity": str(self.ui.reflectivity.text()),
            "emisx": str(self.ui.emisx.text()),
            "emisy": str(self.ui.emisy.text()),
            "emisz": str(self.ui.emisz.text()),
            "diftex": self.diffuse,
            "spectex": self.specular,
            "normaltex": self.normal,
            "normalstrength": self.ui.normalstrength.text()}

        self.vis_materials()
        self.savetoexit = False

    def clearmat(self):
        self.materials = []
        self.ui.matname.clear()
        self.ui.difx.clear()
        self.ui.dify.clear()
        self.ui.difz.clear()
        self.ui.specx.clear()
        self.ui.specy.clear()
        self.ui.specz.clear()
        self.ui.emisx.clear()
        self.ui.emisy.clear()
        self.ui.emisz.clear()
        self.ui.reflectivity.clear()
        self.ui.normalstrength.clear()
        self.vis_materials()
        self.savetoexit = False

    def loadDiffuse(self):
        if self.diffuse != None:
            self.diffuse = None
            self.savetoexit = False
            return
        dialog = qtw.QFileDialog()
        dialog.setNameFilter("Image Files (*.png *.jpg *.tif *.gif)")
        dialog.setWindowTitle("Diffuse Map")

        if(dialog.exec_()):
            self.diffuse = str(dialog.selectedFiles()[0])
            self.savetoexit = False
        else:
            self.ui.diffusemap.toggle()

    def loadSpecular(self):
        if self.specular != None:
            self.specular = None
            return
        dialog = qtw.QFileDialog()
        dialog.setNameFilter("Image Files (*.png *.jpg *.tif *.gif)")
        dialog.setWindowTitle("Specular Map")

        if(dialog.exec_()):
            self.specular = str(dialog.selectedFiles()[0])
        else:
            self.ui.specularmap.toggle()

    def loadNormal(self):
        if self.normal != None:
            self.normal = None
            return
        dialog = qtw.QFileDialog()
        dialog.setNameFilter("Image Files (*.png *.jpg *.tif *.gif)")
        dialog.setWindowTitle("Normal Map")

        if(dialog.exec_()):
            self.normal = str(dialog.selectedFiles()[0])
        else:
            self.ui.normalmap.toggle()

    def vis_materials(self):
        self.ui.mat_list.clear()
        for mat in self.materials:
            self.ui.mat_list.addItem(mat["name"])


# RenderHost class for multithreaded running of the ruby raytracer engine
class RenderHost(qtc.QProcess):

    outputSignal = qtc.pyqtSignal(str)
    errorSignal = qtc.pyqtSignal(str)

    def __init__(self):
        super(RenderHost, self).__init__()

        self.readyReadStandardError.connect(self.onError)
        self.readyReadStandardOutput.connect(self.onOutput)

    def onError(self):
        error = self.readAllStandardError().data().decode()
        print(f"Error: {error}")
        self.errorSignal.emit(error)

    def onOutput(self):
        result = self.readAllStandardOutput().data().decode()
        #if result != "": print(result)
        self.outputSignal.emit(result)

    def run(self, cmd):
        self.start(cmd)


# Function to set transparent BG, frameless mode & dropshadow on dsframe
def set_frameless_attrs(object, dsframe=None):
    object.setWindowFlags(qtc.Qt.FramelessWindowHint)
    object.setAttribute(qtc.Qt.WA_TranslucentBackground)
    if dsframe != None:
        object.shadow = QGraphicsDropShadowEffect(object)
        object.shadow.setBlurRadius(17)
        object.shadow.setXOffset(0)
        object.shadow.setYOffset(0)
        object.shadow.setColor(QColor(0, 0, 0, 150))
        dsframe.setGraphicsEffect(object.shadow)

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    app.setWindowIcon(QIcon("D:\Files\Code\Python\RtGUI\se_logo.ico"))
    mainWindow = RtGui()
    mainWindow.show()
    sys.exit(app.exec_())
