PIP = pip
PYTHON = python3

.PHONY: agg-data
agg-data:
	find ./MillionSongSubset/data/ -name "*.h5" -type f -exec mv {} ./raw_data/ \;

.PHONY: lint 
lint:
	flake8
	
.PHONY: docs
docs:
	pandoc -s -o ./docs/data_collection.pdf ./docs/data_collection.md
	pandoc -s -o ./docs/proposal.pdf ./docs/proposal.md
	$(MAKE) -C ./docs/final_report/ docs

.PHONY: setup
setup:
	$(PIP) install -r requirements.txt
	mkdir ./raw_data/
	mkdir -p ./data/matrix_files/
	mkdir -p ./data/pickled_files/

.PHONY: test
test: lint
	$(PYTHON) -m pytest ./tests/

.PHONY: download_subset
download_subset:
	curl http://static.echonest.com/millionsongsubset_full.tar.gz > millionsongsubset.tar.gz
	tar -xvzf millionsonbsubset.tar.gz

.PHONY: run_clean
run_clean:
	rm -f ./data/matrix_files/*.csv
	rm -f ./data/pickled_files/*.pkl
