# Kingshot Discord Bot

[![CI](https://img.shields.io/github/actions/workflow/status/unRooting/kingshot-discord-bot/ci.yml?branch=main)](../../actions)
[![Docker](https://img.shields.io/github/actions/workflow/status/unRooting/kingshot-discord-bot/docker.yml?label=docker)](../../actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A lightweight, extensible Discord bot to surface **Kingshot** game information via **slash commands**.

## Highlights
- Python **discord.py**
- JSON data files in `./data`
- Fuzzy matching & aliases
- Clean embedded responses
- Docker + compose
- CI for linting & Docker publish

## Quick Start
1) Create a bot token and copy `.env.example` → `.env`.
2) `pip install -r requirements.txt`
3) `python bot.py` (or `docker compose up -d`)

## Commands
- `/hero name:<text>`
- `/building name:<text> [level:<int>]`
- `/research name:<text>`
- `/event [name:<text>]`
- `/links`
- `/ping`
- `/admin_reload`

## Data model
Edit JSONs under `data/`: `heroes.json`, `buildings.json`, `research.json`, `events.json`, `aliases.json`.

---

**Dataset update:** Added heroes *Edwin*, *Seth* and buildings *Embassy*, *Academy* to `data/`.
