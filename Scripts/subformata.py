from argparse import ArgumentParser
from os import chdir
from pathlib import Path
from subprocess import run

try:
    from slugify import slugify
except ImportError:
    print('Instale o pacote slugify')
    print('pip install python-slugify')
    exit(1)

def main():
    parser = ArgumentParser('Substitui o nome dos arquivos de respostas por um nome mais amigável')
    parser.add_argument('-d', '--dir', help='Diretório onde estão os arquivos de respostas', default='respostas')
    args = parser.parse_args()
    resp_dir = Path(args.dir)
    if resp_dir.is_dir():
        chdir(resp_dir)
        resp_files = resp_dir.glob('*.py')

        for f in resp_files:
            name = f.name
            if '-' in name:
                if name.count('-') == 1:
                    slug_name = slugify(name.split('-')[1].strip()).replace('-', '_')
                    new_name = f'desenho_{slug_name}'
                    cmd_args = ["git", "mv", name, new_name]
                    run(cmd_args)
                else:
                    print(name)

if __name__ == '__main__':
    main()
