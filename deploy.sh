#!/bin/bash
# Default deployment script for Backend
# Deoploy to gcp
source env/bin/activate
pip install -r requirements.txt -t lib/
pip install -r requirements.txt
gcloud app deploy
rm -rf lib/
echo "Deployed..."