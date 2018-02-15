#!/usr/bin/env bash
# a script to start movieDB

cd /home/ubuntu/project/musicvideo_db/
. /home/ubuntu/project/musicvideo_db/venv/bin/activate
#echo $FLASK_APP
flask run --host=0.0.0.0

