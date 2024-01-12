#!/bin/bash

rm -rf .aws-sam

sam build --template ./templates/another-root.yaml --profile admin@rr-ashurmatov-root
sam package --output-template-file ./templates/packaged-another-root.yaml --profile admin@rr-ashurmatov-root
sam deploy --template ./templates/packaged-another-root.yaml --stack-name another-aws-serverless-demo --profile admin@rr-ashurmatov-root --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND
