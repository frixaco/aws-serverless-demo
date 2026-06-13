import json

from notification_dispatcher import app


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {"data": {"publishNotification": {"receiverId": "receiver-1"}}}


def test_dispatcher_posts_publish_notification_mutation(monkeypatch):
    posted = {}

    def fake_post(url, *, headers, json, timeout):
        posted["url"] = url
        posted["headers"] = headers
        posted["json"] = json
        posted["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setenv("GRAPHQL_API_URL", "https://example.appsync-api/graphql")
    monkeypatch.setenv("GRAPHQL_API_KEY", "api-key")
    monkeypatch.setattr(app.requests, "post", fake_post)

    response = app.lambda_handler(
        {
            "Records": [
                {
                    "Sns": {
                        "Message": json.dumps(
                            {
                                "receiverId": "receiver-1",
                                "payload": {
                                    "activityId": "activity-1",
                                    "message": "hello",
                                },
                            }
                        )
                    }
                }
            ]
        },
        None,
    )

    assert response == {"data": {"publishNotification": {"receiverId": "receiver-1"}}}
    assert posted["url"] == "https://example.appsync-api/graphql"
    assert posted["headers"]["x-api-key"] == "api-key"
    assert posted["json"]["variables"] == {
        "receiverId": "receiver-1",
        "payload": {
            "activityId": "activity-1",
            "message": "hello",
        },
    }
    assert posted["timeout"] == 10
