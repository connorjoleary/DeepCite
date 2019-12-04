#!/bin/bash
./help_test.sh &
cd nlp
echo starting server
coverage run app.py
coverage report
cd ..