from app.services.topic_generator import generate_topics


def test_generate_topics():

    themes = [

        "Artificial Intelligence",

        "Machine Learning",

        "Cloud Computing"

    ]

    interests = [

        "Python",

        "AI"

    ]

    suggestions = generate_topics(
        themes,
        interests
    )

    assert isinstance(
        suggestions,
        list
    )

    assert len(suggestions) >= 3


def test_empty_inputs():

    suggestions = generate_topics([], [])

    assert isinstance(suggestions, list)