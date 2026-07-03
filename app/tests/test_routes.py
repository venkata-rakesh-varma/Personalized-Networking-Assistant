from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_generate_conversation():

    response = client.post(

        "/generate-conversation",

        json={

            "description":"AI Conference",

            "interests":[

                "Python",

                "Machine Learning"

            ]

        }

    )

    assert response.status_code == 200

    data = response.json()

    assert "topics" in data

    assert "suggestions" in data


def test_analyze_event():

    response = client.post(

        "/analyze-event",

        json={

            "description":"Blockchain Summit"

        }

    )

    assert response.status_code == 200


def test_fact_check():

    response = client.post(

        "/fact-check",

        json={

            "query":"Artificial Intelligence"

        }

    )

    assert response.status_code == 200


def test_history():

    response = client.get(
        "/history"
    )

    assert response.status_code == 200


def test_feedback():

    response = client.post(

        "/feedback",

        json={

            "suggestion":"Hello",

            "feedback":"positive"

        }

    )

    assert response.status_code == 200