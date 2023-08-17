rm -rf .aws-sam

aws appsync get-graphql-schema --api-id xznuaotukff6xo2737cgk22dpm --output graphql > remote-unified-schema.graphql

node schema-merger/index.js

aws appsync update-graphql-schema --api-id xznuaotukff6xo2737cgk22dpm --definition unified-schema.graphql


sam build --template template-endpoint1.yaml --profile admin@rr-ashurmatov-root
sam package --force-upload --output-template-file packaged-template-endpoint1.yaml --profile admin@rr-ashurmatov-root
sam deploy --template packaged-template-endpoint1.yaml --stack-name demo-1-Endpoint1Stack-1V3N3LFGZA78R --profile admin@rr-ashurmatov-root --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND --parameter-overrides Role=arn:aws:iam::117349086557:role/demo-1-LambdaExecutionRole-RBHGZMGNG278 SharedLayerArn=arn:aws:lambda:us-east-1:117349086557:layer:shared-layer:33 FfmpegLayerArn=arn:aws:lambda:us-east-1:117349086557:layer:ffmpeg-layer:23 DemoApiId=xznuaotukff6xo2737cgk22dpm
