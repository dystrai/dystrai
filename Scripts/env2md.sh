#!/bin/sh

if ! [ "$1" == "-n" ]; then
    echo "Content-type: text/markdown;charset=utf-8"
    echo
fi

cat << FIM
# Variáveis de ambiente

| Variável | Valor |
| -------- | ----- |
FIM

env | sed 's/.*/|&|/;s/=/|/'
