#!/bin/bash
./helper.sh &
echo starting server
coverage run main.py
coverage report
cd ..