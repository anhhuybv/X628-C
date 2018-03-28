#!/usr/bin/env bash
# install

#    python pullData.py &
#    python pullUser.py &
#    python view.py
export FLASK_APP=control.py
flask run --reload --debugger