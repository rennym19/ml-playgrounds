from json import loads
from io import StringIO

import pandas as pd

from django.core.files.base import File

from .exceptions import InvalidFormat, InvalidFile, InvalidFeature


class DatasetParser:
    FILE_FORMATS = ['csv', 'json']

    def __init__(self, file, file_format, to_format,
                 label=None, index_col=None):
        self.file = file
        self.file_format = file_format
        self.to_format = to_format
        self.index_col = index_col
        self.label = label
    
    def parse(self):
        if self.file_is_valid() and self.file_formats_are_valid():
            df = self.read()
            data = self.write(df)
            return ParsedDataset(data, df, self.label,
                                 self.index_col, self.file_format)
        return None
    
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
                 index_col=None, original_format=None):
        self.parsed_data = parsed_data
        self.data = data
        self.label = label
        self.label_data = None
        self.index_col = index_col
        self.original_format = original_format

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
