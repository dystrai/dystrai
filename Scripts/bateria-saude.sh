#!/bin/bash
# Script: bateria-saude.sh
# Calcula a saúde da bateria no Linux

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
    echo "Saúde da bateria: $SAUDE %"
    echo "Capacidade atual: $FULL"
    echo "Capacidade de fábrica: $DESIGN"
else
    echo "Nenhuma bateria encontrada em $BAT"
fi
