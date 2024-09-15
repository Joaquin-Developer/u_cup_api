#!/bin/bash

export ENVIRONMENT="production"
source /home/jparilla/envs/env/bin/activate
uvicorn main:app --port 8000
