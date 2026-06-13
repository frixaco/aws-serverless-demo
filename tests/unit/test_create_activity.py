from create_activity import app


def test_create_activity_publishes_notification(monkeypatch):
    published = {}

    def fake_notify_subscribers(*, topic_arn, receiver_id, payload):
        published["topic_arn"] = topic_arn
        published["receiver_id"] = receiver_id
        published["payload"] = payload
        return {"MessageId": "message-1"}

    monkeypatch.setenv("SNS_NOTIFICATION_TOPIC_ARN", "arn:aws:sns:test")
    monkeypatch.setattr(app.utilities, "notify_subscribers", fake_notify_subscribers)

    response = app.lambda_handler(
        {
            "arguments": {
                "input": {
                    "message": "New booking request",
                    "receiverId": "receiver-1",
                }
            }
        },
        None,
    )

    assert response["message"] == "New booking request"
    assert response["receiverId"] == "receiver-1"
    assert response["notified"] is True
    assert published == {
        "topic_arn": "arn:aws:sns:test",
        "receiver_id": "receiver-1",
        "payload": {
            "activityId": response["activityId"],
            "message": "New booking request",
        },
    }
