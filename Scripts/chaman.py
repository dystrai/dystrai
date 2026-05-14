#!/usr/bin/env python3

import os
import sys

from getpass import getuser
from pathlib import Path

from anytree import Node, RenderTree
from anytree.exporter import DotExporter


root = Node(
    '/',
    kind='directory'
)

nodes = {
    '/': root
}


def get_shape(node):

    shapes = {
        'directory': 'folder',
        'file': 'note',
        'executable': 'box3d',
        'symlink': 'oval',
    }

    return shapes.get(node.kind, 'ellipse')


def classify(path: Path) -> str:

    try:

        if path.is_symlink():
            return 'symlink'

        if path.is_dir():
            return 'directory'

        if path.is_file():

            if path.stat().st_mode & 0o111:
                return 'executable'

            return 'file'

    except (
        FileNotFoundError,
        PermissionError,
        OSError
    ):
        pass

    return 'file'


for line in sys.stdin:

    path_str = line.strip()

    if not path_str.startswith('/'):
        continue

    path = Path(path_str)

    current = '/'

    parts = path.parts[1:]

    for i, part in enumerate(parts):

        parent = nodes[current]

        current = str(Path(current) / part)

        is_last = (i == len(parts) - 1)

        #
        # Somente o último elemento precisa
        # ser classificado corretamente.
        #

        kind = (
            classify(Path(current))
            if is_last
            else 'directory'
        )

        if current not in nodes:

            nodes[current] = Node(
                part,
                parent=parent,
                kind=kind
            )


#
# TREE VIEW
#

for pre, fill, node in RenderTree(root):

    print(
        f'{pre}{node.name} '
        f'[{node.kind}]'
    )


#
# DOT EXPORT
#

dst_file = f"/tmp/tree-{getuser()}-{os.getpid()}.dot"

DotExporter(
    root,

    nodenamefunc=lambda node: (
        node.name
    ),

    nodeattrfunc=lambda node: (
        f'shape={get_shape(node)}'
    ),

    options=[
        'rankdir=TB'
    ]

).to_dotfile(dst_file)

print(f'Arquivo gerado: {dst_file}')
