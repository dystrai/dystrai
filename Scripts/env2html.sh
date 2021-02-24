#!/bin/sh


echo "Content-type: text/html;charset=utf-8"
echo

pg_header="# Variáveis de ambiente"

tb_header=$(cat << FIM
| Variável | Valor |
| -------- | ----- |
FIM
)

tb_body=$(env | sed 's/.*/|&|/;s/=/|/')

cat << EOF | pandoc -f gfm -t html -
$pg_header

$tb_header
$tb_body
EOF

