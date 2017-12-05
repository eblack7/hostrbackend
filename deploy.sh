#!/bin/bash
# Default deployment script for Backend
# Deoploy to gcp

# Activate virtual env
source env/bin/activate
# Installing all vendor packages to lib folder
pip install -r requirements.txt -t lib/
# Installing all dependencies to lib folder
pip install -r requirements.txt -t lib/
# Upload app to gcloud
gcloud app deploy
# Removing lib folder
rm -rf lib/
#Deployment confirmation
echo "Deployed..."
