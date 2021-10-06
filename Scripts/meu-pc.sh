#!/bin/bash

PC="pc-${USER}"
CONT=$(lxc list -c n ${PC} --format=csv)

if [ "${CONT}" == "" ]; then
    lxc launch images:debian/11 $PC
fi

figlet $(echo $PC | tr '[a-z]' '[A-Z]') | lolcat

data=$(date +'%F %T')

lxc start $PC
asciinema rec -i 2.5 -t "${PC}: ${data}" -c "lxc exec $PC bash"
