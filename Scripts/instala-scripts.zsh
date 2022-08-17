#!/usr/bin/env zsh

instala_local() {
    setopt extendedglob

    BASENAME="$1"

    for script (^$BASENAME)      
       ln -sv "${PWD}/${script}" ~/.local/bin/${script%.*}

}

DEST=~/.local/bin
BASENAME="${0##*/}"

mkdir -pv "${DEST}" && instala_local "${BASENAME}"