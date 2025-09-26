#!/usr/bin/env python3

import argparse
import logging
import pathlib
import subprocess

ESCOLHAS_LOG = ('CRITICAL', 'ERROR', 'WARN', 'INFO', 'DEBUG')
MAN_BIN = '/bin/man'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', help='Nível de registro de eventos', type=str, choices=ESCOLHAS_LOG, default='CRITICAL')
    parser.add_argument('secao', type=int, help='Número da seção das páginas de manual. Veja: man 1 man')
    parser.add_argument('pagina', type=str, help='Página de manual que se deseja consultar. Veja: man 1 man')

    args = parser.parse_args()

    logging.basicConfig(level=args.log, encoding='utf-8')
    logging.info('Analizando os argumentos passados pela linha de comando.')
    logging.info(f'Recebidos os seguintes argumentos: {args}')

    man_bin_path = pathlib.Path(MAN_BIN)
    if not man_bin_path.exists():
        raise FileNotFoundError
    
    global manual
    proc_completado = subprocess.run([MAN_BIN, str(args.secao), args.pagina], capture_output=True)
    if proc_completado.returncode == 0:
        manual = proc_completado.stdout.decode('utf-8')
        print(manual)
    else:
        logging.info('Commando não terminou com êxito.')
        logging.info(f'Código de retorno: {proc_completado.returncode}.')
        logging.info('Saída de erro:')
        logging.info(proc_completado.stderr)
        logging.info('Saída padrão:')
        logging.info(proc_completado.stdout)

if __name__ == '__main__':
    main()

'''
if [ "$#" -ne 2 ]; then
    cat << EOF
Usage:
  $0 SEÇÃO PÁGINA
EOF
    exit 1
fi

SECTION="${1}"
PAGE="${2}"
DOC_ID="${PAGE}-${SECTION}"

if [[ -f "${DOC_ID}.md" ]]; then
    echo "Arquivo de ajuda já encontrado para comando ${cmd}: <${cmd}.md>."
else
    cat << EOF > "${DOC_ID}.md
(${DOC_ID})=

# ${$2}(${1})

\`\`\`
EOF
# Save a Unix manpage as plain text
# https://electrictoolbox.com/save-manpage-plain-text/
man $1 $2 | col -b >> "${2}.md"
echo \`\`\` >> "${2}.md"
fi
'''