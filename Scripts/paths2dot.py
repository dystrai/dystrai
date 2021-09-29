#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from pprint import pprint
import shutil

from graphviz import Digraph
from slugify import slugify

# Caminho de ID
caminho_id = {}

class Caminho:
    def __init__(self, caminho: Path) -> None:
        self.cam_absoluto = caminho.resolve()
        self.nome = self.cam_absoluto.name
        self.partes = self.cam_absoluto.parts
        self.setID()
        self.filhos = []
        self.visitado = False

    def setID(self):
        nome_base = self.partes[-1]
        cam_absoluto = self.cam_absoluto

        if nome_base in caminho_id:
            if caminho_id[nome_base] != self:
                n = 1
                chave_candidata = f'{nome_base}_{n}'
                while chave_candidata in caminho_id:
                    if caminho_id[chave_candidata] == self:
                        break
                    n += 1
                    chave_candidata = f'{nome_base}_{n}'
                else:
                    self.id_caminho = chave_candidata
                    caminho_id[chave_candidata] = self
                self.id_caminho = chave_candidata
            else:
                self.id_caminho = nome_base
        else: # nome_base not in caminho_id:
            self.id_caminho = nome_base
            caminho_id[nome_base] = self

    def adicionar_filho(self, filho):
        if filho not in self.filhos:
            self.filhos.append(filho)

    def __repr__(self) -> str:
        return str(self.cam_absoluto)

    def __eq__(self, o: object) -> bool:
        return self.cam_absoluto == o.cam_absoluto

    def eh_pasta(self) -> bool:
        return self.cam_absoluto.is_dir()

    def eh_arquivo(self) -> bool:
        return self.cam_absoluto.is_file()


def passeia_nos_filhos(caminho: Caminho, nome=str, grafo=Digraph) -> None:
    if not caminho.visitado:
        for filho in caminho.filhos:
            grafo.edge(nome, filho.id_caminho)
            passeia_nos_filhos(filho, filho.id_caminho, grafo)

        caminho.visitado = True

def desenha_grafo():
    g_nome = sys.argv[1]
    g_titulo = sys.argv[2]
    grafo = Digraph(g_nome, format='png', strict=True)
    grafo.attr('graph', rankdir='LR')
    # https://stackoverflow.com/questions/6450765/how-do-you-center-a-title-for-a-diagram-output-to-svg-using-dot
    grafo.attr('graph', label=g_titulo)
    grafo.attr('graph', labelloc='t')
    grafo.attr('graph', splines='false') # linhas retas (straight lines)

    for id_cam,caminho in caminho_id.items():
        nome = 'barra' if id_cam == '/' else id_cam
        etiqueta = '/' if id_cam == '/' else caminho.nome
        forma = 'folder' if caminho.eh_pasta() else 'plain'
        grafo.node(name=nome, label=etiqueta, shape= forma)
        passeia_nos_filhos(caminho, nome=nome, grafo=grafo)

    #grafo.view()
    grafo.render()
    #shutil.move(f'{g_nome}.gv.png', f'{g_nome}.png')


def principal():
    args = sys.argv
    if len(args) < 4:
        print(f'''\
Uso:
  {sys.argv[0]} NOME TITULO CAMINHO [CAMINHO...]''')
        sys.exit(1)

    for a in args[3:]:
        path = Path(a).resolve()
        partes = path.parts
        global caminhos
        caminhos = []
        for i,p in enumerate(path.parts):
            inter_path = Path('/'+os.path.sep.join((partes[1:(i+1)])))
            c = Caminho(inter_path)
            caminhos.append(c)

        for j,c in enumerate(caminhos[:-1]):
            caminho_id[c.id_caminho].adicionar_filho(caminhos[j+1])

    desenha_grafo()


if __name__ == '__main__':
    principal()
