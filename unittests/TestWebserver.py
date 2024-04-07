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
        ref_file = open('./unittests/refs/global_mean.json', 'r')
        ref_data = json.load(ref_file)
        ref_file.close()
        self.assertEqual(DeepDiff(data, ref_data, math_epsilon=0.01), {})

    def test_states_mean(self):
        job = self.data_ingestor.create_states_mean_job('Percent of adults aged 18 years and older who have obesity')
        data = job()
        data = json.loads(data)
        ref_file = open('./unittests/refs/states_mean.json', 'r')
        ref_data = json.load(ref_file)
        ref_file.close()
        self.assertEqual(DeepDiff(data, ref_data, math_epsilon=0.01), {})

    def test_state_mean(self):
        job = self.data_ingestor.create_state_mean_job('Percent of adults aged 18 years and older who have obesity', 'North Carolina')
        data = job()
        data = json.loads(data)
        ref_file = open('./unittests/refs/state_mean.json', 'r')
        ref_data = json.load(ref_file)
        ref_file.close()
        self.assertEqual(DeepDiff(data, ref_data, math_epsilon=0.01), {})

    def test_best5(self):
        job = self.data_ingestor.create_best5_job('Percent of adults aged 18 years and older who have obesity')
        data = job()
        data = json.loads(data)
        ref_file = open('./unittests/refs/best5.json', 'r')
        ref_data = json.load(ref_file)
        ref_file.close()
        self.assertEqual(DeepDiff(data, ref_data, math_epsilon=0.01), {})

    def test_worst5(self):
        job = self.data_ingestor.create_worst5_job('Percent of adults aged 18 years and older who have obesity')
        data = job()
        data = json.loads(data)
        ref_file = open('./unittests/refs/worst5.json', 'r')
        ref_data = json.load(ref_file)
        ref_file.close()
        self.assertEqual(DeepDiff(data, ref_data, math_epsilon=0.01), {})

    def test_diff_from_mean(self):
        job = self.data_ingestor.create_diff_from_mean_job('Percent of adults aged 18 years and older who have obesity')
        data = job()
        data = json.loads(data)
        ref_file = open('./unittests/refs/diff_from_mean.json', 'r')
        ref_data = json.load(ref_file)
        ref_file.close()
        self.assertEqual(DeepDiff(data, ref_data, math_epsilon=0.01), {})

    def test_state_diff_from_mean(self):
        job = self.data_ingestor.create_state_diff_from_mean_job('Percent of adults aged 18 years and older who have obesity', 'North Carolina')
        data = job()
        data = json.loads(data)
        ref_file = open('./unittests/refs/state_diff_from_mean.json', 'r')
        ref_data = json.load(ref_file)
        ref_file.close()
        self.assertEqual(DeepDiff(data, ref_data, math_epsilon=0.01), {})

    def test_mean_by_category(self):
        job = self.data_ingestor.create_mean_by_category_job('Percent of adults aged 18 years and older who have obesity')
        data = job()
        data = json.loads(data)
        ref_file = open('./unittests/refs/mean_by_category.json', 'r')
        ref_data = json.load(ref_file)
        ref_file.close()
        self.assertEqual(DeepDiff(data, ref_data, math_epsilon=0.01), {})

    def test_state_mean_by_category(self):
        job = self.data_ingestor.create_state_mean_by_category_job('Percent of adults aged 18 years and older who have obesity', 'North Carolina')
        data = job()
        data = json.loads(data)
        ref_file = open('./unittests/refs/state_mean_by_category.json', 'r')
        ref_data = json.load(ref_file)
        ref_file.close()
        self.assertEqual(DeepDiff(data, ref_data, math_epsilon=0.01), {})