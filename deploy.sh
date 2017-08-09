#!/bin/bash

if [ $1 != "testing" ] && [ $1 != "production" ] ;
then
  echo env must be testing or production
  exit
fi

docker build -t chatter:$1 .;
docker tag chatter:$1 832531170141.dkr.ecr.us-east-2.amazonaws.com/chatter:$1;
docker push 832531170141.dkr.ecr.us-east-2.amazonaws.com/chatter:$1;
ecs deploy chatter-$1 chatter-$1-api;
