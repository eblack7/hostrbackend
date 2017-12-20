#!/bin/bash
# Default deployment script for Backend
# Deoploy to gcp

# Check if lib directory exists
LIBDIR="./lib/"
if [ ! -d "$LIBDIR" ]; then
    mkdir lib
fi

# Activate virtual env
source env/bin/activate

# Installing all vendor packages to lib folder
python env/bin/pip install -r requirements-vendor.txt -t lib/

# Installing all dependencies to lib folder
python env/bin/pip install -r requirements.txt -t lib/

# Collecting all Django default static files
python manage.py collectstatic

# Upload app to gcloud
gcloud app deploy

# Removing lib folder
rm -rf lib/
#Deployment confirmation
echo "Deployed..."
