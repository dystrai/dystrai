#!/bin/sh

cat << FIM
| Variavel | Valor |
| -------- | ----- |
FIM

env | sed 's/.*/|&|/;s/=/|/'
