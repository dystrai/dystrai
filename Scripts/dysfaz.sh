#!/bin/bash

# Dependências: git e meld
# No Debian/Ubuntu: sudo apt install -y git meld

# Passeio por todos os commits de um projeto
# A fazer:
#    Verificar: git config --global diff.tool
#    Sugerir: git config --global diff.tool meld
#             git config --global alias.dt 'difftool -d'
# https://kparal.wordpress.com/2020/12/16/show-a-side-by-side-git-diff-on-any-commit-in-tig-using-meld/

hashes=($(git log --reverse --pretty=oneline | awk '{print $1}'))

hashes_len=${#hashes[@]}

for i in $(seq 0 $(($hashes_len-2)))
    do
        clear
        echo "Comparação $((i+1)) de ${hashes_len}"
        echo
        git --no-pager log ${hashes[i]}..${hashes[$((i+1))]}
        # https://stackoverflow.com/questions/2006032/view-differences-of-branches-with-meld
        git difftool -d ${hashes[i]}..${hashes[$((i+1))]}
    done
