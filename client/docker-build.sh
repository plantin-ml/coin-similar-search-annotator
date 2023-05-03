#!/bin/bash

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 414252687335.dkr.ecr.us-east-1.amazonaws.com

TAG=client_02
NAME=similar-search-annotator

docker build -t $NAME:$TAG .

docker tag $NAME:$TAG 414252687335.dkr.ecr.us-east-1.amazonaws.com/$NAME:$TAG

docker push 414252687335.dkr.ecr.us-east-1.amazonaws.com/$NAME:$TAG

echo 'Success'

echo 414252687335.dkr.ecr.us-east-1.amazonaws.com/$NAME:$TAG