#!/bin/bash

if [ $1 != "testing" ] && [ $1 != "production" ] ;
then
  echo env must be testing or production
  exit
fi

# aws ecr get-login
docker build -t chatter:$1 .;
docker tag chatter:$1 832531170141.dkr.ecr.us-east-2.amazonaws.com/chatter:$1;
docker push 832531170141.dkr.ecr.us-east-2.amazonaws.com/chatter:$1;

~/src/ecs-deploy/./ecs-deploy -c chatter-$1 -n chatter-$1-api -i 832531170141.dkr.ecr.us-east-2.amazonaws.com/chatter:$1;
