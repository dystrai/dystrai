#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from getpass import getuser
import pwd
import sys

parser = ArgumentParser()
parser.add_argument('login', default=None, nargs='?')

args = parser.parse_args()

if not args.login:
    login = getuser()
else:
    login = args.login

if '.' in login:
    try:
        user_data = pwd.getpwnam(login)
        gecos = user_data.pw_gecos
        if ',' in gecos:
            full_name,registration = gecos.split(',')
            if registration.isdigit():
                print(registration)
        else:
            sys.exit(2)
    except:
        print('Conta não encontrada.')
        sys.exit(3)
else:   
    print('Somente válido para contas que possuem "." no login.')
    sys.exit(1)
