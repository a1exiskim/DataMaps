from abc import ABC, abstractmethod
from spark.ingestion import Source

class Reader(ABC):
    """Defines the interface for reading data sources and raw records."""

    @abstractmethod
    def read(self, file_path, format, options):
        """Read the file and return a Spark DataFrame.
        
        Args:
            file_path: Path to the file to read.
            format: Format of the file.
            options: Format-specific options used when reading the file.
        """

    @abstractmethod
    def read_raw(self, file_path):
        """Read the source and return the raw data."""
