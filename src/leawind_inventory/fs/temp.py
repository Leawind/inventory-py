import os
from typing import Optional, ContextManager
import leawind_inventory.misc as misc

__all__ = [
    "TempDir",
    "TempFile",
]


def _find_temp_path(
    parent: Optional[str] = None,
    prefix: str = "",
    suffix: str = "",
    max_tries: int = 8,
    message: str = "Failed to find temp path",
) -> str:
    """Find an unused temporary path"""
    for _ in range(max_tries):
        random_string = misc.random_string(16)
        file_name = f"{prefix}{random_string}{suffix}"

        if parent:
            file_path = os.path.join(parent, file_name)
        else:
            file_path = file_name

        if not os.path.exists(file_path):
            return file_path

    raise RuntimeError(message)


class TempDir(ContextManager[str]):
    """
    Temporary directory context manager.
    Can be used with `with` statement or callback function.

    Examples:
    ---------
    >>> with TempDir(prefix="tmp-") as dir_path:
    ...     print(f"Temporary directory: {dir_path}")
    ...     # Work with the directory
    ... # Directory is automatically removed
    """

    def __init__(
        self,
        parent: Optional[str] = None,
        prefix: str = "",
        suffix: str = "",
        max_tries: int = 8,
    ):
        """
        Args:
            parent (Optional[str]): The parent directory path. Defaults to None, means the current working directory.
            prefix (str): The prefix of the temporary file or directory name.
            suffix (str): The suffix of the temporary file or directory name.
            max_tries (int): The maximum number of tries to find an unused path.
        """

        self.parent = parent
        self.prefix = prefix
        self.suffix = suffix
        self.max_tries = max_tries

    def __enter__(self) -> str:
        self.path = _find_temp_path(
            self.parent,
            self.prefix,
            self.suffix,
            self.max_tries,
            "Failed to create temp dir",
        )
        os.makedirs(self.path)
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.path and os.path.exists(self.path):
            import shutil

            shutil.rmtree(self.path)


class TempFile(ContextManager[str]):
    """
    Synchronous temporary file context manager.
    Can be used with `with` statement or callback function.

    Examples:
    ---------
    >>> # Using with statement (Pythonic way)
    >>> with TempFile(prefix="tmp-", suffix=".txt") as file_path:
    ...     print(f"Temporary file: {file_path}")
    ...     # Work with the file
    ... # File is automatically removed
    """

    def __init__(
        self,
        parent: Optional[str] = None,
        prefix: str = "",
        suffix: str = "",
        max_tries: int = 8,
    ):
        """
        Args:
            parent (Optional[str]): The parent directory path. Defaults to None, means the current working directory.
            prefix (str): The prefix of the temporary file or directory name.
            suffix (str): The suffix of the temporary file or directory name.
            max_tries (int): The maximum number of tries to find an unused path.
        """
        self.parent = parent
        self.prefix = prefix
        self.suffix = suffix
        self.max_tries = max_tries

    def __enter__(self) -> str:
        self.path = _find_temp_path(
            self.parent,
            self.prefix,
            self.suffix,
            self.max_tries,
            "Failed to create temp file",
        )
        open(self.path, "a").close()
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.path and os.path.exists(self.path):
            os.unlink(self.path)
