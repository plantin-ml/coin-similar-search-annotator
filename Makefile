CONFIG_FILE:="base-resnet.yaml"

.PHONY: evaluate index up milvus_index clean test

up:
	docker-compose up --build -d
index:
	python -m img_retrieval.src.cli.index --config-name=$(CONFIG_FILE)

evaluate:
	python -m img_retrieval.evaluate --config-name=$(CONFIG_FILE)

predict:
	python -m img_retrieval.predict --config-name=$(CONFIG_FILE) dataset.batch_size=128 \
		dataset.num_workers=16


help:
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-24s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m## /[33m/' && printf "\n"

## TOOLS
clean:
	@rm -rf .cache
	@find . -name *.pyc -delete
	@find . -type d -name __pycache__ -delete

.DEFAULT_GOAL := help