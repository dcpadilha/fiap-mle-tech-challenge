#!/bin/bash

save_var() {
  if [ $? -eq 0 ]; then
    export $1=$2
    echo export $1=$2 >> ~/projects/fiap-mle-tech-challenge/cicd/scripts/env-vars.sh
  fi
}
export PROJECT=2mlet-phase1
export AWS_REGION=sa-east-1
export PROJECT=2mletphase1
export PROJECT=phase1-2mlet
export AWS_REGION=us-east-1=
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=488088354816
export MLET_VPC=vpc-0aa2ef51405ee8b76
export MLET_TARGET_GROUP_ARN=arn:aws:elasticloadbalancing:us-east-1:488088354816:targetgroup/mlet-tg/0cba3e6e4c401834
export MLET_LISTENER_ARN=arn:aws:elasticloadbalancing:us-east-1:488088354816:listener/app/mlet-prod-ALB/75521bcde2bda532/3b3e5f62f5d6d8f2
export MLET_LISTENER_RULE_ARN=arn:aws:elasticloadbalancing:us-east-1:488088354816:listener-rule/app/mlet-prod-ALB/75521bcde2bda532/3b3e5f62f5d6d8f2/3493106540eb0dc4
export MLET_REPO_URI=488088354816.dkr.ecr.us-east-1.amazonaws.com/fiap-mle-tech-challenge
export DB_REPO_URI=488088354816.dkr.ecr.us-east-1.amazonaws.com/embrapa-db
export CODEBUILD_ROLE_NAME=Cloud9-CodeBuild-Role-1721600903
export CODEBUILD_ROLE_ARN=arn:aws:iam::488088354816:role/Cloud9-CodeBuild-Role-1721600903
