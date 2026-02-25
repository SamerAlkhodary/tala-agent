VERSION ?= latest
SERVICE_NAME = {{template-agent}}
DOCKER_IMAGE := ghcr.io/qlik-trial/$(SERVICE_NAME)
DOCKER_FILE ?= Dockerfile
BUILD_TARGET ?= prod
BUILD_TIME = `date -u +%Y-%m-%dT%H:%M:%SZ`
REVISION ?= `git rev-parse HEAD 2>/dev/null`
BRANCH ?= `git rev-parse --abbrev-ref HEAD`

build-docker-image:
	docker build --platform linux/amd64 --file ./Dockerfile --target $(BUILD_TARGET) \
	--build-arg CREATED=$(BUILD_TIME) \
	--build-arg REVISION=$(REVISION) \
	--build-arg VERSION=$(VERSION) \
	--build-arg GITHUB_API_TOKEN=$(GITHUB_API_TOKEN) \
	--tag $(DOCKER_IMAGE)$(IMAGE_NAME_SUFFIX):$(VERSION) \
	--ssh default \
	.
	docker tag $(DOCKER_IMAGE)$(IMAGE_NAME_SUFFIX):$(VERSION) $(DOCKER_IMAGE)$(IMAGE_NAME_SUFFIX):latest

build-docker:
	@IMAGE_NAME_SUFFIX= BUILD_TARGET=prod $(MAKE) build-docker-image
sync-dependencies:
	uv sync
	uv pip compile pyproject.toml --no-deps -o requirements.txt

keys:
		./scripts/fetch-keys.sh

env:
		./scripts/create-env-file.sh

sidecar:
		./scripts/create-sidecar-container.sh


qlty-downlaod-windows:
	powershell -c "iwr https://qlty.sh | iex"

lint:
	uv run ruff check {{template_agent}}/ --config .ruff.toml

lint-fix:
	uv run ruff check {{template_agent}}/ --fix --config .ruff.toml
test-unit:
	uv run -m pytest --cov={{template_agent}} -vv tests/unit --cov-report=lcov:coverage/unit.info

test-component:
	uv run -m pytest --cov={{template_agent}} -vv tests/component --cov-report=lcov:coverage/component.info

registry-image:
	@make build-docker
	@echo "Pushing $(SERVICE_NAME) to registry: $(SDE_REGISTRY)"
	@docker image tag $(DOCKER_IMAGE):latest registry.$(SDE_REGISTRY).pte.qlikdev.com/$(SERVICE_NAME):latest
	@DOCKER_CLIENT_TIMEOUT=$(DOCKER_CLIENT_TIMEOUT) COMPOSE_HTTP_TIMEOUT=$(COMPOSE_HTTP_TIMEOUT) \
		docker image push registry.$(SDE_REGISTRY).pte.qlikdev.com/$(SERVICE_NAME):latest