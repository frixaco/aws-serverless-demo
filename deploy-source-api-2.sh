rm -rf .aws-sam

sam build --template ./templates/child2.yaml --profile admin@rr-ashurmatov-root
sam package --force-upload --output-template-file ./templates/packaged-child2.yaml --profile admin@rr-ashurmatov-root
sam deploy --template ./templates/packaged-child2.yaml \
 --stack-name demo-1-SourceApi2Stack-I9WUF1LKI3QK \
 --profile admin@rr-ashurmatov-root --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
 --parameter-overrides \
 DataSourceRole=arn:aws:iam::117349086557:role/demo-1-DataSourceRole-17AGTZRJ40GQD \
 SharedLayerArn=arn:aws:lambda:us-east-1:117349086557:layer:shared-layer:76 \
 FfmpegLayerArn=arn:aws:lambda:us-east-1:117349086557:layer:ffmpeg-layer:66 \
 MergedApiArn=arn:aws:appsync:us-east-1:117349086557:apis/zsdjl5mgyfaxdgpdvmrgpbbula
