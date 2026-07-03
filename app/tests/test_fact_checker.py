from app.services.fact_checker import fact_check


def test_fact_check():

    result = fact_check(
        "Artificial Intelligence"
    )

    assert isinstance(
        result,
        str
    )


def test_invalid_topic():

    result = fact_check(
        "asdfghjklqwerty12345"
    )

    assert isinstance(
        result,
        str
    )