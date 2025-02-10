#!/bin/bash

echo "Waiting for MongoDB to be ready..."
until mongo --host mongodb --username admin --password password --authenticationDatabase admin --eval "print('MongoDB is up and running!')" > /dev/null 2>&1
do
  sleep 2
done

echo "MongoDB is up, starting Flask..."
flask run --host=0.0.0.0 --port=5000
