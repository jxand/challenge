.PHONY: clean
clean:
	rm -rf venv
	rm -f log.txt
	rm -f ro.db

.PHONY: init
init: clean
	python3 -m venv venv; \
	source venv/bin/activate; \
	pip install -r requirements.txt

.PHONY: run
run:
	source venv/bin/activate; \
	python3 main.py

.PHONY: test
test:
	source venv/bin/activate; \
	python -m unittest -v