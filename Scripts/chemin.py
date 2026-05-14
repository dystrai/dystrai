#!/usr/bin/python3

#head -20 /etc/passwd | grep -Eo '(/[a-z]+)+' | sort -u | sed 's@/@ @2g; s@^/@/ @'

import pwd

from anytree import Node, RenderTree
from anytree.exporter import DotExporter


root = Node('/')

nodes = {
    '/': root
}


for user in pwd.getpwall()[:20]:

    for path in (user.pw_dir, user.pw_shell):

        if path == '/':
            continue

        current = '/'

        for part in path.split('/')[1:]:

            parent = nodes[current]

            if current == '/':
                current += part

            else:
                current += '/' + part

            if current not in nodes:

                nodes[current] = Node(
                    part,
                    parent=parent
                )


for pre, fill, node in RenderTree(root):
    print(f'{pre}{node.name}')


DotExporter(
    root,
    nodenamefunc=lambda node: node.name,
    nodeattrfunc=lambda node: 'shape=folder',
    options=["rankdir=BT;"]
).to_dotfile('/tmp/tree.dot')

