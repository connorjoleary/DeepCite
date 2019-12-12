#!/bin/bash
./helper.sh &
echo starting server
coverage run app.py
coverage report
cd ..