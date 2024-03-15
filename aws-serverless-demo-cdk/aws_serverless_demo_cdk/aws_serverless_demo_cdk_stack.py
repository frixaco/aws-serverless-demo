from os import path

from aws_cdk import Stack
from aws_cdk import aws_appsync
from aws_cdk import aws_appsync as appsync
from aws_cdk import aws_lambda as lambda_  # Duration,; aws_sqs as sqs,
from constructs import Construct


class AwsServerlessDemoCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "AwsServerlessDemoCdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        api_1 = appsync.GraphqlApi(
            self,
            "source_api_1",
            name="source_api_1",
            definition=appsync.Definition.from_file(
                path.join(__dirname, "graphql_schemas/sourceApi1.graphql")
            ),
        )
        endpoint1 = lambda_.Function(
            self,
            "endpoint1",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset("api/endpoint1"),
        )
        endpoint1.add_permission(
            "endpoint1_invoke_permission",
        )
        endpoint1_data_source = api_1.add_lambda_data_source(
            "endpoint1_data_source", lambda_function=endpoint1
        )
        endpoint1_data_source.create_resolver(
            "endpoint1_resolver",
            type_name="Mutation",
            field_name="endpoint1",
            code=appsync.Code.from_asset(path.join(__dirname, "lambdas/resolver.js")),
        )

        source_api_1 = appsync.SourceApi(
            source_api=api_1, merge_type=appsync.MergeType.AUTO_MERGE
        )

        merged_graphql_api = appsync.GraphqlApi(
            self,
            "merged_api",
            name="merged_api",
            definition=appsync.Definition.from_source_apis(source_apis=[source_api_1]),
        )
