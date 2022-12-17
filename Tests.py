import unittest
import Algorithm
import math
import random
import numpy as np

class HungarianAlgorithmTestCase(unittest.TestCase):
    
    def test_init_data_with_wrong_Capacity(self):
        # [GIVEN]
        # Capacity that doesn't match Centres
        Centre = [[1,2], [3,-1], [-3,0]]
        Capacity = [1, 1, 1, 1]
        House = [[0,-3], [-1,6], [2,3], [-5,-1]]
        
        # [WHEN]
        # Creating new class with wrong number of Capacity
        # Algorithm.Hungarian_Algorithm(Centre, Capacity, House)
        
        # [THEN]
        # An error ocures
        self.assertRaises(Exception, Algorithm.Hungarian_Algorithm, Centre, Capacity, House)


    def test_init_data_with_wrong_No_of_Houses(self):
        # [GIVEN]
        # Centres and Capacity that don't match Houses
        Centre = [[1,2], [3,-1], [-3,0]]
        Capacity = [1, 1, 1]
        House = [[0,-3], [-1,6], [2,3], [-5,-1]]
        
        # [WHEN]
        # Creating new class with wrong number of Houses
        # Algorithm.Hungarian_Algorithm(Centre, Capacity, House)
        
        # [THEN]
        # An error ocures
        self.assertRaises(Exception, Algorithm.Hungarian_Algorithm, Centre, Capacity, House)
        
        
    def test_distance_function(self):
        # [GIVEN]
        # Object of type Hungarian_Algorithm
        Centre = [[0,0], [3,-1], [-3,0]]
        Capacity = [1, 1, 1]
        House = [[4,-3], [-1,6], [2,3]]
        A = Algorithm.Hungarian_Algorithm(Centre, Capacity, House)
        
        # [WHEN]
        # Calculating the distance between two points
        result = A.distance(Centre[0], House[0])
        
        # [THEN]
        # Distance between two points is calculated
        expected_value = math.sqrt(4**2 + 3**2)
        msg = 'Wrong result!'
        self.assertEqual(result, expected_value, msg)


    def test_two_centres_in_one_place(self):
        # [GIVEN]
        # Two centres with the same coordinates
        centre = [[0,0], [0,0]]
        capacity = [1, 1]
        house = [[-4,-3], [-3,4]]
        
        # [WHEN]
        # Calculate Hungarian Algorithm 
        G = Algorithm.Hungarian_Algorithm(centre, capacity, house)
        _, Result = G.main_algorithm()
        # [THEN]
        # Calculate perfect matching.
        expected_value = 10.0
        msg = 'Wrong result!'
        self.assertEqual(Result, expected_value, msg)
    
    
    def test_init_potential(self):
        # [GIVEN]
        # Correct example of class Hungarian_Algorithm
        Centre = [[0,0], [1,1]]
        Capacity = [1, 1]
        House = [[-3, -4], [4, 5]]

        # [WHEN]
        # Calculate potentials in class Hungarian_Algorithm.
        G = Algorithm.Hungarian_Algorithm(Centre, Capacity, House)
        Result = G.init_potential()

        # [THEN]
        # Calculate potentials. We know that Centre 1 is closer House 1 and Centre 2 is closer House 2.
        expected_value = np.array([0., 0., math.sqrt(3**2 + 4**2), math.sqrt((4 - 1)**2 + (5 - 1)**2)])
        msg = 'Wrong result!'
        self.assertEqual(Result.tolist(), expected_value.tolist(), msg)


    def test_intersection(self):
        # [GIVEN]
        # Two lists
        l1 = [1, 2, 3, -1, -3, 0]
        l2 = [0, -3, -1, 6, 2, 3, -5]
        
        # [WHEN]
        # Intersection of this two lists.
        result = Algorithm.intersection(l1, l2)
        
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
        result = Algorithm.subtraction(l1, l2)
        
        # [THEN]
        # Check result.
        msg = 'Wrong result!'
        self.assertEqual(result, [1], msg)


    def test_subtraction2(self):
        # [GIVEN]
        # Two lists
        l1 = [1, 2, 3, -1, -3, 0]
        
        # [WHEN]
        # Intersection of this two lists.
        result = Algorithm.subtraction(l1, [-3])
        
        # [THEN]
        # Check result.
        msg = 'Wrong result!'
        self.assertEqual(result, [1, 2, 3, -1, 0], msg)
        

    def test_hungarian_algorithm_length_of_matching(self):
        # [GIVEN]
        # Centres, Capacity, Houses
        Centre = []
        Capacity = []
        House = []
        for _ in range(3):
            Centre.append([random.randint(-10,10), random.randint(-10,10)])
            Capacity.append(random.randint(1,3))
        for _ in range(sum(Capacity)):
            House.append([random.randint(-10,10), random.randint(-10,10)])

        # [WHEN]
        # Calculate perfect matching
        G = Algorithm.Hungarian_Algorithm(Centre, Capacity, House)
        M, _ = G.main_algorithm()

        # [THEN]
        # Perfect matching is calculated 
        expected_value = sum(Capacity)
        msg = 'Wrong result!'
        self.assertEqual(len(M), expected_value, msg)
        
        
    def test_hungarian_algorithm_matching(self):  
        # [GIVEN]
        # Correct example of class Hungarian_Algorithm
        Centre = []
        Centre.append([random.randint(-10, -5), random.randint(-10, -5)])
        Centre.append([random.randint(5, 10), random.randint(5, 10)])
        Capacity = [1, 1]
        House = []
        House.append([random.randint(-100, -50), random.randint(-100, -50)])
        House.append([random.randint(50, 100), random.randint(50, 100)])
    
        # [WHEN]
        # Calculate perfect matching
        G = Algorithm.Hungarian_Algorithm(Centre, Capacity, House)
        M, _ = G.main_algorithm()   
        
        # [THEN]
        # Perfect matching is calculated 
        expected_value = [[0,2],[1,3]]
        msg = 'Wrong result!'
        self.assertEqual(M, expected_value, msg)
        
        
    def test_hungarian_algorithm_result(self):
        # [GIVEN]
        # Correct example of class Hungarian_Algorithm
        Centre = [[0,0], [1,1]]
        Capacity = [1, 1]
        House = [[-3, -4], [4, 5]]
        
        # [WHEN]
        # Calculate distance between houses and centres in perfect matching.
        G = Algorithm.Hungarian_Algorithm(Centre, Capacity, House)
        _, Result = G.main_algorithm()

        # [THEN]
        # Calculate potentials. We know that Centre 1 is closer House 1 and Centre 2 is closer House 2.
        expected_value = math.sqrt((0+3)**2 + (0+4)**2) + math.sqrt((1-4)**2 + (1-5)**2)
        msg = 'Wrong result!'
        self.assertEqual(Result, expected_value, msg)
        
if __name__ == '__main__':
    unittest.main()