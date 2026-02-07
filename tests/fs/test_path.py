import os
import sys
from leawind_inventory.fs.path import Path


def test_path_construction():
    """Test Path object construction"""
    print("=== Testing Path Construction ===")

    # Test with string path
    p1 = Path("/home/user")
    assert str(p1) == "/home/user"

    # Test with Path object (copy constructor)
    p2 = Path(p1)
    assert str(p2) == "/home/user"

    # Test current working directory
    cwd = Path.cwd()
    assert str(cwd) == os.getcwd()

    print("  ✓ Path construction tests passed")


def test_path_operations():
    """Test basic path operations"""
    print("\n=== Testing Path Operations ===")

    p = Path("/home/user")

    # Test __truediv__ (/) operator
    p2 = p / "documents" / "file.txt"
    assert str(p2) == os.path.join("/home/user", "documents", "file.txt")

    # Test join method
    p3 = p.join("documents", "file.txt")
    assert str(p3) == os.path.join("/home/user", "documents", "file.txt")

    # Test basename
    assert Path("/home/user/file.txt").name() == "file.txt"

    # Test name_no_ext
    assert Path("file.txt").name_no_ext() == "file"

    # Test dotext and ext
    assert Path("file.txt").dotext() == ".txt"
    assert Path("file.txt").ext() == "txt"
    assert Path("file.tar.gz").dotext() == ".gz"
    assert Path("file.tar.gz").ext() == "gz"

    # Test split
    dir_part, file_part = Path("/home/user/file.txt").split()
    assert dir_part == "/home/user"
    assert file_part == "file.txt"

    # Test parent
    assert str(Path("/home/user/file.txt").parent()) == "/home/user"

    print("  ✓ Path operations tests passed")


def test_path_properties():
    """Test path properties like absolute/relative"""
    print("\n=== Testing Path Properties ===")

    # Test absolute/relative paths
    abs_path = Path("/home/user")
    assert abs_path.is_abs()
    assert not abs_path.is_rel()

    rel_path = Path("user/documents")
    assert rel_path.is_rel()
    assert not rel_path.is_abs()

    # Test conversion between absolute and relative
    converted_abs = rel_path.to_abs()
    assert converted_abs.is_abs()

    # Test normcase
    if os.name == "nt":
        # Windows-specific test
        win_path = Path("D:\\Home\\User")
        assert str(win_path.normcase()).lower() == "d:\\home\\user"
    else:
        # Unix-specific test
        unix_path = Path("/Home/User")
        assert str(unix_path.normcase()) == "/Home/User"  # Unix doesn't change case

    # Test expand_user
    home_path = Path("~").expand_user()
    assert home_path.is_abs()

    print("  ✓ Path properties tests passed")


def test_file_system_operations():
    """Test file system operations"""
    print("\n=== Testing File System Operations ===")

    # Test exists/is_dir/is_file
    cwd = Path.cwd()
    assert cwd.exists()
    assert cwd.is_dir()
    assert not cwd.is_file()

    # Test touch/mkdir functionality with a temporary file
    from leawind_inventory.fs.temp import TempDir

    with TempDir(prefix="path-test-") as temp_dir:
        temp_path = Path(temp_dir)

        # Test mkdir
        new_dir = temp_path / "new_directory"
        new_dir.mkdir()
        assert new_dir.exists()
        assert new_dir.is_dir()

        # Test write_text/read_text
        test_file = temp_path / "test.txt"
        test_content = "Hello, Path!"
        test_file.write_text(test_content)
        assert test_file.exists()
        assert test_file.is_file()

        read_content = test_file.read_text()
        assert read_content == test_content

        # Test listdir
        files = temp_path.listdir()
        file_names = [f.name() for f in files]
        assert "test.txt" in file_names
        assert "new_directory" in file_names

        # Test same_file
        same_file = Path(str(test_file))
        assert test_file.same_file(same_file)

    print("  ✓ File system operations tests passed")


def test_walk():
    """Test directory walking functionality"""
    print("\n=== Testing Path.walk() ===")

    from leawind_inventory.fs.temp import TempDir

    with TempDir(prefix="walk-test-") as temp_dir:
        temp_path = Path(temp_dir)

        # Create a test directory structure
        (temp_path / "dir1").mkdir()
        (temp_path / "dir1" / "subdir").mkdir()
        (temp_path / "dir1" / "file1.txt").write_text("content1")
        (temp_path / "dir2").mkdir()
        (temp_path / "dir2" / "file2.txt").write_text("content2")

        # Test walk
        entries = list(temp_path.walk())
        assert len(entries) >= 3  # Should have at least 3 entries: root, dir1, dir2

        # Check if we can find the files
        found_files = []
        for root, dirs, files in temp_path.walk():
            for file in files:
                found_files.append(file)

        assert "file1.txt" in found_files
        assert "file2.txt" in found_files

    print("  ✓ Path.walk() tests passed")


def test_modify_operations():
    """Test file system modification operations"""
    print("\n=== Testing Modify Operations ===")

    from leawind_inventory.fs.temp import TempDir

    with TempDir(prefix="modify-test-") as temp_dir:
        temp_path = Path(temp_dir)

        # Test move_to
        source_file = temp_path / "source.txt"
        source_file.write_text("Test content")
        dest_file = temp_path / "destination.txt"
        source_file.move_to(dest_file)
        assert not source_file.exists()
        assert dest_file.exists()
        assert dest_file.read_text() == "Test content"

        # Test copy_to for file
        copied_file = temp_path / "copied.txt"
        dest_file.copy_to(copied_file)
        assert copied_file.exists()
        assert copied_file.read_text() == "Test content"

        # Test copy_to for directory
        source_dir = temp_path / "source_dir"
        source_dir.mkdir()
        (source_dir / "file1.txt").write_text("File 1 content")
        (source_dir / "file2.txt").write_text("File 2 content")
        dest_dir = temp_path / "dest_dir"
        source_dir.copy_to(dest_dir)
        assert dest_dir.exists()
        assert (dest_dir / "file1.txt").exists()
        assert (dest_dir / "file2.txt").exists()
        assert (dest_dir / "file1.txt").read_text() == "File 1 content"
        assert (dest_dir / "file2.txt").read_text() == "File 2 content"

        # Test remove for file
        copied_file.remove()
        assert not copied_file.exists()

        # Test remove for directory
        dest_dir.remove()
        assert not dest_dir.exists()

        print("  ✓ Modify operations tests passed")
