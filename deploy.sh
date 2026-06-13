#!/usr/bin/env bash
set -euo pipefail

PROJECT_NAME="${PROJECT_NAME:-aws-serverless-demo}"
STACK_NAME="${STACK_NAME:-aws-serverless-demo}"
REGION="${AWS_REGION:-us-east-1}"
PROFILE_ARGS=()

if [[ -n "${AWS_PROFILE:-}" ]]; then
  PROFILE_ARGS=(--profile "${AWS_PROFILE}")
fi

if [[ -z "${COGNITO_USER_POOL_ID:-}" ]]; then
  echo "COGNITO_USER_POOL_ID is required" >&2
  exit 1
fi

sam build \
  --template ./templates/root.yaml \
  "${PROFILE_ARGS[@]}"

sam package \
  --output-template-file ./templates/packaged-root.yaml \
  --region "${REGION}" \
  "${PROFILE_ARGS[@]}"

sam deploy \
  --template ./templates/packaged-root.yaml \
  --stack-name "${STACK_NAME}" \
  --region "${REGION}" \
  --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
  --parameter-overrides \
    ProjectName="${PROJECT_NAME}" \
    CognitoUserPoolId="${COGNITO_USER_POOL_ID}" \
  "${PROFILE_ARGS[@]}"
