.PHONY: setup test build check audit serve

setup:
	python -m pip install -e .

test:
	PYTHONPATH=src python -m unittest discover -s tests -v

build:
	PYTHONPATH=src python -m monopoly build --out artifacts

audit:
	PYTHONPATH=src python -m monopoly audit --rounds 100000

check: test build
	python scripts/verify_deliverables.py --dir artifacts

serve:
	python -m http.server 8000 --directory site
