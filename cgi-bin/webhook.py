#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##  https://stackoverflow.com/questions/10718572/post-json-to-python-cgi

import os
import sys
import json

compr_conteudo = int(os.environ["CONTENT_LENGTH"])
corpo_req = sys.stdin.read(compr_conteudo)
dados_recebidos = json.loads(corpo_req)

