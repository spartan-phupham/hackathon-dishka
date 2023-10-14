import glob
import os


def find_file(file_name: str) -> str:
    """
    Find the path of file with the given name in the project.

    :param file_name: name of the file to search for.
    :return: path of the found file.
    """
    search_pattern = f"**/{file_name}"
    file_paths: list[str] = glob.glob(search_pattern, recursive=True)
    return file_paths[0]


def find_directories(directory_name: str) -> str:
    """
    Find the path of the directory with the given name in the project.

    :param directory_name: name of the directory to search for.
    :return: path of the found directory.
    """
    search_pattern = os.path.join("**", directory_name)
    directory_paths = glob.glob(search_pattern, recursive=True)
    return os.path.join(directory_paths[0], "")
