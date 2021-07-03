default:
  just --list

ci: fmt lint

lint:
  pylint main.py

fmt:
  yapf --in-place --recursive *.py

run *args:
  python3 main.py {{args}}

install *pkg:
  pipenv install {{pkg}} --skip-lock

lock:
  pipenv lock --pre

install-editable:
  pipenv install -e .
