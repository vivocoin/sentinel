#!/bin/bash
set -evx

mkdir ~/.desirecore

# safety check
if [ ! -f ~/.desirecore/.desire.conf ]; then
  cp share/desire.conf.example ~/.desirecore/desire.conf
fi
