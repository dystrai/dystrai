#! /usr/bin/env python3

from random import randint

oct1 = randint(1, 255)
oct2 = randint(0, 255)
oct3 = randint(0, 255)
oct4 = randint(0, 255)

masc = randint(24, 32)

print(f'{oct1}.{oct2}.{oct3}.{oct4}/{masc}')