code-compiler

Using Python PLY.

Instalation guide:

venv:

1 - python3 -m venv .venv

2 - source .venv/bin/activate

3 - python --version

pip: 

1 - pip install --upgrade pip

2 - pip install pip-tools

Sync requirements:``˜

 1 - pip-sync requirements/requirements.txt

Compile requirements:

1 - pip-compile requirements/requirements.in -o requirements/requirements.txt