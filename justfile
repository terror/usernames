fmt:
  black .

run:
  python3 main.py -i input.txt -o output.txt

lint:
  pylint main.py
