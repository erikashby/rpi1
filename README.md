# rpi1 Documentation
Adding a test line.
This is the documentation for how the RPI1 is setup

Device Description
Raspberry Pi 5, 8GB RAM

Operating System: 32 Bit default "Raspberry PI OS" (Used Raspberry Pi Imager tool)

Hostname: ashbypi-rpi1

Main account: erika
PwdHint: As**0

Folder structure

main applications /home/erika/app/rpi1

Setup Activity:
- Confirmed RPI was updated
    - sudo app-get update
    - sudo apt-get upgrade

- Established Remote access
    - SSH - On by default from OS setting
    - RDP using instructions from https://www.youtube.com/watch?v=o-iucAC6PaA&t=192s&ab_channel=UnboxingTomorrow
        Commands:
            sudo apt-get remove xrdp vnc4server tightvncserver
            sudo apt-get install tightvncserver
            sudo apt-get install xrdp
    - Tested command line SSH, and RDP terminal

- setup git folder
    - from /home/erika/app
    - git clone "http://github.com/erikashby/rpi1"

    - tested git folder
    - created this README.md
    - from /home/erika/app/rpi1
    - git pull "https://github.com/erikashby/rpi1"


- Installed Flask
    - made sure there was a virtual enviornment
    - from /home/erika/app
    -   sudo apt install python3-venv  << to install virtual enviornment >>
    -    python3 -m venv app << to create the virtual enviornment called app>>
    -   . app/bin/activate  << to activate the virtual enviornment >>

    - Installed flask
        pip install Flask

    - Tested flask
        - added hello.py (see file) and updated raspberry pi
        - from /home/erika/app/rpi1
        - flask --app hello run --host=0.0.0.0

- Added script to auto-update pi and launch flask
    - Added start_api.sh
    - Added update_api.sh 
    - Updated /app/rpi1/ from github
    - Added cron job to start on reboot
        - sudo crontab -e
        - @reboot sh /home/erika/app/rpi1/start_api.sh
    - Added cron job to start on reboot for erika
        - crontab -e
        - @reboot sh /home/erika/app/rpi1/update_api.sh

    - Rebooted






