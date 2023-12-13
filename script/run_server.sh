#!/bin/bash


server_home=/Users/kristoff/Desktop/ComMoni/server

export PYTHONPATH=$server_home

cd $server_home
source venv/bin/activate

python -m uvicorn app.main:app --reload --log-config app/log.ini 
