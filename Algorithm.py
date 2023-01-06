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
        self.check_init_data(centre, capacity, house)

        self.centre = centre # postaci: [[0,1], [-3,2], [-1,5]]
        self.capacity = capacity # postaci [1,1,2]
        self.house = house # postaci [[-1,2], [3,1], [-4,2], [-1,-2]] 
        
    def check_init_data(self, centre, capacity, house):
        """[Function which validates input data.]

        Args:
            centre ([list[list[int]]]): [Coordinates of all distribution centres. For example: [[0,1], [-3,2], [-1,5]] ]
            capacity ([list[int]]): [Capacity of every distribution center. For example: [1,1,2] ]
            house ([list[list[int]]]): [Coordinates of all houses. For example: [[-1,2], [3,1], [-4,2], [-1,-2]] ]

        Raises:
            [Exception if data doesn't match the pattern.]
        """
        text = "Inappropriate type of an object: "
        if not isinstance(centre, list):
            raise Exception(text + 'centre.')
        if not isinstance(capacity, list):
            raise Exception(text + 'capacity.')
        if not isinstance(house, list):
            raise Exception(text + 'house.')
        
        for i in range(len(centre)):
            if (not isinstance(centre[i], list)) or (not (isinstance(centre[i][0], float) or (isinstance(centre[i][0], int)))) or (not (isinstance(centre[i][1], float) or (isinstance(centre[i][1], int)))):
                raise Exception(text + 'centre.')
        for i in range(len(house)):
            if (not isinstance(house[i], list)) or (not (isinstance(house[i][0], float) or (isinstance(house[i][0], int)))) or (not (isinstance(house[i][1], float) or (isinstance(house[i][1], int)))):
                raise Exception(text + 'house.')
            
        if int(sum(capacity)) != len(house):
            raise Exception("No. of houses doesn't match the capacity.")
        if len(capacity) != len(centre):
            raise Exception("No. of centres doesn't match the capacity.")

    def distance(self, centre: list, house: list):
        """[Function which calculates distance from distribution centre to house.]

        Args:
            centre_iterator (list): [Distribution centre coordinates]
            house_iterator (list): [House coordinates]

        Returns:
            [float]: [Distance from distribution centre to house.]
        """
        return round(math.sqrt((centre[0] - house[0]) ** 2 + (centre[1] - house[1]) ** 2), 2)

    def calculate_adjency_matrix(self):
        """[Function which makes matrix of distances from every distribution centre to every house.]

        Returns:
            [list[list[float]]]: [Matrix of distances from every distribution centre to every house.]
        """
        iterator = 0
        A = np.zeros((len(self.house), len(self.house))) #kolumny odpowiadaja za kolejne centra razy pojemnosc, wiersze za domy
        for i in range(len(self.centre)):
            for j in range(int(self.capacity[i])):
                for k in range(A.shape[1]):
                    A[iterator,k] = self.distance(self.centre[i], self.house[k]) 
                iterator += 1
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
        iterator = 0
        NoOfHouses = int(len(self.house))
        NoOfCentres = int(len(self.centre))
        G = np.zeros((2 * NoOfHouses, 2 * NoOfHouses)) # najpierw centra razy pojemnosc, potem domy
        for i in range(NoOfCentres):
            for j in range(int(self.capacity[i])):
                for k in range(NoOfHouses):
                    G[iterator,k + NoOfHouses] = self.distance(self.centre[i], self.house[k])
                    G[k + NoOfHouses, iterator] = self.distance(self.centre[i], self.house[k])
                iterator += 1
        return G
    
    def update_R(self, R, M, IsCentre: bool):
        """[Function deletes from list R nodes which already are in perfect matching M.]

        Returns:
            [list]: [Updated list R.]
        """
        if IsCentre:
            i = 0
        else:
            i = 1
        for pairs in M:
            if pairs[i] in R:
                R = delete_element_from_list(R, pairs[i])
            if R == None:
                return []
        return R
    
    def reverse_path(self, G_y, R_C, R_H):
        """[Function creates bipartite, oriented subgraph which contains all tight edges.]

        Returns:
            [matrix]: [Oriented subrgraph which contains all tight edges.]
        """
        path = BFS(G_y,R_C,R_H) # zwraca sciezke, na parzystych miejscach beda centra, nieparzyste - domy
        for i in range(len(path) - 1):
            temp = G_y[path[i]][path[i + 1]]
            G_y[path[i]][path[i + 1]] = 0
            G_y[path[i + 1]][path[i]] = round(temp, 2)
        return G_y

    def update_M(self, M, G_y):
        """[Function adds edges from graph G_y to perfect matching M]

        Returns:
            [list]: [List of pairs - first coordinate centre number, second coordinate house number]
        """
        M = []
        NoOfHouses = int(len(self.house))
        NoOfCentres = int(len(self.house))
        for i in range(NoOfCentres):
            for j in range(NoOfCentres, NoOfCentres + NoOfHouses):
                if G_y[j][i] > 0: # [j][i] poniewaz interesuja nas tylko krawedzie z klasy H do klasy C
                    M.append([i,j]) # M jako pary (centrum, dom)              
        return M
    
    def update_Z(self, Z, G_y, R_C, R_H):
        """[Function updates set Z at vertices from updated graph G_y which are joined with graph R_C]

        Returns:
            [list]: [List of vertices]
        """
        Z = R_C.copy()
        for vertex in R_C:
            temp = BFS_vertex(G_y,vertex) 
            for w in temp:
                if w not in Z:
                    Z.append(w)
        return Z
    
    def update_Gy(self, G, y, G_y):
        """[Function updates graph G_y at tight edges]

        Returns:
            [matrix]: [Matrix distances between two vertices]
        """
        Centre_Capacity_iterator = list(range(len(self.house))) #centra razy pojemnosc
        House_iterator = list(range(len(self.house)))
        NoOfHouses = int(len(self.house))
        for i in Centre_Capacity_iterator:
            for j in House_iterator:
                if round(y[i]+y[j + NoOfHouses],2) == round(G[i][j + NoOfHouses], 2):
                    if round(G_y[i][j + NoOfHouses], 2) != round(G[i][j + NoOfHouses], 2) and round(G_y[j + NoOfHouses][i], 2) != round(G[i][j + NoOfHouses], 2):
                        G_y[i][j + NoOfHouses] = round(G[i][j + NoOfHouses], 2)
                else:
                    if round(G_y[i][j + NoOfHouses], 2) == round(G[i][j + NoOfHouses], 2) or round(G_y[j + NoOfHouses][i], 2) == round(G[i][j + NoOfHouses], 2):
                        G_y[i][j + NoOfHouses] = 0
                        G_y[j + NoOfHouses][i] = 0    
        return G_y    
    
    def calculate_delta(self, Z, Y, Centre, Houses):
        """[summary]

        Returns:
            [type]: [description]
        """
        G = self.generate_bipartite_graph()
        Z_intersection_C = intersection(Z, Centre)
        H_minus_Z = subtraction(Houses, Z)
        delta = G[Z_intersection_C[0]][H_minus_Z[0]] - Y[Z_intersection_C[0]] - Y[H_minus_Z[0]]
        for i in Z_intersection_C:
            for j in H_minus_Z:
                if (G[i][j] - Y[i] - Y[j]) < delta:
                    delta = G[i][j] - Y[i] - Y[j]
        return round(delta, 2)
    
    def print_info(self, M):
        StringResult =''
        Centre_Indexes = []
        Temporary_List = [[] for _ in range(len(self.centre))]
        NoOfHouses = int(len(self.house))
        for i in range(len(self.centre)):
            for _ in range(int(self.capacity[i])):
                Centre_Indexes.append(i)
        for i in range(len(M)):
            Temporary_List[Centre_Indexes[M[i][0]]].append(M[i][1] - NoOfHouses + 1)
        print('Centre ---> House')
        StringResult += 'Centrum ---> Dom\n'
        for i in range(len(Temporary_List)):
            print('  ', i+1, '  --->', *Temporary_List[i])
            StringResult += '  ' + str(i+1) + '  --->' + str(Temporary_List[i]) + '\n'
        return StringResult
            
    def calculate_result(self, M):
        Result = 0
        Centre_Indexes = []
        NoOfHouses = int(len(self.house))
        for i in range(len(self.centre)):
            for _ in range(int(self.capacity[i])):
                Centre_Indexes.append(i)
        for i in range(len(M)):

            Result += self.distance(self.centre[Centre_Indexes[int(M[i][0])]], self.house[int(M[i][1]) - NoOfHouses])
        return Result
        
    def main_algorithm(self, print_info = False):
        """[Main Hungarian algorithm]

        Returns:
            [list]: [Perfect matching in graph containing distribution centres and houses.]
        """
        M = []
        StringResult = ''
        G = self.generate_bipartite_graph()
        NoOfHouses = int(len(self.house))
        NoOfCentres = int(len(self.centre))
        Y = self.init_potential()
        G_y = np.zeros(((2 * NoOfHouses), (2 * NoOfHouses)))
        G_y = self.update_Gy(G, Y, G_y)
        R_C = list(range(NoOfHouses)) # wierzcholki niepokryte przez M
        R_H = list(range(NoOfHouses,2*len(self.house))) # wierzcholki niepokryte przez M
        Z = []
        Z = self.update_Z(Z, G_y, R_C, R_H)
        Centre_iterator = list(range(len(self.house))) # indeksy centrow
        House_iterator = list(range(NoOfHouses,2*len(self.house))) # indeksy domow

        while len(M) < NoOfHouses:
            if len(intersection(R_H, Z)) != 0:
                G_y = self.reverse_path(G_y, R_C, R_H)
            else:
                delta = self.calculate_delta(Z, Y, Centre_iterator, House_iterator)
                Z_Intersection_C = intersection(Z, Centre_iterator)
                Z_Intersection_H = intersection(Z, House_iterator)
                for i in Z_Intersection_C: # dodawanie odejmowanie delty
                    Y[i] += delta
                for j in Z_Intersection_H:
                    Y[j] -= delta
            
                G_y = self.update_Gy(G, Y, G_y) # dodaje ciasne i usuwam nieciasne krawedzie z Gy
            M = self.update_M(M, G_y)
            R_C = self.update_R(R_C, M, True)
            R_H = self.update_R(R_H, M, False)
            Z = self.update_Z(Z, G_y, R_C, R_H)
        if print_info:
            StringResult = self.print_info(M)
        Result = self.calculate_result(M)
        return M, Result, StringResult
                
                
