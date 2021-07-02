from datetime import datetime

import pytest

from hiperline.model import Item, Person


@pytest.fixture
def date_format():
    return "%Y-%m-%d"


@pytest.fixture
def dpedro_I(date_format):
    return Person(
        name="Dom Pedro I",
        start=datetime.strptime("1798-10-12", date_format),
        end=datetime.strptime("1834-09-24", date_format),
    )


@pytest.fixture
def dpedro_II(date_format):
    return Person(
        name="Dom Pedro II",
        start=datetime.strptime("1825-12-02", date_format),
        end=datetime.strptime("1891-12-05", date_format),
    )


@pytest.fixture
def independencia(date_format):
    return Item(
        name="Independência do Brasil",
        start=datetime.strptime("1822-09-07", date_format),
    )


@pytest.fixture
def republica(date_format):
    return Item(
        name="Proclamação da República",
        start=datetime.strptime("1889-11-15", date_format),
    )
