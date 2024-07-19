#!/bin/bash

if [[ ! -z "${CREATE_DB}" ]]; then 
  if [[ ${CREATE_DB} = 'true' ]]; then
    mongoimport -d embrapa -c users /localfiles/users.json --jsonArray
    mongoimport -d embrapa -c scrape_target /localfiles/targets.json --jsonArray
  fi
fi 

