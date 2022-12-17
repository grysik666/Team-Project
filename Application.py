from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QFileDialog


class Application(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interface()
        
    def interface(self):

        self.resize(200, 200)
        self.setWindowTitle("Aplikacja")
        layoutT = QGridLayout()

        self.setLayout(layoutT)
        self.setGeometry(800, 300, 250, 250)
        self.setWindowTitle("Aplikacja")
        self.show()
        # przyciski
        own_values = QPushButton("Własne parametry", self)
        #own_values.resize(own_values.sizeHint())
        random_values = QPushButton("Losowe wartosci", self)
        random_values_by_user = QPushButton("Podaj przykładowe wartosci", self)
        #random_values.resize(random_values.sizeHint())
        exit_Button = QPushButton("Koniec", self)
        #exit_Button.resize(exit_Button.sizeHint())
        
        layoutH = QVBoxLayout()
        layoutH.addWidget(own_values)
        layoutH.addWidget(random_values)
        layoutH.addWidget(random_values_by_user)
        layoutH.addWidget(exit_Button)
        
        layoutT.addLayout(layoutH, 0, 0, 1, 3)
        exit_Button.clicked.connect(self.finish)
        own_values.clicked.connect(self.open_file)
        
    def open_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Otwórz plik", "", "Wszystkie pliki (*);; Plik tekstowy (*.txt)")

    def finish(self):
        self.close()
        sys.exit(app.exec_())

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    okno = Application()
    sys.exit(app.exec_())