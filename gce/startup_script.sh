#!/bin/bash
# Copyright Hostr LLC.
# 
# Default deployment startup script for GCE.

# Get PROJECTID from google metadata servers
PROJECTID=$(curl -s "http://metadata.google.internal/computeMetadata/v1/project/project-id" -H "Metadata-Flavor: Google")

# Installing logging monitor
# [START logging]
curl -s "https://storage.googleapis.com/signals-agents/logging/google-fluentd-install.sh" | bash
service google-fluentd restart &
# [END logging]

# Install dependencies from apt-get
apt-get update
apt-get install -yq \
    git build-essential supervisor python python-dev python-pip libffi-dev \
    libssl-dev

# Create a pythonapp user.
useradd -m -d /home/pythonapp pythonapp

# Update pip if its old
pip install --upgrade pip virtualenv

# Setting enviorment variable HOME for Git
export HOME=/root
git config --global credential.helper gcloud.sh
git clone "https://github.com/kirandasika98/hbackend.git"

# Install virtual env dependencies
virtualenv env/
env/pip install -r requirements.txt
