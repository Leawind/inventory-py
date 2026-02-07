import os, random, string
from typing import Mapping, TypeVar, overload

T = TypeVar("T")


@overload
def by_platform(value: Mapping[str, T]) -> T | None: ...
@overload
def by_platform(value: Mapping[str, T], default: T) -> T: ...
def by_platform(value: Mapping[str, T], default: T | None = None) -> T | None:
    """
    Select a value based on the current operating system.

    The current platform is determined by :data:`os.name`.

    Lookup order:
        1. The key matching ``os.name`` (e.g. ``"posix"``, ``"nt"``)
        2. The provided ``default`` value

    Args:
        value:
            A mapping from platform names to values.
        default:
            A fallback value returned when no platform-specific entry exists.
            If omitted, ``None`` is returned.

    Returns:
        The value associated with the current platform, or the fallback value.
        If no fallback is provided, ``None`` may be returned.
    """
    return value.get(os.name, default)


def random_string(
    length: int = 8,
    chars: str = string.ascii_lowercase + string.digits,
) -> str:
    """
    Generate a random string of fixed length.

    Args:
        length:
            The length of the string to generate.
            Must be greater than 0.

        chars:
            The characters to use when generating the string.
            Defaults to ``string.ascii_lowercase + string.digits``.
            Must be non-empty.

    Example:
        >>> random_string()
        '5c5f7c0d'
    """
    return "".join(random.choices(chars, k=length))
