from tools.UI.ui import MainWindow, QApplication, sys


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
