#!/usr/bin/env python3

import googletrans
tradutor = googletrans.Translator()

while linha := input():
    print(tradutor.translate(linha, src='pt', dest='en'))
