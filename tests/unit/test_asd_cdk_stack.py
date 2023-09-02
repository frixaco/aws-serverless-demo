import aws_cdk as core
import aws_cdk.assertions as assertions

from asd_cdk.asd_cdk_stack import AsdCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in asd_cdk/asd_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AsdCdkStack(app, "asd-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
