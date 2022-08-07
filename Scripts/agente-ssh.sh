#!/usr/bin/env bash

# TODO: Detect if script was sourced
# Ref.: [bash - How to detect if a script is being sourced - Stack Overflow]
# Link: https://stackoverflow.com/questions/2683279/how-to-detect-if-a-script-is-being-sourced
# 

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519


