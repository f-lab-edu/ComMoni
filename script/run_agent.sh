#!/bin/bash


agent_home=/Users/kristoff/Desktop/ComMoni/agent

export PYTHONPATH=$agent_home

cd $agent_home
source ./venv/bin/activate

cd app
python main.py 
