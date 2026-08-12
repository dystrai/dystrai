#!/bin/sh
# AI prompt: https://chatgpt.com/share/6a7ca0b4-ee6c-83e9-a8d3-f4102a413ae6

SSH_DIR="$HOME/.ssh"
SSH_CONFIG="$SSH_DIR/config"

if [ ! -d "$SSH_DIR" ]; then
    mkdir -p "$SSH_DIR"
    chmod 700 "$SSH_DIR"
fi

if [ ! -f "$SSH_CONFIG" ] ||
   ! grep -qE '^[[:space:]]*StrictHostKeyChecking[[:space:]]+accept-new[[:space:]]*$' "$SSH_CONFIG"
then
    cat >> "$SSH_CONFIG" << 'EOF'

Host *
    StrictHostKeyChecking accept-new
EOF
    chmod 600 "$SSH_CONFIG"
fi
