import unittest
from Source import Algorithm
import math

class HungarianAlgorithmTestCase(unittest.TestCase):
    def test_init_data_with_wrong_capacity(self):
        # [GIVEN]
        # Capacity that doesn't match centres
        centre = [[1,2], [3,-1], [-3,0]]
        capacity = [1, 1, 1, 1]
        house = [[0,-3], [-1,6], [2,3], [-5,-1]]
        
        # [WHEN]
        # Creating new class with wrong number of capacity
        # Algorithm.Hungarian_Algorithm(centre, capacity, house)
        
        # [THEN]
        # An error ocures
        self.assertRaises(Exception, Hungarian_Algorithm, centre, capacity, house)

    def test_init_data_with_wrong_no_of_houses(self):
        # [GIVEN]
        # Centres and capacities that don't match houses
        centre = [[1,2], [3,-1], [-3,0]]
        capacity = [1, 1, 1]
        house = [[0,-3], [-1,6], [2,3], [-5,-1]]
        
        # [WHEN]
        # Creating new class with wrong number of houses
        # Algorithm.Hungarian_Algorithm(centre, capacity, house)
        
        # [THEN]
        # An error ocures
        self.assertRaises(Exception, Hungarian_Algorithm, centre, capacity, house)
        
    def test_distance_function(self):
        # [GIVEN]
        # Object of type Hungarian_Algorithm
        centre = [[0,0], [3,-1], [-3,0]]
        capacity = [1, 1, 1]
        house = [[4,-3], [-1,6], [2,3]]
        A = Algorithm.Hungarian_Algorithm(centre, capacity, house)
        
        # [WHEN]
        # Calculating the distance between two points
        result = A.distance(centre[0], house[0])
        
        # [THEN]
        # Distance between two points is calculated
        expected_value = math.sqrt(4**2 + 3**2)
        msg = 'Wrong result!'
        self.assertEqual(result, expected_value, msg)

    #test dwa domy / dwa centra o tych samych współrzędnych 
    
    def test_two_centres_in_one_place(self):
        # [GIVEN]
        # Two centres with the same coordinates
        centre = [[0,0], [0,0]]
        capacity = [1, 1]
        house = [[4,-3], [-1,6]]
       
        
        # [WHEN]
        # Calculate Hungarian Algorithm 
        result = Algorithm.Hungarian_Algorithm(centre, capacity, house)
        
        # [THEN]
        # Build perfect matching with simple methods.
        # !!!
        expected_value =   0      #TO DO
        # !!!
        msg = 'Wrong result!'
        self.assertEqual(result, expected_value, msg)
    
    
    
    #test centrum i dom o tych samych współrzędnych

    def test_two_centres_in_one_place(self):
        # [GIVEN]
        # Two centres with the same coordinates
        centre = [[0,0], [-1,6]]
        capacity = [1, 1]
        house = [[4,-3], [0,0]]
       
        
        # [WHEN]
        # Calculate Hungarian Algorithm 
        result = Algorithm.Hungarian_Algorithm(centre, capacity, house)
        
        # [THEN]
        # Build perfect matching with simple methods.
        # !!!
        expected_value =  0       #TO DO
        # !!!
        msg = 'Wrong result!'
        self.assertEqual(result, expected_value, msg)

    #test calculate_adjency_matrix
    def test_calculate_adjency_matrix(self):
       

        # [GIVEN]
        # Correct example of class Hungarian_Algorithm
        for _ in range(3):
            Centre.append([random.randint(-10,10), random.randint(-10,10)])
            Capacities.append([random.randint(1,3)])
        for _ in range(sum(Capacities)):
            House.append([random.randint(-10,10), random.randint(-10,10)])
       
        
        # [WHEN]
        # Calculate adjency matrix in class Hungarian_Algorithm.
        result = Algorithm.Hungarian_Algorithm.calculate_adjency_matrix(centre, capacity, house)
        
        # [THEN]
        # Calculate adjency matrix outside class Hungarian_Algorithm.
        iterator = 0
        A = np.zeros((len(house), len(house))) #kolumny odpowiadaja za kolejne domy razy pojemnosc, wiersze za centra
        for i in range(len(centre)):
            for j in range(int(capacity[i])):
                for k in range(A.shape[1]):
                    A[iterator,k] = distance(centre[i], house[k]) 
                iterator += 1
        expected_value = A
        msg = 'Wrong result!'
        self.assertEqual(result, expected_value, msg)


    #test generate_bipartite_graph
    def test_generate_bipartite_graph(self):
       

        # [GIVEN]
        # Correct example of class Hungarian_Algorithm
        for _ in range(3):
            Centre.append([random.randint(-10,10), random.randint(-10,10)])
            Capacities.append([random.randint(1,3)])
        for _ in range(sum(Capacities)):
            House.append([random.randint(-10,10), random.randint(-10,10)])
       
        
        # [WHEN]
        # Create bipartite graph in class Hungarian_Algorithm.
        result = Algorithm.Hungarian_Algorithm.generate_bipartite_graph(centre, capacity, house)
        
        # [THEN]
        # Calculate bipartitie graph outside class Hungarian_Algorithm.
        iterator = 0
        NoOfHouses = int(len(house))
        NoOfCentres = int(len(centre))
        G = np.zeros((2 * NoOfHouses, 2 * NoOfHouses)) # najpierw centra razy pojemnosc, potem domy
        for i in range(NoOfCentres):
            for j in range(int(capacity[i])):
                for k in range(NoOfHouses):
                    G[iterator,k + NoOfHouses] = distance(centre[i], house[k])
                    G[k + NoOfHouses, iterator] = distance(centre[i], house[k])
                iterator += 1
        expected_value = G
        msg = 'Wrong result!'
        self.assertEqual(result, expected_value, msg)


    #test reverse path
    
    #test wektor potencjałów

    def test_init_potential(self):
        # [GIVEN]
        # Correct example of class Hungarian_Algorithm
        centre = [[0,0], [1,1]]
        capacity = [1, 1]
        house = [[-3, -4], [4, 5]]

        # [WHEN]
        # Calculate potentials in class Hungarian_Algorithm.
        result = Algorithm.Hungarian_Algorithm.init_potential(centre, capacity, house)

        # [THEN]
        # Calculate potentials. We know that centre 1 is closer house 1 and centre 2 is closer house 2.
        expected_value = [sqrt(3^2 + 4^2), sqrt((4-1)^2 + (5-1)^2), sqrt(3^2 + 4^2), sqrt((4-1)^2 + (5-1)^2)]
        msg = 'Wrong result!'
        self.assertEqual(result, expected_value, msg)

        
    #test działań na listach

    def test_intersection(self):
        # [GIVEN]
        # Two lists
        l1 = [1, 2, 3, -1, -3, 0]
        l2 = [0, -3, -1, 6, 2, 3, -5]
        
        # [WHEN]
        # Intersection of this two lists.
        result = Algorithm.Hungarian_Algorithm.intersection(l1, l2)
        
        # [THEN]
        # Check result.
        msg = 'Wrong result!'
        self.assertEqual(result, [2, 3, -1, -3, 0], msg)

    def test_subtraction(self):
        # [GIVEN]
        # Two lists
        l1 = [1, 2, 3, -1, -3, 0]
        l2 = [0, -3, -1, 6, 2, 3, -5]
        
        # [WHEN]
        # Intersection of this two lists.
        result = Algorithm.Hungarian_Algorithm.subtraction(l1, l2)
        
        # [THEN]
        # Check result.
        msg = 'Wrong result!'
        self.assertEqual(result, [1], msg)

    def test_subtraction(self):
        # [GIVEN]
        # Two lists
        l1 = [1, 2, 3, -1, -3, 0]
        
        # [WHEN]
        # Intersection of this two lists.
        result = Algorithm.Hungarian_Algorithm.subtraction(l1, -3)
        
        # [THEN]
        # Check result.
        msg = 'Wrong result!'
        self.assertEqual(result, [1, 2, 3, -1, 0], msg)

    #test BFS

    #test wszystkich śmiesznych małych funkcji update

    #test delta

    
    #test całości

    def test_hungarian_algorithm(self):
        # [GIVEN]
        # Centres, Capacities, Houses
        Centre = []
        Capacities = []
        House = []
        for _ in range(3):
            Centre.append([random.randint(-10,10), random.randint(-10,10)])
            Capacities.append([random.randint(1,3)])
        for _ in range(sum(Capacities)):
            House.append([random.randint(-10,10), random.randint(-10,10)])

        # [WHEN]
        # Starting main algorithm
        G = Algorithm.Hungarian_Algorithm(Centre, Capacities, House)
        Algorithm.Hungarian_Algorithm.main_algorithm(G)

        # [THEN]
        # Perfect matching is calculated 
        
    
if __name__ == '__main__':
    unittest.main()