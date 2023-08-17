run:
	poetry run python -m route_lengths.main

output.json: route_lengths

.PHONY: run