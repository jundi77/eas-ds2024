#!/bin/bash

# I use this a lot to start docker desktop service,
# since i disabled graphical.target and
# use multi-user.target and cannot easily launch docker desktop via GUI
systemctl start --user docker-desktop