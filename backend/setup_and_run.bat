@echo off
echo Inicializando ambiente Mágico do MVP OpusClone...

IF NOT EXIST ".venv" (
    echo [1/3] Criando Ambiente Virtual (VENV)...
    python -m venv .venv
)

echo [2/3] Instalando Dependencias e IA...
call .venv\Scripts\activate.bat
pip install -r requirements.txt

echo [3/3] Iniciando o Servidor de Inteligencia Artificial (FastAPI)...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
