import logging, os
from leawind_inventory import misc

log = logging.getLogger(__name__)


def test_by_platform():
    platform_names = {
        "posix": "posix",
        "nt": "nt",
    }
    assert misc.by_platform(platform_names, "unknown") == os.name

    assert misc.by_platform({}) is None

    assert misc.by_platform({}, "default") == "default"
