import math
import numpy as np

class Data:

    def __init__(self, centre, capacity, house):
        """[Constructor]

        Args:
            centre ([list[list[int]]]): [Coordinates of all distribution centres. For example: [[0,1], [-3,2], [-1,5]] ]
            capacity ([list[int]]): [Capacity of every distribution center. For example: [1,1,2] ]
            house ([list[list[int]]]): [Coordinates of all houses. For example: [[-1,2], [3,1], [-4,2], [-1,-2]] ]
        """
        # TODO Sprawdzenie poprawności danych wejściowych
        self.centre = centre # postaci: [[0,1], [-3,2], [-1,5]]
        self.capacity = capacity # postaci [1,1,2]
        self.house = house # postaci [[-1,2], [3,1], [-4,2], [-1,-2]] 
        
    def __init__(self, path):
        """[Function which loads data about centres and houses from file.]

        Args:
            path ([string]): [File path where are saved data about some distribution centres and houses.]
        """
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

        self.centre = centre
        self.capacity = capacity
        self.house = house

    def distance(self, centre_iterator: int, house_iterator: int):
        """[Function which calculate distance from distribution centre to house.]

        Args:
            centre_iterator (int): [Distribution centre number.]
            house_iterator (int): [House number.]

        Returns:
            [float]: [Distance from distribution centre to house.]
        """
        return math.sqrt((self.centre[centre_iterator][0]-self.house[house_iterator][0])**2+(self.centre[centre_iterator][1]-self.house[house_iterator][1])**2)

    def calculate_adjency_matrix(self):
        """[Function which makes matrix of distances from every distribution centre to every house.]

        Returns:
            [list[list[float]]]: [Matrix of distances from every distribution centre to every house.]
        """
        A = np.zeros((len(self.centre), len(self.house))) #kolumny odpowiadaja za kolejne domy, wiersze za centra
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                A[i,j] = self.distance(i,j)
        return A

    def init_potential(self):
        """[Function which makes vector of potentials of every distribution centre and house.]

        Returns:
            [list[float]]: [Vector of potentials - first potienals of every distribution centre then every house.]
        """
        A = self.calculate_adjency_matrix()
        NoOfHouses = int(sum(self.capacity))
        y = np.zeros((NoOfHouses * 2)) # najpierw centra * pojemnosc, potem domy
        column = 0
        for i in range(NoOfHouses, len(y), 1):
            minimum = A[0][column]
            for row in range(A.shape[0]):
                if A[row][column] < minimum:
                    minimum = A[row][column]
            y[i] = minimum
            column += 1
        return y
    
    def generate_bipartite_graph(self):
        NoOfHouses = int(len(self.house))
        NoOfCentres = int(len(self.centre))
        G = np.zeros((NoOfCentres + NoOfHouses, NoOfCentres + NoOfHouses)) # najpierw centra, potem domy
        for i in range(NoOfCentres):
            for j in range(NoOfHouses):
                G[i,j + NoOfCentres] = self.distance(i,j)
                G[j + NoOfCentres, i] = self.distance(i,j)
        return G
    
    def intersection(list1, list2):
        return [value for value in list1 if (value in list2)]

    def subtraction(list1,list2):
        return[value for value in list1 if (value not in list2)]

    def delete_vertex_from_R(L,x):
        for i in range(len(L)):
            if L[i]==x:
                return L[:i]+L[i+1:]
        return L
    
    def update_R(self, R, M, Centre: bool):
        if Centre:
            i = 0
        else:
            i = 1
        for pairs in M:
            if pairs[i] in R:
                R = self.delete_vertex_from_R(R,pairs[0])
            if R == None:
                return []
        return R
    
    def hungarian_algorithm(self):
        M = []
        NoOfHouses = int(len(self.house))
        NoOfCentres = int(len(self.centre))
        G_y = np.zeros((NoOfCentres + NoOfHouses, NoOfCentres + NoOfHouses))
        R_C = list(range(NoOfCentres)) #wierzcholki niepokryteprzez M
        R_H = list(range(NoOfHouses)) #wierzcholki niepokryteprzez M
        Z = list(range(NoOfHouses))
        while len(M) < (NoOfHouses):
            
            if len(self.intersection(R_H, Z))!=0:
                # TODO
                #odwróć skierowanie ścieżki w Gy wychodzącej z RS i wchodzącej do RD .
                
                