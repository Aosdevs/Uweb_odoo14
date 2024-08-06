#!/bin/bash
docker login

cd ./14.0

docker-compose up -d

docker ps