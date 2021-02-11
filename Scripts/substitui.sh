#!/bin/bash

if [ "$#" -ne 1 ]; then
    cat << EOF
Usage:
  $1 DESTINATION
EOF
    exit 1
fi

DEST=$1
if ! [ -d "${DEST}" ]; then
    echo "ERROR: Destination not found (${DEST})."
    exit 2
fi

for f in * 
do
    dest_f=${DEST}/${f}
    if ! [ -d "${dest_f}" ] && ! [ -f "${dest_f}" ]; then
        echo "WARNING: File or directory not found on destination (${dest_f})."
    fi
    rm -rf ${DEST}/$f; mv -v $f ${DEST} ; 
done
