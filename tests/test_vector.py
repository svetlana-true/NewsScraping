import unittest
#from .context import src
from src.vector_db import VectorDB

class TestVectorDB(unittest.TestCase):
    urls = ["https://www.bbc.com/news/articles/czx415erwkwo", 
            "https://www.bbc.com/news/articles/ckgxk40ndk1o"]
    test_vector_db = VectorDB(urls)  # instantiate the Person Class
    article1 = '{"summary": "The IMF has downgraded its global growth forecast due to trade tariffs, predicting US growth at 1.8% and UK growth at 1.1% for the year. The uncertainty from tariffs is expected to slow down global economic activity significantly, with a 40% chance of a US recession this year.", "topics": ["IMF", "growth", "tariffs", "economy"]}'
    article2 = '{"summary": "The article discusses the upcoming papal conclave to elect the next pope, highlighting key candidates and the implications of their potential election for the Catholic Church, particularly in terms of geographical representation and ideological diversity.", "topics": ["Pope", "Election", "Candidates", "Catholicism"]}'
    
    def setUp(self):
        self.test_vector_db.prepare_data(self.article1)
        self.test_vector_db.prepare_data(self.article2)
        self.test_vector_db.createFaissIndex()
        self.test_vector_db.createVectorStore()
    
    def test_search(self):
        query = "weather"
        distance, url = self.test_vector_db.search_in_db(query)

        decimalPlace = 2
        # error message in case if test case got failed
        message = "first and second are not almost equal."
        self.assertAlmostEqual(distance, 26.348576, decimalPlace, message)
        self.assertEqual(url, self.urls[0])

        score = self.test_vector_db.simularity_search(query)
        delta = 500
        self.assertAlmostEqual(score[0], 8220.861, None, message, delta)

if __name__ == "__main__":
    unittest.main()
