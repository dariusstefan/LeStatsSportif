import unittest
import json
import os
import sys
from deepdiff import DeepDiff

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir, '..', 'app'))
from data_ingestor import DataIngestor

class TestWebserver(unittest.TestCase):
    def setUp(self):
        self.data_ingestor = DataIngestor('./unittests/unittesting.csv')

    def test_global_mean(self):
        job = self.data_ingestor.create_global_mean_job('Percent of adults aged 18 years and older who have obesity')
        data = job()
        data = json.loads(data)
        self.assertEqual(DeepDiff(data['global_mean'], 32.3, math_epsilon=0.01), {})

    def test_states_mean(self):
        job = self.data_ingestor.create_states_mean_job('Percent of adults aged 18 years and older who have obesity')
        data = job()
        self.assertEqual(data, '{"Arizona":14.6,"Rhode Island":24.1,"North Carolina":24.1,"Utah":24.9,"Montana":26.2,"New Mexico":27.7,"Ohio":29.4,"New Hampshire":29.5,"Missouri":31.0,"Pennsylvania":32.7,"Indiana":33.1,"Wyoming":33.9,"Mississippi":33.9,"California":36.7,"Arkansas":38.6,"Iowa":41.0,"Tennessee":41.6,"Nebraska":44.3}')

    def test_state_mean(self):
        job = self.data_ingestor.create_state_mean_job('Percent of adults aged 18 years and older who have obesity', 'North Carolina')
        data = job()
        data = json.loads(data)
        self.assertEqual(DeepDiff(data['North Carolina'], 24.1, math_epsilon=0.01), {})

    def test_best5(self):
        job = self.data_ingestor.create_best5_job('Percent of adults aged 18 years and older who have obesity')
        data = job()
        self.assertEqual(data, '{"Arizona":14.6,"Rhode Island":24.1,"North Carolina":24.1,"Utah":24.9,"Montana":26.2}')

    def test_worst5(self):
        job = self.data_ingestor.create_worst5_job('Percent of adults aged 18 years and older who have obesity')
        data = job()
        self.assertEqual(data, '{"Nebraska":44.3,"Tennessee":41.6,"Iowa":41.0,"Arkansas":38.6,"California":36.7}')

    def test_diff_from_mean(self):
        job = self.data_ingestor.create_diff_from_mean_job('Percent of adults aged 18 years and older who have obesity')
        data = job()
        self.assertEqual(data, '{"Ohio":2.9095238095,"New Mexico":4.6095238095,"Tennessee":-9.2904761905,"Nebraska":-11.9904761905,"Pennsylvania":-0.3904761905,"Iowa":-8.6904761905,"New Hampshire":2.8095238095,"Missouri":1.3095238095,"Rhode Island":8.2095238095,"Indiana":-0.7904761905,"Wyoming":-1.5904761905,"Arkansas":-6.2904761905,"Utah":7.4095238095,"California":-4.3904761905,"Arizona":17.7095238095,"Montana":6.1095238095,"North Carolina":8.2095238095,"Mississippi":-1.5904761905}')

    def test_state_diff_from_mean(self):
        job = self.data_ingestor.create_state_diff_from_mean_job('Percent of adults aged 18 years and older who have obesity', 'North Carolina')
        data = job()
        data = json.loads(data)
        self.assertEqual(DeepDiff(data['North Carolina'], 8.2, math_epsilon=0.01), {})

    def test_mean_by_category(self):
        job = self.data_ingestor.create_mean_by_category_job('Percent of adults aged 18 years and older who have obesity')
        data = job()
        self.assertEqual(data, '{"Income 1":32.7,"Income 2":33.1,"Income 3":32.3,"Income 4":32.9}')

    def test_state_mean_by_category(self):
        job = self.data_ingestor.create_state_mean_by_category_job('Percent of adults aged 18 years and older who have obesity', 'North Carolina')
        data = job()
        self.assertEqual(data, '{"Income 1":24.1,"Income 2":24.1,"Income 3":24.1,"Income 4":24.1}')