import os


def lambda_handler(event, context):
    exported_topic_arn = os.environ.get("ExportedTopicArn")
    print(f"Topic ARN: {exported_topic_arn}")
