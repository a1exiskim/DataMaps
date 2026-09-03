from abc import ABC, abstractmethod
from spark.ingestion import Source

class Reader(ABC):

    @abstractmethod
    def read(self, source):
        """Read the source and return a Spark DataFrame."""

    @abstractmethod
    def read_raw(self, file_path):
        """Read the source and return the raw data."""
