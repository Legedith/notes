poetry env use "C:\Program Files\Python39\python.exe"
set PYTHONPATH=%PYTHONPATH%;%CD%
poetry shell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124