import json
import os
import time
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import cast, Union, List

import boto3
from jsonlines import jsonlines

from src import settings


class DataLakeWriter(metaclass=ABCMeta):
    @abstractmethod
    def write(self, key: str, data: Union[dict, List[dict]]) -> None:
        pass


class FileSystemWriter(DataLakeWriter):
    def write(self, key: str, data: Union[dict, List[dict]]) -> None:
        write_path_with_data_lake = os.path.join('.localdatalake', key)
        Path(os.path.join(*write_path_with_data_lake.split(os.path.sep)[0:-1])).mkdir(parents=True, exist_ok=True)
        with cast(jsonlines.Writer, jsonlines.open(write_path_with_data_lake, 'w', compact=True)) as writer:
            writer.write_all([data])


class S3Writer(DataLakeWriter):
    def __init__(self):
        self.__client = boto3.client('s3')

    def write(self, key: str, data: Union[dict, List[dict]]) -> None:
        write_timestamp = int(time.time())
        items = data if isinstance(data, list) else [data]
        self.__client.put_object(
            Body='\n'.join([json.dumps(x) for x in items]),
            Bucket=settings.s3_bucket,
            Key=key,
            Metadata={
                'write_timestamp': str(write_timestamp)
            }
        )


def get_writer() -> DataLakeWriter:
    return S3Writer() if settings.write_to_s3 else FileSystemWriter()