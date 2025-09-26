#!/bin/bash

if [ "$#" -ne 2 ]; then
    cat << EOF
Usage:
  $0 SEÇÃO PÁGINA
EOF
    exit 1
fi

SECTION="${1}"
PAGE="${2}"
DOC_ID="${PAGE}-${SECTION}"

if [[ -f "${DOC_ID}.md" ]]; then
    echo "Arquivo de ajuda já encontrado para comando ${cmd}: <${cmd}.md>."
else
    cat << EOF > "${DOC_ID}.md
(${DOC_ID})=

# ${$2}(${1})

\`\`\`
EOF
# Save a Unix manpage as plain text
# https://electrictoolbox.com/save-manpage-plain-text/
man $1 $2 | col -b >> "${2}.md"
echo \`\`\` >> "${2}.md"
fi
