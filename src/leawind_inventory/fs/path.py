import os
from typing import List, Tuple, Union

PathLike = Union[str, "Path"]
"""
Type alias for path-like objects.
"""


class Path:
    """
    An object-oriented interface for working with file paths and performing file system operations.

    The Path class provides a convenient way to manipulate paths across different operating systems
    (Windows, Linux, macOS) while maintaining a consistent API.

    Examples:
        >>> p = Path("/home/user")
        >>> q = p / "documents" / "file.txt"
        >>> print(q)
        /home/user/documents/file.txt
        >>> q.exists()
        False
        >>> q.write_text("Hello World")
        >>> q.exists()
        True
        >>> q.read_text()
        "Hello World"
    """

    @staticmethod
    def as_str(path: PathLike) -> str:
        """
        Convert a PathLike object to a string representation.

        Args:
            path (PathLike): A string or Path object to convert.

        Returns:
            str: The string representation of the path.
        """
        if isinstance(path, Path):
            return str(path)
        return path

    @staticmethod
    def cwd() -> "Path":
        """
        Return a Path object representing the current working directory.

        Returns:
            Path: The current working directory as a Path object.
        """
        return Path(os.getcwd())

    def __init__(self, path: PathLike):
        """
        Initialize a new Path object.

        Args:
            path (PathLike): A string or Path object representing the path.
        """
        if isinstance(path, Path):
            path = str(path)
        self.path = path

    def to_str(self) -> str:
        """
        Return the string representation of the path.

        Returns:
            str: The string representation of the path.
        """
        return self.path

    ################################################################
    # Built-in Methods
    ################################################################

    def __str__(self):
        """
        Return the string representation of the path.

        Returns:
            str: The string representation of the path.
        """
        return self.path

    def __truediv__(self, other: str) -> "Path":
        """
        Join the path with other.

        Args:
            other (str): The other path to join.

        Returns:
            Path: The joined path.

        Examples:
            >>> Path("/home/user") / "documents"
            "/home/user/documents"
        """
        return Path(os.path.join(self.path, other))

    def __repr__(self):
        """
        Return the string representation of the path.

        Returns:
            str: The string representation of the path.
        """
        return self.path

    ################################################################
    # Path Operations
    ################################################################

    def is_abs(self) -> bool:
        r"""
        Check if the path is absolute. It works for both Unix and Windows.

        Examples:
            >>> Path("/home/user").is_abs()
            True
            >>> Path(r"D:\home\user").is_abs()
            True
            >>> Path("relative/path").is_abs()
            False
        """
        return os.path.isabs(self.path)

    def is_rel(self) -> bool:
        """
        Check if the path is relative. It works for both Unix and Windows.

        Returns:
            bool: True if the path is relative, False otherwise.

        Examples:
            >>> Path("relative/path").is_rel()
            True
            >>> Path("/absolute/path").is_rel()
            False
        """
        return not self.is_abs()

    def to_abs(self) -> "Path":
        """
        Return an absolute version of the path.

        Returns:
            Path: An absolute path.

        Examples:
            >>> Path("./relative").to_abs()
            /current/directory/relative
        """
        return Path(os.path.abspath(self.path))

    def to_rel(self, base: str = ".") -> "Path":
        """
        Return a relative path to this path from the given base directory.

        Args:
            base (str, optional): The base directory from which to compute the relative path.
                Defaults to the current working directory.

        Returns:
            Path: A relative path from base to this path.

        Examples:
            >>> Path("/home/user/docs").to_rel("/home")
            user/docs
        """
        return Path(os.path.relpath(self.path, base))

    def name(self) -> str:
        """
        Return the base name of the path (the final component).

        Returns:
            str: The base name of the path.

        Examples:
            >>> Path("/home/user/file.txt").name()
            file.txt
            >>> Path("/home/user/dir").name()
            dir
        """
        return os.path.basename(self.path)

    def name_no_ext(self) -> str:
        """
        Return the base name without the file extension.

        Returns:
            str: The base name without the extension.

        Examples:
            >>> Path("file.txt").name_no_ext()
            file
            >>> Path("archive.tar.gz").name_no_ext()
            archive.tar
        """
        return os.path.splitext(self.name())[0]

    def dotext(self) -> str:
        """
        Extension with dot

        Examples:
        >>> Path("file.tar.gz").dotext()
        ".gz"
        """
        return os.path.splitext(self.name())[1]

    def ext(self) -> str:
        """
        Extension without dot
        Examples:
        >>> Path("file.tar.gz").ext()
        "gz"
        """
        return os.path.splitext(self.name())[1].lstrip(".")

    def normcase(self) -> "Path":
        """
        Normalize the case of the path.

        On Windows, converts the path to lowercase and forward slashes to backslashes.
        On Unix, returns the path unchanged.

        Returns:
            Path: The normalized path.

        Examples:
            >>> Path("D:/Home/User").normcase()  # Windows
            d:\\home\\user
            >>> Path("/Home/User").normcase()  # Unix
            /Home/User
        """
        return Path(os.path.normcase(self.path))

    def join(self, *paths: str) -> "Path":
        """
        Join one or more path components intelligently.

        Args:
            *paths (str): Path components to join to this path.

        Returns:
            Path: The joined path.

        Examples:
            >>> Path("/home").join("user", "documents", "file.txt")
            /home/user/documents/file.txt
        """
        return Path(os.path.join(self.path, *paths))

    def split(self) -> Tuple[str, str]:
        """
        Split the path into (head, tail) where tail is the final path component
        and head is everything leading up to that.

        Returns:
            Tuple[str, str]: A tuple containing the head and tail of the path.

        Examples:
            >>> Path("/home/user/file.txt").split()
            ('/home/user', 'file.txt')
            >>> Path("/home/user/").split()
            ('/home', 'user')
        """
        return os.path.split(self.path)

    def splitext(self) -> Tuple[str, str]:
        """
        Split the path into (root, ext) where ext is the extension including
        the leading dot and root is everything leading up to that.

        Returns:
            Tuple[str, str]: A tuple containing the root and extension of the path.

        Examples:
            >>> Path("file.txt").splitext()
            ('file', '.txt')
            >>> Path("archive.tar.gz").splitext()
            ('archive.tar', '.gz')
        """
        return os.path.splitext(self.path)

    def splitdrive(self) -> Tuple[str, str]:
        """
        Split the path into (drive, tail) where drive is the drive letter
        or UNC path (on Windows) and tail is the rest of the path.

        On Unix, the drive component is always empty.

        Returns:
            Tuple[str, str]: A tuple containing the drive and tail of the path.

        Examples:
            >>> Path("D:/home/user").splitdrive()  # Windows
            ('D:', '/home/user')
            >>> Path("/home/user").splitdrive()  # Unix
            ('', '/home/user')
        """
        return os.path.splitdrive(self.path)

    def parent(self) -> "Path":
        """
        Return the parent directory of this path.

        Returns:
            Path: The parent directory.

        Examples:
            >>> Path("/home/user/file.txt").parent()
            /home/user
            >>> Path("/home/user/").parent()
            /home
        """
        return Path(os.path.dirname(self.path))

    def common_path(self, *others: PathLike) -> "Path":
        """
        Return the longest common subpath of this path and the given paths.

        Args:
            *others (PathLike): Other paths to find common path with.

        Returns:
            Path: The longest common subpath.

        Examples:
            >>> Path("/home/user1/docs").common_path(Path("/home/user2/pics"))
            /home
        """
        return Path(os.path.commonpath([self.path, *[Path.as_str(p) for p in others]]))

    def expand_user(self) -> "Path":
        """
        Expand the tilde (~) in the path to the user's home directory.

        Returns:
            Path: A path with ~ expanded.

        Examples:
            >>> Path("~").expand_user()
            /home/username  # Unix
            C:\\Users\\username  # Windows
        """
        return Path(os.path.expanduser(self.path))

    def expand_vars(self) -> "Path":
        """
        Expand environment variables in the path.

        Returns:
            Path: A path with environment variables expanded.

        Examples:
            >>> Path("$HOME/docs").expand_vars()
            /home/username/docs  # Unix
        """
        return Path(os.path.expandvars(self.path))

    ################################################################
    # File System Operations
    ################################################################

    ################################
    # Query

    def exists(self) -> bool:
        """
        Check if the path exists on the file system.

        Returns:
            bool: True if the path exists, False otherwise.
        """
        return os.path.exists(self.path)

    def lexists(self) -> bool:
        """
        Check if the path exists on the file system, following symlinks.

        Returns:
            bool: True if the path exists, False otherwise.
        """
        return os.path.lexists(self.path)

    def is_dir(self) -> bool:
        """
        Check if the path points to a directory on the file system.

        Returns:
            bool: True if the path is a directory, False otherwise.
        """
        return os.path.isdir(self.path)

    def is_file(self) -> bool:
        """
        Check if the path points to a regular file on the file system.

        Returns:
            bool: True if the path is a file, False otherwise.
        """
        return os.path.isfile(self.path)

    def is_link(self) -> bool:
        """
        Check if the path points to a symbolic link.

        Returns:
            bool: True if the path is a symbolic link, False otherwise.
        """
        return os.path.islink(self.path)

    def is_mount(self) -> bool:
        """
        Check if the path points to a mount point.

        Returns:
            bool: True if the path is a mount point, False otherwise.
        """
        return os.path.ismount(self.path)

    def get_size(self) -> int:
        """
        Return the size of the file in bytes.

        Returns:
            int: The size of the file in bytes.

        Raises:
            OSError: If the file does not exist or is inaccessible.
        """
        return os.path.getsize(self.path)

    def get_mtime(self) -> float:
        """
        Return the time of last modification of the path.

        Returns:
            float: A timestamp representing the last modification time.

        Raises:
            OSError: If the path does not exist or is inaccessible.
        """
        return os.path.getmtime(self.path)

    def get_atime(self) -> float:
        """
        Return the time of last access of the path.

        Returns:
            float: A timestamp representing the last access time.

        Raises:
            OSError: If the path does not exist or is inaccessible.
        """
        return os.path.getatime(self.path)

    def get_ctime(self) -> float:
        """
        Return the creation time of the path.

        On Windows, this is the actual creation time.
        On Unix, this is the time of last metadata change.

        Returns:
            float: A timestamp representing the creation time.

        Raises:
            OSError: If the path does not exist or is inaccessible.
        """
        return os.path.getctime(self.path)

    def same_file(self, other: PathLike) -> bool:
        """
        Check if this path and the given path refer to the same file or directory.

        Args:
            other (PathLike): The other path to compare with.

        Returns:
            bool: True if both paths refer to the same file/directory, False otherwise.

        Raises:
            OSError: If either path does not exist or is inaccessible.
        """
        return os.path.samefile(self.path, Path.as_str(other))

    ################################
    # Modify

    def mkdir(self, exist_ok: bool = True) -> None:
        """
        Create a directory and any necessary parent directories.

        Args:
            exist_ok (bool, optional): If False, raise an error if the directory already exists.
                Defaults to True.

        Raises:
            OSError: If the directory cannot be created and exist_ok is False.
        """
        os.makedirs(self.path, exist_ok=exist_ok)

    def touch(self) -> None:
        """
        Create an empty file at this path.

        If the file already exists, this function does nothing.

        Raises:
            OSError: If the operation fails.
        """
        open(self.path, "a").close()

    def listdir(self) -> List["Path"]:
        """
        Return a list of all files and directories in this directory.

        Returns:
            List[Path]: A list of Path objects representing entries in the directory.

        Raises:
            NotADirectoryError: If this path is not a directory.
            OSError: If the operation fails.
        """
        return [Path(os.path.join(self.path, p)) for p in os.listdir(self.path)]

    def read_text(self) -> str:
        """
        Read the entire file content as a string.

        Returns:
            str: The file content.

        Raises:
            IsADirectoryError: If this path is a directory.
            OSError: If the operation fails.
        """
        with open(self.path, "r") as f:
            return f.read()

    def write_text(self, content: str) -> None:
        """
        Write a string to the file, overwriting existing content.

        Args:
            content (str): The content to write to the file.

        Raises:
            IsADirectoryError: If this path is a directory.
            OSError: If the operation fails.
        """
        with open(self.path, "w") as f:
            f.write(content)

    def remove(self) -> None:
        """
        Delete the file or directory at this path.

        If the path is a directory, it will be deleted recursively along with all its contents.

        Raises:
            FileNotFoundError: If the path does not exist.
            OSError: If the operation fails.
        """
        if self.is_file():
            os.remove(self.path)
        elif self.is_dir():
            import shutil

            shutil.rmtree(self.path)
        else:
            raise FileNotFoundError(f"Path does not exist: {self.path}")

    def move_to(self, dst: PathLike) -> None:
        """
        Rename/move this file or directory to the given destination.

        Args:
            dst (PathLike): The destination path.

        Raises:
            OSError: If the operation fails.
        """
        os.rename(self.path, Path.as_str(dst))

    def copy_to(
        self, dst: PathLike, symlinks: bool = False, dirs_exist_ok: bool = False
    ) -> None:
        """
        Copy the file or directory at this path to the destination path.

        If the path is a directory, it will be copied recursively along with all its contents.

        Args:
            dst (PathLike): The destination path.
            symlinks (bool, optional): If True, copy symbolic links as symbolic links instead of copying the
                files they point to. Defaults to False.
            dirs_exist_ok (bool, optional): If True, existing directories at the destination will not cause an error.
                Defaults to False.

        Raises:
            FileNotFoundError: If the source path does not exist.
            OSError: If the operation fails.
        """
        import shutil

        dst_str = Path.as_str(dst)

        if self.is_file():
            shutil.copy2(self.path, dst_str, follow_symlinks=symlinks)
        elif self.is_dir():
            shutil.copytree(
                self.path,
                dst_str,
                symlinks=symlinks,
                dirs_exist_ok=dirs_exist_ok,
            )
        else:
            raise FileNotFoundError(f"Path does not exist: {self.path}")

    def walk(
        self,
        topdown: bool = True,
        onerror=None,
        followlinks: bool = False,
    ):
        """
        Generate the file names in a directory tree by walking the tree either top-down or bottom-up.

        Args:
            topdown (bool, optional): If True, walk from top-down; if False, walk from bottom-up.
                Defaults to True.
            onerror (callable, optional): A function to call when an error occurs.
                Defaults to None.
            followlinks (bool, optional): If True, follow symbolic links.
                Defaults to False.

        Yields:
            Tuple: (dirpath, dirnames, filenames): `Tuple[str, List[str], List[str]]`
        """
        return os.walk(
            self.path,
            topdown=topdown,
            onerror=onerror,
            followlinks=followlinks,
        )
