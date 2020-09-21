test:
	pipenv run python -m unittest src -v

pipeline:
	./scripts/run_pipeline_locally.sh