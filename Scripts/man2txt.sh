#!/bin/bash

if [ "$#" -ne 2 ]; then
    cat << EOF
Usage:
  $1 SECTION COMMAND
EOF
    exit 1
fi

if [ -f "${cmd}.md" ]; then
    echo "Arquivo de ajuda já encontrado para comando ${cmd}: <${cmd}.md>."
else
cat << EOF > ${cmd}.md
(${2}-${1})=

# ${$2}(${1})

\`\`\`
EOF
# Save a Unix manpage as plain text
# https://electrictoolbox.com/save-manpage-plain-text/
man $1 $2 | col -b >> "${2}.md"
echo \`\`\` >> "${2}.md"
fi
