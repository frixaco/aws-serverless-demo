import aws_cdk as cdk

# from aws_cdk import cloudformation_include as cfn_inc
from aws_cdk import aws_appsync as appsync
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_s3 as s3
from constructs import Construct


class AsdCdkStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ffmpeg_layer = lambda_.LayerVersion(
            self,
            id="ffmpeg-layer",
            layer_version_name="ffmpeg-layer",
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_11],
            code=lambda_.Code.from_bucket(
                s3.Bucket.from_bucket_name(
                    self, "FfmpegLayerBucket", "frixaco-lambda-layers"
                ),
                "ffmpeg-layer.zip",
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )
        shared_layer = lambda_.LayerVersion(
            self,
            id="shared-layer",
            layer_version_name="shared-layer",
            code=lambda_.Code.from_asset(
                "./asd_cdk/lambda_functions/shared",
                bundling=cdk.BundlingOptions(
                    image=cdk.DockerImage.from_registry("python:3.11.1"),
                    command=[
                        "bash",
                        "-c",
                        "pip install --no-cache -r requirements.txt -t /asset-output && cp -au . /asset-output",
                    ],
                ),
            ),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_11],
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        endpoint1_lambda = lambda_.Function(
            self,
            id="endpoint1-lambda",
            function_name="endpoint1-lambda",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="app.lambda_handler",
            code=lambda_.Code.from_asset(
                "./asd_cdk/lambda_functions/endpoint1",
                bundling=cdk.BundlingOptions(
                    image=cdk.DockerImage.from_registry("python:3.11.1"),
                    command=[
                        "bash",
                        "-c",
                        "pip install --no-cache -r requirements.txt -t /asset-output && cp -au . /asset-output",
                    ],
                ),
            ),
            layers=[shared_layer],
        )

        endpoint2_lambda = lambda_.Function(
            self,
            id="endpoint2-lambda",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="app.lambda_handler",
            code=lambda_.Code.from_asset(
                "./asd_cdk/lambda_functions/endpoint2",
                bundling=cdk.BundlingOptions(
                    image=cdk.DockerImage.from_registry("python:3.11.1"),
                    command=[
                        "bash",
                        "-c",
                        "pip install --no-cache -r requirements.txt -t /asset-output && cp -au . /asset-output",
                    ],
                ),
            ),
            layers=[ffmpeg_layer, shared_layer],
        )

        endpoint3_lambda = lambda_.Function(
            self,
            id="endpoint3-lambda",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="app.lambda_handler",
            code=lambda_.Code.from_asset(
                "./asd_cdk/lambda_functions/endpoint3",
                bundling=cdk.BundlingOptions(
                    image=cdk.DockerImage.from_registry("python:3.11.1"),
                    command=[
                        "bash",
                        "-c",
                        "pip install --no-cache -r requirements.txt -t /asset-output && cp -au . /asset-output",
                    ],
                ),
            ),
            layers=[shared_layer],
        )

        source_api_1 = appsync.GraphqlApi(
            self,
            id="source-api-1",
            name="source-api-1",
            definition=appsync.Definition.from_schema(
                appsync.SchemaFile.from_asset(
                    "./asd_cdk/graphql_schemas/sourceApi1.graphql"
                )
            ),
        )
        endpoint1_lambda_ds = appsync.LambdaDataSource(
            self,
            id="endpoint1-lambda-ds",
            lambda_function=endpoint1_lambda,
            api=source_api_1,
        )
        appsync.Resolver(
            self,
            id="endpoint1-resolver",
            api=source_api_1,
            type_name="Query",
            field_name="endpoint1",
            data_source=endpoint1_lambda_ds,
            code=appsync.Code.from_asset(
                "./asd_cdk/graphql_unit_resolvers/base.js",
            ),
            runtime=appsync.FunctionRuntime.JS_1_0_0,
        )

        source_api_2 = appsync.GraphqlApi(
            self,
            id="source-api-2",
            name="source-api-2",
            definition=appsync.Definition.from_schema(
                appsync.SchemaFile.from_asset(
                    "./asd_cdk/graphql_schemas/sourceApi2.graphql"
                )
            ),
        )
        endpoint2_lambda_ds = appsync.LambdaDataSource(
            self,
            id="endpoint2-lambda-ds",
            lambda_function=endpoint2_lambda,
            api=source_api_2,
        )
        appsync.Resolver(
            self,
            id="endpoint2-resolver",
            api=source_api_2,
            type_name="Mutation",
            field_name="endpoint2",
            data_source=endpoint2_lambda_ds,
            code=appsync.Code.from_asset(
                "./asd_cdk/graphql_unit_resolvers/base.js",
            ),
            runtime=appsync.FunctionRuntime.JS_1_0_0,
        )
        endpoint3_lambda_ds = appsync.LambdaDataSource(
            self,
            id="endpoint3-lambda-ds",
            lambda_function=endpoint3_lambda,
            api=source_api_2,
        )
        appsync.Resolver(
            self,
            id="endpoint3-resolver",
            api=source_api_2,
            type_name="Mutation",
            field_name="endpoint3",
            data_source=endpoint3_lambda_ds,
            code=appsync.Code.from_asset(
                "./asd_cdk/graphql_unit_resolvers/base.js",
            ),
            runtime=appsync.FunctionRuntime.JS_1_0_0,
        )

        merged_api = appsync.GraphqlApi(
            self,
            id="merged-api",
            name="merged-api",
            definition=appsync.Definition.from_source_apis(
                source_apis=[
                    appsync.SourceApi(
                        source_api=source_api_1,
                        merge_type=appsync.MergeType.AUTO_MERGE,
                    ),
                    appsync.SourceApi(
                        source_api=source_api_2,
                        merge_type=appsync.MergeType.AUTO_MERGE,
                    ),
                ],
                merged_api_execution_role=iam.Role(
                    self,
                    id="merged-api-execution-role",
                    assumed_by=iam.ServicePrincipal("appsync.amazonaws.com"),
                    inline_policies={
                        "appsync": iam.PolicyDocument(
                            statements=[
                                iam.PolicyStatement(
                                    resources=["*"],
                                    actions=["appsync:*"],
                                )
                            ]
                        )
                    },
                ),
            ),
        )

        # merged_api_cw_role = iam.Role(
        #     self,
        #     "MergedApiCWRole",
        #     assumed_by=iam.ServicePrincipal("appsync.amazonaws.com"),
        # )
        # merged_api_cw_role.add_to_policy(
        #     iam.PolicyStatement(
        #         resources=[
        #             f"arn:aws:logs:{cdk.Stack.of(self).region}:{cdk.Stack.of(self).account}:*"
        #         ],
        #         actions=[
        #             "logs:CreateLogGroup",
        #             "logs:CreateLogStream",
        #             "logs:PutLogEvents",
        #         ],
        #     )
        # )

        cdk.CfnOutput(
            self,
            "API URL",
            value=merged_api.graphql_url,
            description="Merged API URL",
        )
        cdk.CfnOutput(
            self,
            "API KEY",
            value=merged_api.api_key,
            description="Merged API KEY",
        )
