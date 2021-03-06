from unittest import TestCase
from unittest.mock import patch, MagicMock

from io import StringIO

from json import loads

import pandas as pd

from ..parsers.parser import DatasetParser, ParsedDataset
from ..parsers.exceptions import (
    InvalidFormat,
    InvalidFile,
    InvalidFeature
)


class TestDatasetParser(TestCase):
    def setUp(self):
        self.test_df = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['New York', 'Tokyo', 'Coro'],
            'population(m)': [8.4, 9.3, 0.2],
            'large_city': [True, True, False]
        })

        self.test_df_csv_buffer = StringIO()
        self.test_df.to_csv(self.test_df_csv_buffer, index=False)
        self.test_df_csv_buffer.seek(0)

        self.parser = DatasetParser(self.test_df_csv_buffer,
                                    file_format='csv',
                                    to_format='json',
                                    label='large_city',
                                    problem_type='classification')

    def test_parse_from_file(self):
        self.dataset = self.parser.parse()
        
        self.assertEqual(self.dataset.get_data(),
                         loads(self.test_df.to_json(orient='records')))

    def test_parse_valid_format(self):
        self.assertEqual(self.parser.file_formats_are_valid(), True)

    def test_read_valid_file_and_format(self):
        df = self.parser.read()
        self.assertEqual(len(df), 3)

    def test_read_unsupported_format(self):
        self.parser.file_format = 'psd'

        with self.assertRaises(InvalidFormat):
            self.parser.file_formats_are_valid()

    def test_read_valid_file_wrong_format(self):
        self.parser.file_format = 'json'

        with self.assertRaises(InvalidFile):
            self.parser.parse()
    
    def test_write_invalid_format(self):
        self.parser.to_format = 'png'

        with self.assertRaises(InvalidFormat):
            self.parser.write(self.test_df)


class TestParsedDataset(TestCase):
    def setUp(self):
        self.test_df = pd.DataFrame({
            'name': ['New York', 'Tokyo', 'Coro', 'Madrid', 'Cefalu', 'Oslo'],
            'population(m)': [8.4, 9.3, 0.2, None, 0.014, 0.68],
            'city_class': ['lg', 'lg', 'sm', 'lg', 'sm', 'md']
        }, index=[1, 2, 3, 4, 5, 6])

        self.test_y = self.test_df['city_class'].copy().to_list()

        self.parsed_dataset = ParsedDataset({},
                                            self.test_df,
                                            label='city_class',
                                            original_format='csv',
                                            problem_type='classification')
    
    def test_initialize_with_invalid_label(self):
        with self.assertRaises(InvalidFeature):
            ParsedDataset({}, self.test_df, 'price')

    def test_get_num_records(self):
        self.assertEqual(self.parsed_dataset.get_num_records(), 6)

    def test_get_features(self):
        self.assertListEqual(self.parsed_dataset.get_features(),
                            ['name', 'population(m)'])

    def test_get_label(self):
        self.assertEqual(self.parsed_dataset.get_label(),
                         'city_class')

    def test_get_label_data(self):
        self.assertEqual(self.parsed_dataset.get_label_data(),
                         self.test_y)

    def test_get_na_pct(self):
        self.assertAlmostEqual(self.parsed_dataset.get_not_assigned_pct(),
                               8.33)

    def test_get_original_data_format(self):
        self.assertEqual(self.parsed_dataset.get_original_format(),
                         'csv')
    
    def test_get_class_counts(self):
        self.assertListEqual(self.parsed_dataset.get_y_value_counts(), [
            {'y': 'lg', 'count': 3},
            {'y': 'sm', 'count': 2},
            {'y': 'others', 'count': 1}
        ])
    
    @patch('mlplaygrounds.datasets.parsers.parser.pd.cut')
    def test_get_interval_counts(self, mock_pd_cut):
        pass
