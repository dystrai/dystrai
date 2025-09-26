#!/bin/bash
# Script: bateria-check.sh
# Mostra saúde da bateria e recomendação

BAT="/sys/class/power_supply/BAT0"

if [ -d "$BAT" ]; then
    if [ -f "$BAT/energy_full" ]; then
        FULL=$(cat "$BAT/energy_full")
        DESIGN=$(cat "$BAT/energy_full_design")
    elif [ -f "$BAT/charge_full" ]; then
        FULL=$(cat "$BAT/charge_full")
        DESIGN=$(cat "$BAT/charge_full_design")
    else
        echo "Não foi possível encontrar informações de capacidade."
        exit 1
    fi

    SAUDE=$(echo "scale=2; $FULL / $DESIGN * 100" | bc)

    echo "Capacidade de fábrica : $DESIGN"
    echo "Capacidade atual      : $FULL"
    echo "Saúde da bateria      : $SAUDE %"

    # Recomendação
    if (( $(echo "$SAUDE >= 80" | bc -l) )); then
        echo "Situação: ✅ Bateria saudável"
    elif (( $(echo "$SAUDE >= 60" | bc -l) )); then
        echo "Situação: ⚠️  Atenção — autonomia reduzida"
    else
        echo "Situação: ❌ Troca recomendada"
    fi
else
    echo "Nenhuma bateria encontrada em $BAT"
fi
