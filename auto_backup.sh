#!/usr/bin/env bash
# script to use on rpi

cd /home/ubuntu/project
sudo rsync -rv --exclude 'venv/' musicvideo_db/ admin@192.168.178.197:/volume1/musicvideo_db/