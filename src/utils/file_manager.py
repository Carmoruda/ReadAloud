import os


class FileManager:
    @staticmethod
    def ensure_dir(path: str) -> None:
        """Ensures that a directory exists at the specified path.
        If the directory does not exist, it creates it.

        Args:
            path (str): The path to the directory to ensure.
        """
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def file_exists(path: str) -> bool:
        """Checks if a file exists at the specified path.
        This method returns True if the file exists, otherwise False.

        Args:
            path (str): The path to the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """

        return os.path.isfile(path)

    @staticmethod
    def dir_exists(path: str) -> bool:
        """Checks if a directory exists at the specified path.

        Args:
            path (str): _description_

        Returns:
            bool: _description_
        """

        return os.path.isdir(path)
