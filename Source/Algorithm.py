import math
import numpy as np

class Data:

    def __init__(self, centre, capacity, house):
        # TODO Sprawdzenie poprawności danych wejściowych
        self.centre = centre # postaci: [[0,1], [-3,2], [-1,5]]
        self.capacity = capacity # postaci [1,1,2]
        self.house = house # postaci [[-1,2], [3,1], [-4,2], [-1,-2]] 

    def load_from_file(path):
        temp = []
        centre = []
        capacity = []
        house = []
        
        with open(path) as file:
            lines = file.readlines()
        for line in lines:
            temp.append(list(map(float, line
                .replace('\t', ' ')
                .replace('\r', '')
                .replace('\n', '')
                .split(' '))))

        for j in range(0, len(temp[0])-1, 2):
            centre.append([temp[0][j],temp[0][j+1]])
        for j in range(len(temp[1])):
            capacity.append(temp[1][j])
        for j in range(0, len(temp[2])-1, 2):
            house.append([temp[2][j],temp[2][j+1]])

        return centre, capacity, house

    def distance(self, centre_iterator: int, house_iterator: int):
        return math.sqrt((self.centre[centre_iterator][0]-self.house[house_iterator][0])**2+(self.centre[centre_iterator][1]-self.house[house_iterator][1])**2)

    def calculate_adjency_matrix(self):
        A = np.zeros((len(self.centre), len(self.house))) #kolumny odpowiadaja za kolejne domy, wiersze za centra
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                A[i,j] = self.distance(i,j)
        return(A)

    def init_potential(self):
        A = self.calculate_adjency_matrix()
        NoOfHouses = sum(self.capacity)
        y = np.zeros((NoOfHouses * 2)) # najpierw centra * pojemnosc, potem domy
        column = 0
        for i in range(NoOfHouses, len(y), 1):
            minimum = A[0][column]
            for row in range(A.shape[0]):
                if A[row][column] < minimum:
                    minimum = A[row][column]
            y[i] = minimum
            column += 1
        return[y]