def intersection(list1, list2):
    """[Function makes intersection of two any lists. It returns elements from first list list which are on second list, too.]

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
    n = len(G)
    for v in A:
        colors = [0]*n
        colors[v] = 1
        parent = [None]*n
        dist = [-1]*n
        dist[v] = 0
        Q = [v]
        while len(Q) != 0:
            u = Q[0]
            Q.pop(0)
            neighbours = []
            for i in range(n):
                if G[u][i] != 0:
                    neighbours.append(i)
            for w in neighbours:
                if colors[w] == 0:
                    colors[w] = 1
                    parent[w] = u
                    if w in B:
                        temp = w
                        path = [temp]
                        while parent[temp] != None:
                            path.append(parent[temp])
                            temp = parent[temp]
                        return path[::-1]
                    dist[w ] =dist[u]+1
                    Q.append(w)
            colors[u] = 2
    return []


def BFS_vertex(G, v):
    """_summary_

    Args:
        G (_type_): _description_
        v (_type_): _description_
    """
    '''v wierzcholek z G
    zwraca wierzcholki do ktorych mozna w G dojsc z v''' 
    n = len(G)
    colors = [0]*n
    colors[v] = 1
    parent = [None]*n
    dist = [-1]*n
    dist[v] = 0
    Q = [v]
    while len(Q) != 0:
        u = Q[0]
        Q.pop(0)
        neighbours = []
        for i in range(n):
            if G[u][i] != 0:
                neighbours.append(i)
        for w in neighbours:
            if colors[w] == 0:
                colors[w] = 1
                parent[w] = u
                dist[w] = dist[u] + 1
                Q.append(w)
        colors[u] = 2
    results = []
    for i in range(n):
        if dist[i] > -1:
            results.append(i)
    return results

def load_from_file(path):
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

    return centre, capacity, house

