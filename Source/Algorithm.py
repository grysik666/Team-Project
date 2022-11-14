import math
import numpy as np

class Hungarian_Algorithm:

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

        for j in range(0, len(temp[0]) - 1, 2):
            centre.append([temp[0][j],temp[0][j+1]])
        for j in range(len(temp[1])):
            capacity.append(temp[1][j])
        for j in range(0, len(temp[2]) - 1, 2):
            house.append([temp[2][j],temp[2][j+1]])

        self.centre = centre
        self.capacity = capacity
        self.house = house

    def distance(self, centre_iterator: int, house_iterator: int):
        """[Function which calculates distance from distribution centre to house.]

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
            [list[float]]: [Vector of potentials - first potentials of every distribution centre then every house.]
        """
        A = self.calculate_adjency_matrix()
        NoOfHouses = int(sum(self.capacity))
        Y = np.zeros((NoOfHouses * 2)) # najpierw centra * pojemnosc, potem domy
        column = 0
        for i in range(NoOfHouses, len(Y), 1):
            minimum = A[0][column]
            for row in range(A.shape[0]):
                if A[row][column] < minimum:
                    minimum = A[row][column]
            Y[i] = minimum
            column += 1
        return Y
    
    def generate_bipartite_graph(self):
         """[Function generates bipartite graph which first part are centres, second houses and save it as matrix of edge weights.]

        Returns:
            [matrix[float]]: [Matrix of distances between centres and houses.]
        """
        NoOfHouses = int(len(self.house))
        NoOfCentres = int(len(self.centre))
        G = np.zeros((NoOfCentres + NoOfHouses, NoOfCentres + NoOfHouses)) # najpierw centra, potem domy
        for i in range(NoOfCentres):
            for j in range(NoOfHouses):
                G[i,j + NoOfCentres] = self.distance(i,j)
                G[j + NoOfCentres, i] = self.distance(i,j)
        return G
    
    def update_R(self, R, M, IsCentre: bool):
         """[Function deletes from list R nodes which already are in perfect matching M.]

        Returns:
            [list]: [Updated list R.]
        """
        # copy()
        if IsCentre:
            i = 0
        else:
            i = 1
        for pairs in M:
            if pairs[i] in R:
                R = delete_element_from_list(R, pairs[0])
            if R == None:
                return []
        return R
    
    def reverse_path(self, G_y, R_C, R_H):
         """[Function creates bipartite, oriented subgraph which contains all tight edges.]

        Returns:
            [matrix]: [Oriented subrgraph which contains all tight edges.]
        """
        # copy()
        NoOfCentres = int(len(self.centre))        
        path = BFS(G_y,R_C,R_H) # parzyste to centra
        
        for i in range(len(path) - 1):
            temp = G_y[path[i]][path[i + 1]]
            G_y[path[i]][path[i + 1] + NoOfCentres] = 0
            G_y[path[i + 1] + NoOfCentres][path[i]] = temp
        return G_y

    def update_M(self, M, G_y):
         """[summary]

        Returns:
            [type]: [description]
        """
        # TODO
        return M
    
    def update_Z(self, Z, G_y, R_C, R_H):
         """[summary]

        Returns:
            [type]: [description]
        """
        # TODO
        return Z
    
    def update_Gy(self, G_y, G, y):
         """[summary]

        Returns:
            [type]: [description]
        """
        # TODO
        return G_y    
    
    def calculate_delta(self, delta, Z, y):
         """[summary]

        Returns:
            [type]: [description]
        """
        # TODO
        return delta
        
    def main_algorithm(self):
         """[Main Hungarian algorithm]

        Returns:
            [list]: [Perfect matching in graph containing distribution centres and houses.]
        """
        M = []
        G = self.generate_bipartite_graph()
        NoOfHouses = int(len(self.house))
        NoOfCentres = int(len(self.centre))
        Y = self.init_potential()
        G_y = np.zeros((NoOfCentres + NoOfHouses, NoOfCentres + NoOfHouses))
        R_C = list(range(NoOfCentres)) # wierzcholki niepokryte przez M
        R_H = list(range(NoOfHouses)) # wierzcholki niepokryte przez M
        Z = list(range(NoOfHouses))
        Centre_iterator = list(range(len(self.centre))) # indeksy studni
        House_iterator = list(range(len(self.house))) # indeksy domow
        
        
        while len(M) < (NoOfHouses):
            
            if len(intersection(R_H, Z)) != 0:
                G_y = self.reverse_path(G_y, R_C, R_H)
            else:
                delta = self.calculate_delta
                Z_Intersection_C = intersection(Z, Centre_iterator)
                Z_Intersection_H = intersection(Z, range(House_iterator))

                for i in Z_Intersection_C: # dodawanie odejmowanie delty
                    Y[i] += delta
                for j in Z_Intersection_H:
                    Y[j] -= delta
            
                G_y = self.update_Gy(G, Y, G_y) # dodaje ciasne i usuwam nieciasne krawedzie z Gy

                M = self.update_M(G_y)
                R_C = self.update_R(R_C, M, True)
                R_H = self.update_R(R_C, M, False)
                Z = self.update_Z(Z, G_y, R_C, R_H)
                
        return M
                
                
def intersection(list1, list2):
     """[Function makes intersection of two any lists. I returns elements from first list list which are on second list, too.]

        Returns:
            [list]: [Intersection of two lists.]
        """
    return [value for value in list1 if (value in list2)]

def subtraction(list1, list2):
     """[Function makes substraction of two any lists. It returns elements from first list which are not on second list.]

        Returns:
            [list]: [Substraction of two lists.]
        """
    return[value for value in list1 if (value not in list2)]

def delete_element_from_list(L, x):
     """[Function deletes particular element from list.]

        Returns:
            [list]: [List without particular element.]
        """
    for i in range(len(L)):
        if L[i] == x:
            return L[:i] + L[i + 1:]
    return L

def BFS(G, A, B):
     """[summary]

        Returns:
            [type]: [description]
        """
    '''A,B podzbiory wierzcholkow G
    zwraca sciezke z wierzcholka z A  do wierzcholka z B o ile taka istnieje''' 
    # TODO
    return []

