#!/bin/sh

# Allow OAUTH over https for local testing.
export OAUTHLIB_INSECURE_TRANSPORT=1

# Name of module for flask to run.
export FLASK_APP=api.py

python -m flask run
