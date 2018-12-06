#!python3
import sys
from ui import mainWindow
from ui.progress import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QMainWindow()
    ui = mainWindow.Ui_MainWindow()
    ui.setupUi(main)
    form_window = QWidget()
    form = Ui_Form()
    form.setupUi(form_window)

    ui.pushButton.clicked.connect(lambda: ui.start(main, form_window))
    main.show()
    sys.exit(app.exec_())
