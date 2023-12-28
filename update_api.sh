#!/bin/bash

# GitHub repository URL
github_repo="https://github.com/erikashby/zero2"

# Directory where you want to clone or pull the repository
local_directory="/home/erika/app/zero2"

# Ensure the local directory exists
if [ ! -d "$local_directory" ]; then
  mkdir -p "$local_directory"
fi

# Move to the local directory
cd "$local_directory" || exit

# Check if the directory is a Git repository
if [ -d ".git" ]; then
  # If it is a Git repository, perform a pull
  git pull origin main
else
  # If it is not a Git repository, perform a clone
  git clone "$github_repo" .
fi

# Optionally, you can add more commands or actions here after pulling/cloning

echo "Script executed successfully!"
