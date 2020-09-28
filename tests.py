import sys

from PyQt5 import QtCore, QtGui, QtWidgets

class Console(QtWidgets.QWidget):
    errorSignal = QtCore.pyqtSignal(str)
    outputSignal = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.editor = QtWidgets.QPlainTextEdit(self)
        self.editor.setReadOnly(True)
        self.font = QtGui.QFont()
        # self.font.setFamily(editor["editorFont"])
        self.font.setPointSize(12)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.editor, 1)
        self.setLayout(self.layout)
        self.output = None
        self.error = None
        self.editor.setFont(self.font)
        self.process = QtCore.QProcess()
        self.process.readyReadStandardError.connect(self.onReadyReadStandardError)
        self.process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)

    def onReadyReadStandardError(self):
        error = self.process.readAllStandardError().data().decode()
        self.editor.appendPlainText(error)
        self.errorSignal.emit(error)

    def onReadyReadStandardOutput(self):
        result = self.process.readAllStandardOutput().data().decode()
        self.editor.appendPlainText(result)
        self.outputSignal.emit(result)


    def run(self, command):
        """Executes a system command."""
        # clear previous text
        self.editor.clear()
        self.process.start(command)

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
        print(f"Output: {result}")
        self.outputSignal.emit(result)

    def run(self, cmd):
        self.start(cmd)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Console()
    w.show()
    w.errorSignal.connect(lambda error: print(error))
    w.outputSignal.connect(lambda output: print(output))
    w.run("ping google.com -t")
    sys.exit(app.exec_())
