#!/bin/bash
set -x
set -e

virtualenv --python python3.12 env
source env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install -e .