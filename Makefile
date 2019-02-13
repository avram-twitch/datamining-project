.PHONY: agg-data
agg-data:
	find ./MillionSongSubset/data/ -name "*.h5" -type f -exec mv {} ./raw_data/ \;

.PHONY: process-raw
process-raw:
	python3 ./process_raw_data.py

.PHONY: lint 
lint:
	flake8
	
.PHONY: docs
docs:
	pandoc -s -o ./docs/data_collection.pdf ./docs/data_collection.md
	pandoc -s -o ./docs/proposal.pdf ./docs/proposal.md
