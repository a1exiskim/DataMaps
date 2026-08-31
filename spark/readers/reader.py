from abc import ABC, abstractmethod
from spark.ingestion import Source

class Reader(ABC):

    @abstractmethod
    def read(self, source):
        """Read the source and return a Spark DataFrame."""

    
