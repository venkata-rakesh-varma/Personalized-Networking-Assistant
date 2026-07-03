from app.services.event_analyzer import extract_event_themes


def test_extract_event_themes():

    description = """
    AI Conference discussing Machine Learning,
    Generative AI and Cloud Computing.
    """

    themes = extract_event_themes(description)

    assert isinstance(themes, list)

    assert len(themes) == 3


def test_empty_description():

    themes = extract_event_themes("")

    assert isinstance(themes, list)