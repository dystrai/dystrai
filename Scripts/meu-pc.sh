#!/bin/bash

PC="pc-${USER}"
CONT=$(lxc list -c n ${PC} --format=csv)
ARG1="$1"

if [ "${CONT}" == "" ]; then
    lxc launch ubuntu:20.04 $PC
fi

figlet $(echo $PC | tr '[a-z]' '[A-Z]') | lolcat

STATUS=$(lxc list -c s ${PC} --format=csv)

if [ "${STATUS}" == "STOPPED" ]; then
    lxc start $PC
fi

if [ "${ARG1}" == "grava" ]; then
  data=$(date +'%F %T')
  asciinema rec -i 2.5 -t "${PC}: ${data}" -c "lxc exec $PC bash"
else
  lxc exec $PC bash
fi

# vim: ts=2 sw=2 et ai
