import pytest
from src.source import get_source

def test_nonexistent_path(tmp_path):
    test_dir = tmp_path / "does_not_exist"

    with pytest.raises(ValueError):
        get_source(test_dir)

    assert test_dir.exists() is False

def test_not_directory(tmp_path):
    test_file = tmp_path / "test file"
    test_file.touch(exist_ok=True)

    with pytest.raises(NotADirectoryError):
        get_source(test_file)

def test_valid_path(tmp_path):
    test_dir = tmp_path / "test dir"
    test_dir.mkdir()
    dir1 = test_dir / "dir1"
    dir1.mkdir()
    dir2 = test_dir / "dir2"
    dir2.mkdir()

    result = get_source(test_dir)
    result_set = set(result)

    assert result_set == {dir1, dir2}

    
