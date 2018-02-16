#!/usr/bin/env bash
# a script to start movieDB on RPi

# go to proper directory
cd /home/ubuntu/project/musicvideo_db/

# activate virt env for python
. /home/ubuntu/project/musicvideo_db/venv/bin/activate

# run $FLASK_APP, accesable from all IPs
flask run --host=0.0.0.0

