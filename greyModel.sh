#!/bin/bash
java -cp .:Jama-1.0.2.jar:py4j0.9.1.jar py4j/Grey py4j/IFilter &
sleep 1
python greyModel.py
