#!/bin/bash -xv

shopt -s nullglob

DISCOS=(/dev/sd[a-z])
DISCOS+=(none)

select disco in "${DISCOS[@]}"; do
    case "$disco" in
        none)
            exit 1
            ;;
        /dev/sd[a-z])
            DISCO="$disco"
            break
            ;;
        *)
            echo "Opção inválida."
            ;;
    esac
done
PARTICAO="${DISCO}1"

# 1. Verifica se o script está sendo executado como root
if [ "$EUID" -ne 0 ]; then
  echo "Erro: Este script precisa ser executado como root (use sudo)."
  exit 1
fi

# 2. Confirmação de segurança
echo "==========================================================="
echo " ATENÇÃO: TODOS OS DADOS EM $DISCO SERÃO PERDIDOS!"
echo " Certifique-se de que $DISCO é o disco correto."
echo "==========================================================="
#read -p "Você tem certeza absoluta que deseja continuar? (s/N): " confirm
#if [[ ! "$confirm" =~ ^[sS]$ ]]; then
#  echo "Operação cancelada pelo usuário."
#  exit 1
#fi

echo "[1/5] Desmontando partições ativas em $DISCO..."
umount ${DISCO}* 2>/dev/null

echo "[2/5] Removendo assinaturas de sistemas de arquivos antigos..."
wipefs -a $DISCO

echo "[3/5] Criando nova tabela de partições (GPT)..."
parted -s $DISCO mklabel gpt

echo "[4/5] Criando a nova partição ($PARTICAO) ocupando 100% do espaço..."
parted -s $DISCO mkpart primary ext4 0% 100%

# Força o kernel a reler a tabela de partições e aguarda
partprobe $DISCO
sleep 2

echo "[5/5] Formatando a partição em ext4..."
mkfs.ext4 -F $PARTICAO

echo "Concluído! A partição $PARTICAO foi criada e formatada com sucesso."
