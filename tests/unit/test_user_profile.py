from user_profile import app


def test_current_user_uses_cognito_sub():
    response = app.lambda_handler(
        {
            "identity": {"sub": "user-123", "username": "ignored"},
            "arguments": {"input": {"includeDebug": True}},
        },
        None,
    )

    assert response["userId"] == "user-123"
    assert response["source"] == "aws-serverless-demo:user-api"
    assert response["debug"] == "identity keys: sub, username"


def test_current_user_falls_back_for_api_key_calls():
    response = app.lambda_handler({"identity": {}, "arguments": {}}, None)

    assert response["userId"] == "anonymous-demo-user"
