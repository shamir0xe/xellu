import os


class FileFinder:
    @staticmethod
    def all_files_recursive(*paths, file_type: str='') -> list:
        files = [] 
        path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', *paths))
        for obj in os.scandir(path):
            if obj.is_file() and obj.name[-len(file_type):] == file_type:
                files.append((obj.name, obj.path))
            if obj.is_dir():
                files = [*files, *FileFinder.all_files_recursive(*[*paths, obj.name], file_type=file_type)]
        files.sort()
        return files
    