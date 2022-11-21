import unittest
from ..Source.Algorithm import *

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

    #test za dużo centrów w porównaniu z capacity

    #test centra*pojemność =/= liczba domów
    
    #test dwa domy / dwa centra o tych samych współrzędnych
    
    #test centrum i dom o tych samych współrzędnych

    #test calculate_adjency_matrix

    #test generate_bipartite_graph

    #test reverse path
    
    #test wektor potencjałów

    #test działań na listach

    #test BFS

    #test wszystkich śmiesznych małych funkcji update

    #test delta

    #test całości
        
    
if __name__ == '__main__':
    unittest.main()