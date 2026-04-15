#!/bin/bash

echo "==============================="
echo "Activando entorno virtual..."
echo "==============================="

if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "==============================="
echo "Ejecutando aplicacion..."
echo "==============================="

python main.py