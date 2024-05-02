#!/bin/bash

ls /packages/*.whl | xargs --verbose -I FILE pip install FILE &> /dev/null;

python main.py