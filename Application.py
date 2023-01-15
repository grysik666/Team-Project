from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QScrollArea
from PyQt5.QtWidgets import QGridLayout, QLabel, QInputDialog
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QFileDialog
import Algorithm
import Graph
import random

class ScrollMessageBox(QMessageBox):
   def __init__(self, *args, **kwargs):
      QMessageBox.__init__(self, *args, **kwargs)
      chldn = self.children()
      scrll = QScrollArea(self)
      scrll.setWidgetResizable(True)
      grd = self.findChild(QGridLayout)
      lbl = QLabel(chldn[1].text(), self)
      lbl.setWordWrap(True)
      scrll.setWidget(lbl)
      scrll.setMinimumSize (680,250)
      scrll.setWidgetResizable(True)
      grd.addWidget(scrll,0,1)
      chldn[1].setText('')
      self.exec_()
      
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
        random_values = QPushButton("Losowe wartosci", self)
        random_values_by_user = QPushButton("Podaj przykładowe wartosci", self)
        exit_Button = QPushButton("Koniec", self)
        
        layoutH = QVBoxLayout()
        layoutH.addWidget(own_values)
        layoutH.addWidget(random_values)
        layoutH.addWidget(random_values_by_user)
        layoutH.addWidget(exit_Button)
        
        layoutT.addLayout(layoutH, 0, 0, 1, 3)
        exit_Button.clicked.connect(self.finish)
        random_values.clicked.connect(self.random_values)
        random_values_by_user.clicked.connect(self.values_generated_by_user)
        own_values.clicked.connect(self.open_file)
          
    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Otwórz plik", "", "Wszystkie pliki (*);; Plik tekstowy (*.txt)")
        Centre, Capacity, House = Algorithm.load_from_file(path)
        G = Algorithm.Hungarian_Algorithm(Centre, Capacity, House)
        M, Result, StringResult = G.main_algorithm(True)
        StrResult = 'Łączna odległość pomiędzy połączonymi centrami i domami wynosi ' + str(round(Result, 3)) + ' km'
        Box = ScrollMessageBox(1, "Wynik", StrResult + '\n' + StringResult, QMessageBox.Save | QMessageBox.Ok)
        ret = Box.exec_()
        if ret == QMessageBox.Save:
            with open('Results.txt', 'w') as f:
                f.write(StrResult + '\n' + StringResult)
        G = Graph.Graphs()
        G.plot_graph(Centre, Capacity, House, M)
        
    def random_values(self):
        Centre = []
        Capacity = []
        House = []
        for _ in range(5):
            Centre.append([random.random()*4 + 49.8, random.random()*8.5 + 14.8])
            Capacity.append(random.randint(10,25))
        for _ in range(sum(Capacity)):
            House.append([random.random()*4.2 + 50.05, random.random()*8.8 + 14.75])
        G = Algorithm.Hungarian_Algorithm(Centre, Capacity, House)
        M, Result, StringResult = G.main_algorithm(True)
        StrResult = 'Łączna odległość pomiędzy połączonymi centrami i domami wynosi ' + str(round(Result, 3)) + ' km'
        Box = ScrollMessageBox(1, "Wynik", StrResult + '\n' + StringResult, QMessageBox.Save | QMessageBox.Ok)
        ret = Box.exec_()
        if ret == QMessageBox.Save:
            with open('Results.txt', 'w') as f:
                f.write(StrResult + '\n' + StringResult)
        G = Graph.Graphs()
        G.plot_graph(Centre, Capacity, House, M)

    def values_generated_by_user(self):
        Centre, done1 = QInputDialog.getText(
            self, 'Współrzędne centrów', 'Podaj współrzędne centrów')
        Capacity, done2 = QInputDialog.getText(
            self, 'Limity centrów', 'Podaj limity centrów')
        House, done3 = QInputDialog.getText(
            self, 'Współrzędne domów', 'Podaj współrzędne domów')

        Centre = [float(i) for i in Centre.split(' ')]
        Capacity = [int(i) for i in Capacity.split(' ')]
        House = [float(i) for i in House.split(' ')]
        centre = []
        capacity = []
        house = []
        for j in range(0, len(Centre) - 1, 2):
            centre.append([Centre[j], Centre[j + 1]])
        for j in range(len(Capacity)):
            capacity.append(Capacity[j])
        for j in range(0, len(House) - 1, 2):
            house.append([House[j], House[j + 1]])

        G = Algorithm.Hungarian_Algorithm(centre, capacity, house)
        M, Result, StringResult = G.main_algorithm(True)
        StrResult = 'Łączna odległość pomiędzy połączonymi centrami i domami wynosi ' + str(round(Result, 3)) + ' km'
        Box = ScrollMessageBox(1, "Wynik", StrResult + '\n' + StringResult, QMessageBox.Save | QMessageBox.Ok)
        ret = Box.exec_()
        if ret == QMessageBox.Save:
            with open('Results.txt', 'w') as f:
                f.write(StrResult + '\n' + StringResult)
        G = Graph.Graphs()
        G.plot_graph(centre, capacity, house, M)
        
    def finish(self):
        self.close()
        sys.exit(app.exec_())

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    okno = Application()
    sys.exit(app.exec_())
