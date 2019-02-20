
PIP = pip3
PYTHON = python3

.PHONY: agg-data
agg-data:
	find ./MillionSongSubset/data/ -name "*.h5" -type f -exec mv {} ./raw_data/ \;

.PHONY: process-raw
process-raw:
	$(PYTHON) ./process_raw_data.py

.PHONY: lint 
lint:
	flake8
	
.PHONY: docs
docs:
	pandoc -s -o ./docs/data_collection.pdf ./docs/data_collection.md
	pandoc -s -o ./docs/proposal.pdf ./docs/proposal.md

.PHONY: setup
setup:
	$(PIP) install -r requirements.txt

.PHONY: test
test: lint
	$(PYTHON) -m pytest ./tests/
