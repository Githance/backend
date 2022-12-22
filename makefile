# Приводит venv в соответствие с pyproject.toml и обновляет requirements.txt.
poetry:
	poetry add pycowsay && \
	poetry remove pycowsay && \
	poetry export --without-hashes > requirements.txt && \
	poetry export --dev --without-hashes > requirements_dev.txt

# Проверяет код на соответствие PEP8. Не форматирует, только информирует.
check:
	isort --check .
	black --check .
	flake8 .

format:
	isort .
	black .