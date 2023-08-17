#!/bin/bash

rm -rf .aws-sam
node schema-merger/index.js
sam build --template template-root.yaml --profile admin@rr-ashurmatov-root
sam package --force-upload --output-template-file packaged-template-root.yaml --profile admin@rr-ashurmatov-root
sam deploy --template packaged-template-root.yaml --stack-name demo-1 --profile admin@rr-ashurmatov-root --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND