#!/usr/bin/env python3

'''
Miniblog para linha de comandos
'''

import argparse
from datetime import datetime
from getpass import getuser
import os
import pathlib
from time import strftime

DIR_NOVIDADES = '/var/lib/novidades'
agora = datetime.now()
meu_usuario = getuser()
editor = environ.get('EDITOR', 'nano')

novidades = pathlib.Path(DIR_NOVIDADES)
novidades_hj = novidades / str(agora.year) / str(agora.month) / str(agora.day)
minhas_novidades = novidades_hj / f'{strftime("%H-%M-%S")}-{meu_usuario}.md'

if not novidades_hj.exists():
    novidades_hj.mkdir(parents=True)
   
minhas_novidades.touch()
os.system(f'{editor} {minhas_novidades}')

