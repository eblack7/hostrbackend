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
#python env/bin/pip install -r requirements-vendor.txt -t lib/

# Installing all dependencies to lib folder
#python env/bin/pip install -r requirements.txt -t lib/

# Collecting all Django default static files
#python manage.py collectstatic

# Setting up software to run db migrations on app engine
export SERVER_SOFTWARE='Google App Engine'
python manage.py migrate

# Upload app to gcloud
gcloud app deploy

# Removing lib folder
echo "Removing cached lib folder..."
rm -rf lib/

# Removing intermediate staticfiles folder
echo "Removing intermediate staticfiles folder..."
rm -rf staticfiles/

#Deployment confirmation
echo "Deployed to App Engine."
