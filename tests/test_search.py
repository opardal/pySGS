import pytest
import requests

from sgs.search import *
from sgs.common import to_datetime, to_datetime_string


@pytest.mark.search
@pytest.mark.parametrize("language", ["en", "pt"])
def test_init_search_session(language):
    session = init_search_session(language)
    assert isinstance(session, requests.Session)


@pytest.mark.search
def test_search_by_code_english():
    code = 4
    results = search_ts(code, Language.en.value)
    print(results)
    metadata = results[0]
    assert metadata['name'] == "BM&F Gold - gramme"
    assert metadata['first_value'] == to_datetime_string("29/12/1989", "en", "%Y-%m-%d %H:%M:%S")
    assert metadata['frequency'] == "D"


@pytest.mark.search
def test_search_by_code_portuguese():
    code = 4
    results = search_ts(code, Language.pt.value)
    metadata = results[0]
    assert metadata['name'] == "Ouro BM&F - grama"
    assert metadata['first_value'] == to_datetime_string("29/12/1989", "pt", "%Y-%m-%d %H:%M:%S")
    assert metadata['frequency'] == "D"


@pytest.mark.search
@pytest.mark.parametrize(
    "query,language,expected",
    [
        (
            4,
            "pt",
            {
                "name": "Ouro BM&F - grama",
                "first_value": to_datetime_string("29/12/1989", "pt", "%Y-%m-%d %H:%M:%S"),
                "freq": "D",
            },
        ),
        (
            4,
            "en",
            {
                "name": "BM&F Gold - gramme",
                "first_value": to_datetime_string("29/12/1989", "en", "%Y-%m-%d %H:%M:%S"),
                "freq": "D",
            },
        ),
        (
            28209,
            "pt",
            {
                "name": (
                    "Saldo de títulos de dívida emitidos por "
                    "empresas e famílias - títulos privados"
                ),
                "first_value": to_datetime_string("01/01/2013", "pt", "%Y-%m-%d %H:%M:%S"),
                "freq": "M",
            },
        ),
    ],
)
def test_search_by_code(query, language, expected):
    results = search_ts(query, language)
    assert isinstance(results, list)
    results = results[0]
    assert results["frequency"] == expected["freq"]
    assert results["name"] == expected["name"]
    assert results["first_value"] == expected["first_value"]


@pytest.mark.search
def test_search_by_text():
    results = search_ts("Ouro BM$F - grama", "pt")
    assert isinstance(results, list)
    assert len(results) == 1

    # portuguese query and english language returns None
    results = search_ts("Ouro BM$F - grama", "en")
    assert results is None


@pytest.mark.search
def test_search_by_text_query_returns_multiple_result_pages():
    results = search_ts("produto", "pt")
    assert isinstance(results, list)
    assert len(results) == 50


@pytest.mark.search
def test_search_by_text_multiple_results():
    results = search_ts("dolar", "pt")
    assert isinstance(results, list)
    result_count = 41
    assert len(results) == result_count
    assert results[0]["code"] == 1
    assert results[-1]["code"] == 21636
