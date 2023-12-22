#Script to update and start the API service through flask
#This script will run automatically through a cronjob on boot

#Part 1 - Update API app folder
cd /home/erika/app/rpi1/
git pull https://github.com/erikashby/rpi1

#Part 2 - Start flask
#   activate the virtual enviornment
cd /home/erika/app/
. app/bin/activate

#   start the flask app
cd /home/erika/app/rpi1/
flask --app hello run --host=0.0.0.0