import os, sys
from leawind_inventory.fs.temp import (
    TempDir,
    TempFile,
)


def test_temp_dir():
    """Test synchronous temporary directory context manager"""
    print("=== Testing TempDir (context manager) ===")

    # Test with keyword arguments
    dir_path = None
    with TempDir(prefix="test-", suffix="-dir") as path:
        dir_path = path
        print(f"  Temporary directory created: {path}")
        assert os.path.exists(path)
        assert os.path.isdir(path)
        assert path.startswith("test-")
        assert path.endswith("-dir")

        # Create a test file inside
        test_file = os.path.join(path, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")
        assert os.path.exists(test_file)

    # Verify directory was removed
    assert not os.path.exists(dir_path)
    print("  ✓ Directory was automatically removed")


def test_temp_file():
    """Test synchronous temporary file context manager"""
    print("\n=== Testing TempFile (context manager) ===")

    # Test with keyword arguments
    file_path = None
    with TempFile(prefix="test-", suffix=".txt") as path:
        file_path = path
        print(f"  Temporary file created: {path}")
        assert os.path.exists(path)
        assert os.path.isfile(path)
        assert path.startswith("test-")
        assert path.endswith(".txt")

        # Write content to the file
        with open(path, "w") as f:
            f.write("test file content")

        # Read the content back
        with open(path, "r") as f:
            content = f.read()
        assert content == "test file content"

    # Verify file was removed
    assert not os.path.exists(file_path)
    print("  ✓ File was automatically removed")
