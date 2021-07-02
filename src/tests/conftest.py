from datetime import datetime

import pytest

from hiperline.model import Item, Person


@pytest.fixture
def portuguese():
    return "pt"


@pytest.fixture
def dpedro_I():
    return Person(name="Dom Pedro I", start=datetime(1798, 10, 12), end=datetime(1834, 9, 24))


@pytest.fixture
def dpedro_II():
    return Person(name="Dom Pedro II", start=datetime(1825, 12, 2), end=datetime(1891, 12, 5))


@pytest.fixture
def independencia():
    return Item(name="Independência do Brasil", start=datetime(1822, 9, 7))


@pytest.fixture
def republica():
    return Item(name="Proclamação da República", start=datetime(1889, 11, 15))
