from json import loads
from io import StringIO

import pandas as pd

from django.core.files.base import File

from .exceptions import InvalidFormat, InvalidFile, InvalidFeature


class DatasetParser:
    FILE_FORMATS = ['csv', 'json']

    def __init__(self, file, file_format, to_format,
                 label=None, index_col=None, problem_type=None):
        self.file = file
        self.file_format = file_format
        self.to_format = to_format
        self.index_col = index_col
        self.label = label
        self.problem_type = problem_type
    
    def parse(self):
        if self.is_valid():
            df = self.read()
            data = self.write(df)
            return ParsedDataset(data, df, self.label, self.index_col,
                                 self.file_format, self.problem_type)
        return None
    
    def is_valid(self):
        return all([
            self.file_is_valid(), 
            self.file_formats_are_valid(),
            self.problem_type_is_valid()
        ])

    def file_is_valid(self):
        if isinstance(self.file, (File, StringIO, str)):
            return True
        raise InvalidFile('Not a proper file')
    
    def file_formats_are_valid(self):
        if self.file_format not in self.FILE_FORMATS:
            raise InvalidFormat(
                'The specified file format is not supported/valid')

        if self.to_format not in self.FILE_FORMATS:
            raise InvalidFormat(
                'The desired format is not supported/valid')

        return True
    
    def problem_type_is_valid(self):
        if self.problem_type is None:
            raise ValueError('You must specify the problem type')
        return True

    def read(self):
        try:
            if self.file_format == self.FILE_FORMATS[0]:
                return pd.read_csv(self.file, index_col=self.index_col)
            elif self.file_format == self.FILE_FORMATS[1]:
                return pd.read_json(self.file)
            
            raise InvalidFormat(
                f'Can not read file format {self.file_format.upper()}')
        except (ValueError, pd.errors.ParserError, pd.errors.EmptyDataError):
            raise InvalidFile(
                f'Could not read data as a {self.file_format.upper()} file')
    
    def write(self, df, path_or_buffer=None):
        if self.to_format == self.FILE_FORMATS[0]:
            return df.to_csv(path_or_buffer)
        elif self.to_format == self.FILE_FORMATS[1]:
            return loads(df.to_json(orient='records'))

        raise InvalidFormat(
            f'Can not write data to {self.to_format.upper()} format')


class ParsedDataset:
    def __init__(self, parsed_data, data=None, label=None,
                 index_col=None, original_format=None, problem_type=None):
        self.parsed_data = parsed_data
        self.data = data
        self.label = label
        self.label_data = None
        self.index_col = index_col
        self.original_format = original_format
        self.problem_type = problem_type

        if self.label is not None:
            if self._label_is_valid():
                self.label_data = self.data.pop(self.label)
            else:
                raise InvalidFeature(
                    f'Could not set label: {self.label} is not a valid column')
    
    def _label_is_valid(self):
        if self.label in [col for col in self.data.columns]:
            return True
        return False

    def get_data(self):
        return self.parsed_data
    
    def get_num_records(self):
        return len(self.data)
    
    def get_features(self):
        return [col for col in self.data.columns if col != self.label]
    
    def get_label(self):
        return self.label
    
    def get_label_data(self):
        return self.label_data.to_list() if self.label is not None else None

    def get_index_col(self):
        return self.index_col
    
    def get_not_assigned_pct(self):
        na_pct = self.data.isnull().mean() * 100
        return round(na_pct.mean(), 2)

    def get_original_format(self):
        return self.original_format

    def get_y_value_counts(self):
        if self.problem_type == 'regression':
            return self._calculate_interval_distribution()
        elif self.problem_type == 'classification':
            return self._calculate_class_distribution()
        
        raise ValueError(f'{self.problem_type} is not a valid problem type')

    def _calculate_interval_distribution(self):
        bin_counts = pd.cut(self.label_data, bins=6).value_counts()
        return self._y_counts(bin_counts)

    def _calculate_class_distribution(self):
        class_counts = self.label_data.value_counts()
        return self._y_counts(class_counts)
    
    def _y_counts(self, value_counts, by_interval=False):
        """ 
        Transforms value_counts into a three-element dict,
        not only for simplicity purposes but also to ease plotting.

        Two of the elements are the most common y values, 
        the other is a sum of all other y values' counts.
        """
        counts = []
        others_count = 0
        for i, (name, count) in enumerate(value_counts.to_dict().items()):
            if i > 1:
                others_count += count
            else:
                counts.append({
                    'y': str(name),
                    'count': count
                })

        if others_count > 0:
            counts.append({
                'y': 'others',
                'count': others_count
            })

        return counts
