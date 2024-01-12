#!/bin/bash

rm -rf .aws-sam

sam build --template ./templates/root.yaml --profile admin@rr-ashurmatov-root
sam package --output-template-file ./templates/packaged-root.yaml --profile admin@rr-ashurmatov-root
sam deploy --template ./templates/packaged-root.yaml --stack-name aws-serverless-demo --profile admin@rr-ashurmatov-root --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND
