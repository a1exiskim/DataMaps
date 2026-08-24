from pathlib import Path

def get_source(path):
    source_objs = []
    path_obj = Path(path)

    if path_obj.exists() is False:
        raise ValueError('Path does not exist')
    elif path_obj.is_dir() is False:
        raise NotADirectoryError('Path does not lead to directory')
    else: 
        for object in path_obj.iterdir():
            source_objs.append(object)

        return source_objs

