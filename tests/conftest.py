"""
    Dummy conftest.py for fiora.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest


def test_import():
    import numpy
    import nibabel
    import rich
