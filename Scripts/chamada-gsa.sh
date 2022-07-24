#!/bin/sh

data=$(echo "$1" | awk '{print $2}')

echo "Chamada de ${data})"
cut -d: -f1 "$1" | sort -u | grep -Ev '^[0-9]' | nl
