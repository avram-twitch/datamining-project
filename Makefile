.PHONY: agg-data
agg-data:
	find ./MillionSongSubset/data/ -name "*.h5" -type f -exec mv {} ./data/ \;

.PHONY: lint 
lint:
	flake8
	
