import utilities


def main(event):
    identity = event.get("identity") or {}
    arguments = event.get("arguments") or {}
    include_debug = (arguments.get("input") or {}).get("includeDebug", False)

    user_id = utilities.identity_user_id(identity)
    response = {
        "userId": user_id,
        "source": utilities.demo_source_name("user-api"),
    }

    if include_debug:
        response["debug"] = f"identity keys: {', '.join(sorted(identity.keys()))}"

    return response


def lambda_handler(event, context):
    print("event:", event)
    response = main(event)
    print("response:", response)
    return response
