# Setup

1. Create a bash function to help handling environment variables.

This function will help you to keep track of your variables ensuring that they will be recreated when you log back in.


```
cat <<EoF > ~/env-vars.sh
#!/bin/bash

save_var() {
  if [ \$? -eq 0 ]; then
    export \$1=\$2
    echo export \$1=\$2 >> ~/env-vars.sh
  fi
}
EoF
chmod +x ~/env-vars.sh
source ~/env-vars.sh
echo "[[ -s ~/env-vars.sh ]] && source ~/env-vars.sh" >> ~/.bash_profile

```

Define the project name

```
save_var PROJECT 2mletphase1
```

2. Install AWS Command Line Interface (awscli)

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

 1. In order to use the new Instance Metadata (IMDSv2) you now have to create a token to be added to the GET/PUT request's header

 ```
 TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
 ```

 2. For ease of use, here is a simple bash function to refresh the token whenever needed.

 ```
 cat <<EoF > ~/token.sh
 #!/bin/bash

refresh_token() {
  TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
}
EoF
chmod +x ~/token.sh
echo "[[ -s ~/token.sh ]] && source ~/token.sh" >> ~/.bash_profile
 ```

3. Define the default AWS region to be used

If you are running this lab through Cloud9 you can get the region from the Cloud9 EC2 metadata, otherwise, manually specify the desired region.
For completeness sake, we're going to use North Virginia (us-east-1) as the default region.

 1. Using Cloud9

```
save_var AWS_REGION $(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" 169.254.169.254/latest/dynamic/instance-identity/document | jq -r .region)
aws configure set default.region ${AWS_REGION}
aws configure get default.region

```

 2. Using a fixed region

 ```
save_var AWS_REGION us-east-1
aws configure set default.region ${AWS_REGION}
aws configure get default.region

```

4. Disable AWS CLI client-side pager

```
aws configure set default.cli_pager ''
```

5. Enable Cloudwatch Container Insights


```
aws ecs put-account-setting-default --name containerInsights --value enabled

aws ecs list-account-settings --effective-settings --name containerInsights

```

```
aws iam get-role --role-name "AWSServiceRoleForElasticLoadBalancing" || aws iam create-service-linked-role --aws-service-name "elasticloadbalancing.amazonaws.com"
aws iam get-role --role-name "AWSServiceRoleForECS" || aws iam create-service-linked-role --aws-service-name "ecs.amazonaws.com"
```

```
cd ~/projects/fiap-mle-tech-challenge/cicd/cloudformation/ecs-cluster
aws cloudformation deploy \
  --stack-name ${PROJECT} \
  --template-file build-infra.yaml \
  --parameter-overrides "EnvironmentName=${PROJECT}-prod" \
  --capabilities CAPABILITY_IAM &
```

```
save_var IMAGE_REPO_URI $( \
    aws ecr create-repository \
        --repository-name ${PROJECT} \
        --query repository.repositoryUri \
        --output text \
)
echo Repo URI: $IMAGE_REPO_URI
```

```
aws logs create-log-group --log-group-name /ecs/fiap-mle-tech-challenge
aws logs create-log-group --log-group-name /ecs/embrapa-db
```

```
cd cicd/cloudformation
envsubst < task-definition-template.json > task-definition.json
```

```
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

```
save_var MLET_VPC $( \
  aws cloudformation describe-stacks \
  --stack-name mlet-cluster \
  --query "Stacks[0].Outputs[?OutputKey == 'VpcId'].OutputValue" \
  --output text \
)
save_var MLET_TARGET_GROUP_ARN $( \
  aws elbv2 create-target-group \
  --name mlet-tg \
  --port 8000 \
  --protocol HTTP \
  --health-check-path /ping \
  --health-check-timeout-seconds 3 \
  --health-check-interval-seconds 5 \
  --healthy-threshold-count 2 \
  --target-type instance \
  --vpc-id $MLET_VPC \
  --query "TargetGroups[0].TargetGroupArn" \
  --output text \
)
aws elbv2 modify-target-group-attributes \
  --target-group-arn $MLET_TARGET_GROUP_ARN \
  --attributes "Key=deregistration_delay.timeout_seconds,Value=5"
```

```
cat <<EoF >conditions-pattern.json
[
    {
        "Field": "path-pattern",
        "PathPatternConfig": {
            "Values": ["/mlet/*"]
        }
    }
]
EoF
cat <<EoF >actions.json
[
    {
        "Type": "forward",
        "ForwardConfig": {
            "TargetGroups": [ { "TargetGroupArn": "${MLET_TARGET_GROUP_ARN}" } ]
        }
    }
]
EoF
save_var MLET_LISTENER_ARN $( \
  aws cloudformation describe-stacks \
  --stack-name mlet-cluster \
  --query "Stacks[0].Outputs[?OutputKey == 'PublicListener'].OutputValue" \
  --output text \
)
save_var MLET_LISTENER_RULE_ARN $( \
    aws elbv2 create-rule \
    --listener-arn $MLET_LISTENER_ARN \
    --priority 10 \
    --conditions file://conditions-pattern.json \
    --actions file://actions.json \
    --query "Rules[0].RuleArn" \
    --output text \
)

```

```
envsubst \
  < service-mlet.json.template \
  > service-mlet.json
cat service-mlet.json
```

```
aws ecs create-service --cli-input-json file://service-mlet.json
```

```
save_var MLET_REPO_URI $( \
    aws ecr create-repository \
        --repository-name fiap-mle-tech-challenge \
        --query repository.repositoryUri \
        --output text \
)
echo Repo URI: $MLET_REPO_URI

save_var DB_REPO_URI $( \
    aws ecr create-repository \
        --repository-name embrapa-db \
        --query repository.repositoryUri \
        --output text \
)
echo Repo URI: $DB_REPO_URI
```

```
sed -i "s%<MLET_REPO_URI>%$MLET_REPO_URI%" buildspec.yml

sed -i "s%<DB_REPO_URI>%$DB_REPO_URI%" buildspec.yml
```