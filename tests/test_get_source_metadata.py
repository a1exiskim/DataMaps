from src.metadata_discovery import get_source_metadata
from datetime import datetime

def test_correct_return(tmp_path):
    test_file = tmp_path/ "test.json"
    test_file.touch()

    test_file_timestamp = test_file.stat().st_mtime
    result = get_source_metadata(test_file)

    assert result == {"name": "test.json",
                      "path": test_file,
                      "extension": ".json",
                      "size_bytes": test_file.stat().st_size,
                      "last modified": datetime.fromtimestamp(test_file_timestamp)
                      }


def test_directory_metadata(tmp_path):
    test_dir = tmp_path/ "test folder"
    test_dir.mkdir()

    test_dir_timestamp = test_dir.stat().st_mtime

    result = get_source_metadata(test_dir)

    assert result == {"name": "test folder",
                      "path": test_dir,
                      "extension": "",
                      "size_bytes": test_dir.stat().st_size,
                      "last modified": datetime.fromtimestamp(test_dir_timestamp)}