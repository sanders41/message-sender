@_default:
  just --list

@lint:
  echo pyrefly
  just --justfile {{justfile()}} pyrefly
  echo ruff-check
  just --justfile {{justfile()}} ruff-check
  echo ruff-format
  just --justfile {{justfile()}} ruff-format

@pyrefly:
  uv run pyrefly check

@ruff-check:
  uv run ruff check message_sender tests

@ruff-format:
  uv run ruff format message_sender tests

@lock:
  uv lock

@lock-upgrade:
  uv lock --upgrade

@install:
  uv sync --frozen --all-extras

@test *args="":
  uv run pytest {{args}}
