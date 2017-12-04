#!/bin/bash
set -evx

mkdir ~/.vivocore

# safety check
if [ ! -f ~/.vivocore/.vivo.conf ]; then
  cp share/vivo.conf.example ~/.vivocore/vivo.conf
fi
