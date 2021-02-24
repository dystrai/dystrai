#!/bin/sh

# Adaptation from:
# - UNIX command output in csv format:
# Available in:
# - <https://www.unix.com/shell-programming-and-scripting/232553-unix-command-output-csv-format.html>

LANG= df -h | sed -e 's/[ ]\+/,/g' -e 's/Mounted,on/Mounted on/'