PIP = pip3
PYTHON = python3

.PHONY: agg_data
agg-data:
	find ./MillionSongSubset/data/ -name "*.h5" -type f -exec mv {} ./raw_data/ \;

.PHONY: process_raw
process_raw:
	$(PYTHON) ./run.py process_raw

.PHONY: to_matrix
to_matrix:
	$(PYTHON) ./run.py to_matrix

.PHONY: lsh
lsh:
	$(PYTHON) ./run.py run_lsh

.PHONY: minhash
run_minhash:
	$(PYTHON) ./run.py run_minhash

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
