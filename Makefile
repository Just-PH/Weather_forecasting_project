PYTHON_VERSION := 3.10.6
ENV_NAME := weather_forecasting-env
ENV_FILE := .env
ML_DIR=~/.lewagon/pokedex

install_dependencies:
	pip install --upgrade pip
	pip install -r requirements.txt

start_env:
	pyenv virtualenv $(PYTHON_VERSION) $(ENV_NAME)
	pyenv local $(ENV_NAME)

set_up_env:
	@echo ""
	@echo "Copying .env from .env.sample ..."
	@if [ -f .env ]; then \
		echo ".env already exists, creating backup as .env.bak ..."; \
		cp .env .env.bak; \
	fi
	cp .env.sample .env
	@echo ""
	@echo "UPDATE ENV VARIABLES IN .env"
	@echo ""
	@echo "Once you are done: make run_pred | run_api_local "

start: start_env set_up_env
	direnv allow
