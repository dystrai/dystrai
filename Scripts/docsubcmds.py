# coding: utf-8
subcomandos = '''   clone             Clone a repository into a new directory
   init              Create an empty Git repository or reinitialize an existing one
   add               Add file contents to the index
   mv                Move or rename a file, a directory, or a symlink
   restore           Restore working tree files
   rm                Remove files from the working tree and from the index
   sparse-checkout   Initialize and modify the sparse-checkout
   bisect            Use binary search to find the commit that introduced a bug
   diff              Show changes between commits, commit and working tree, etc
   grep              Print lines matching a pattern
   log               Show commit logs
   show              Show various types of objects
   status            Show the working tree status
   branch            List, create, or delete branches
   commit            Record changes to the repository
   merge             Join two or more development histories together
   rebase            Reapply commits on top of another base tip
   reset             Reset current HEAD to the specified state
   switch            Switch branches
   tag               Create, list, delete or verify a tag object signed with GPG
   fetch             Download objects and refs from another repository
   pull              Fetch from and integrate with another repository or a local branch
   push              Update remote refs along with associated objects'''.splitlines
cmd_descs = '''   clone             Clone a repository into a new directory
   init              Create an empty Git repository or reinitialize an existing one
   add               Add file contents to the index
   mv                Move or rename a file, a directory, or a symlink
   restore           Restore working tree files
   rm                Remove files from the working tree and from the index
   sparse-checkout   Initialize and modify the sparse-checkout
   bisect            Use binary search to find the commit that introduced a bug
   diff              Show changes between commits, commit and working tree, etc
   grep              Print lines matching a pattern
   log               Show commit logs
   show              Show various types of objects
   status            Show the working tree status
   branch            List, create, or delete branches
   commit            Record changes to the repository
   merge             Join two or more development histories together
   rebase            Reapply commits on top of another base tip
   reset             Reset current HEAD to the specified state
   switch            Switch branches
   tag               Create, list, delete or verify a tag object signed with GPG
   fetch             Download objects and refs from another repository
   pull              Fetch from and integrate with another repository or a local branch
   push              Update remote refs along with associated objects'''.splitlines
cmd_descs = '''   clone             Clone a repository into a new directory
   init              Create an empty Git repository or reinitialize an existing one
   add               Add file contents to the index
   mv                Move or rename a file, a directory, or a symlink
   restore           Restore working tree files
   rm                Remove files from the working tree and from the index
   sparse-checkout   Initialize and modify the sparse-checkout
   bisect            Use binary search to find the commit that introduced a bug
   diff              Show changes between commits, commit and working tree, etc
   grep              Print lines matching a pattern
   log               Show commit logs
   show              Show various types of objects
   status            Show the working tree status
   branch            List, create, or delete branches
   commit            Record changes to the repository
   merge             Join two or more development histories together
   rebase            Reapply commits on top of another base tip
   reset             Reset current HEAD to the specified state
   switch            Switch branches
   tag               Create, list, delete or verify a tag object signed with GPG
   fetch             Download objects and refs from another repository
   pull              Fetch from and integrate with another repository or a local branch
   push              Update remote refs along with associated objects'''.splitlines()
cmd_descs[0]
cmd_descs[0].split()
cmd_descs[0].split(maxsplit=1)
desc_cmd = {}
desc_cmd = {}
for cmd_desc in cmd_descs:
    cmd,desc = cmd_desc.split(maxsplit=1)
    desc_cmd = {cmd, desc}
    
desc_cmd
desc_cmd = {}
for cmd_desc in cmd_descs:
    cmd,desc = cmd_desc.split(maxsplit=1)
    desc_cmd[cmd] = desc
    
    
desc_cmd
!pwd
cd git/
import os
desc_cmd
for cmd,desc in desc_cmd.items():
    print(cmd, desc)
    
for cmd,desc in desc_cmd.items():
    print(cmd, '|', desc)
    
    
for cmd,desc in desc_cmd.items():
    os.mkdir(cmd)
    with open(f'{cmd}/index.md', 'w', encoding='utf-8') as indice:
        indice.write('''(git-cmd)=
        
# git {cmd}

{desc}
''')

    
    
import subprocess
cmd_help = 'git {cmd} --help'
processo = subprocess.Popen(cmd_help, shell=True, stdout=subprocess.PIPE)
cmd
cmd_help = f'git {cmd} --help'
processo = subprocess.Popen(cmd_help, shell=True, stdout=subprocess.PIPE)
saida_processo = processo.stdout.read()
saida_processo
%hist
for cmd,desc in desc_cmd.items():
    os.mkdir(cmd)
    cmd_help = f'git {cmd} --help'
    processo = subprocess.Popen(cmd_help, shell=True, stdout=subprocess.PIPE)
    saida_processo = processo.stdout.read()
    with open(f'{cmd}/index.md', 'w', encoding='utf-8') as indice:
        indice.write('''(git-cmd)=
        
# git {cmd}

{desc}

## Ajuda do comando

O texto abaixo é uma tradução com eventual reformatação da saída do comando `git {cmd} --help`

```
{saida_processo}
```
''')


    
    
for cmd,desc in desc_cmd.items():
    os.makedirs(cmd)
    cmd_help = f'git {cmd} --help'
    processo = subprocess.Popen(cmd_help, shell=True, stdout=subprocess.PIPE)
    saida_processo = processo.stdout.read()
    with open(f'{cmd}/index.md', 'w', encoding='utf-8') as indice:
        indice.write('''(git-cmd)=
        
# git {cmd}

{desc}

## Ajuda do comando

O texto abaixo é uma tradução com eventual reformatação da saída do comando `git {cmd} --help`

```
{saida_processo}
```
''')


    
    
for cmd,desc in desc_cmd.items():
    #os.mkdir(cmd)
    cmd_help = f'git {cmd} --help'
    processo = subprocess.Popen(cmd_help, shell=True, stdout=subprocess.PIPE)
    saida_processo = processo.stdout.read()
    with open(f'{cmd}/index.md', 'w', encoding='utf-8') as indice:
        indice.write('''(git-cmd)=
        
# git {cmd}

{desc}

## Ajuda do comando

O texto abaixo é uma tradução com eventual reformatação da saída do comando `git {cmd} --help`

```
{saida_processo}
```
''')


    
    
