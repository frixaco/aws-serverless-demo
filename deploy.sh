#!/bin/bash

rm -rf .aws-sam

sam build --template ./templates/root.yaml --profile admin@rr-ashurmatov-root
sam package --force-upload --output-template-file ./templates/packaged-root.yaml --profile admin@rr-ashurmatov-root
sam deploy --template ./templates/packaged-root.yaml --stack-name demo-1 --profile admin@rr-ashurmatov-root --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND