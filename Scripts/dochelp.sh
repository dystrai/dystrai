#!/bin/bash

# Document commands' help
# TODO: Check if a command is built-in or external

# Documenta a ajuda de comandos.
# A FAZER: Verificar se o comando é interno ou externo ao shell
#
# * Interno do bash: `help COMANDO`
# * Interno do zsh: `run-help COMANDO`
# * Externo: `COMANDO --help`


if [ ! "$#" -ge 1 ]; then
    cat << EOF
Usage:
  $1 COMMAND...
EOF
    exit 1
fi

for cmd in $@
do
if [ -f "${cmd}.md" ]; then
echo "Arquivo de ajuda já encontrado para comando ${cmd}: <${cmd}.md>."
continue
else
cat << EOF > ${cmd}.md
(${cmd})=

# ${cmd}

\`\`\`
EOF
${cmd} --help >> "${cmd}.md"
echo \`\`\` >> "${cmd}.md"
fi
done
