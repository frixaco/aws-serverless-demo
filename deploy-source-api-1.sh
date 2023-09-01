rm -rf .aws-sam

sam build --template ./templates/child1.yaml --profile admin@rr-ashurmatov-root
sam package --force-upload --output-template-file ./templates/packaged-child1.yaml --profile admin@rr-ashurmatov-root
sam deploy --template ./templates/packaged-child1.yaml \
 --stack-name demo-1-SourceApi1Stack-52B7GQCK5SI1 \
 --profile admin@rr-ashurmatov-root --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
 --parameter-overrides \
 LambdaExecutionRole=arn:aws:iam::117349086557:role/demo-1-LambdaExecutionRole-17AGTZRJ40GQD \
 SharedLayerArn=arn:aws:lambda:us-east-1:117349086557:layer:shared-layer:76 \
 MergedApiArn=arn:aws:appsync:us-east-1:117349086557:apis/zsdjl5mgyfaxdgpdvmrgpbbula
