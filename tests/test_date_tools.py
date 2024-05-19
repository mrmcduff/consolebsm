from app.utils import date_tools as dt
from datetime import datetime


def test_ymd_valid():
    response = dt.parse_date("2021-03-14")
    assert response["error"] is None
    assert response["date"].year == 2021
    assert response["date"].month == 3
    assert response["date"].day == 14
    assert response["valid"] is True


def test_ymd_invalid():
    response = dt.parse_date("2021-03-34")
    assert response["error"] == "2021-03-34 could not be parsed as a date"
    assert response["date"] is None
    assert response["valid"] is False


def test_mdy_valid():
    response = dt.parse_date("05/04/2024")
    assert response["error"] is None
    assert response["date"].year == 2024
    assert response["date"].month == 5
    assert response["date"].day == 4
    assert response["valid"] is True


def test_mdy_invalid():
    response = dt.parse_date("15/04/2024")
    assert response["error"] == "15/04/2024 could not be parsed as a date"
    assert response["date"] is None
    assert response["valid"] is False


def test_bmy_valid():
    response = dt.parse_date("4 May, 2023")
    assert response["error"] is None
    assert response["date"].year == 2023
    assert response["date"].month == 5
    assert response["date"].day == 4
    assert response["valid"] is True


def test_bmy_invalid():
    response = dt.parse_date("4 Ma, 2023")
    assert response["error"] == "4 Ma, 2023 could not be parsed as a date"
    assert response["date"] is None
    assert response["valid"] is False


def test_mby_valid():
    response = dt.parse_date("May 4, 2023")
    assert response["error"] is None
    assert response["date"].year == 2023
    assert response["date"].month == 5
    assert response["date"].day == 4
    assert response["valid"] is True


def test_mby_padded_valid():
    response = dt.parse_date("February 04, 2023")
    assert response["error"] is None
    assert response["date"].year == 2023
    assert response["date"].month == 2
    assert response["date"].day == 4
    assert response["valid"] is True


def test_output_date():
    output = dt.format_date(datetime.strptime("01/02/2023", "%m/%d/%Y"))
    assert output == "2023-01-02"
