#!/bin/bash

# Passeio por todos os commits de um projeto

# O diretório de trabalho é um diretório de trabalho do Git?
# https://stackoverflow.com/questions/2180270/check-if-current-directory-is-a-git-repository
# https://stackoverflow.com/questions/876239/how-to-redirect-and-append-both-stdout-and-stderr-to-a-file-with-bash
if ! git rev-parse --is-inside-work-tree &> /dev/null; then
    echo "O diretório atual não é um diretório de trabalho do Git."
    exit 1
fi


# Um visualizador de diferenças está configurado?
#    Verificar: git config --global diff.tool
#    Sugestão para Debian/Ubuntu: 
#             sudo apt update
#             sudo apt install -y meld
#             git config --global diff.tool meld
#             git config --global alias.dt 'difftool -d'
# https://kparal.wordpress.com/2020/12/16/show-a-side-by-side-git-diff-on-any-commit-in-tig-using-meld/

# https://opensource.com/article/18/5/you-dont-know-bash-intro-bash-arrays
hashes=($(git log --reverse --pretty=oneline | awk '{print $1}'))

for h in ${hashes[@]}
    do
        git log $h..$h
        git checkout $h
        read -p "ENTER para continuar"
    done
