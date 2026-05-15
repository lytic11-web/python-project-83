# Page Analyzer

### Hexlet tests and linter status,SonarCloud status:
[![Actions Status](https://github.com/lytic11-web/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/lytic11-web/python-project-83/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lytic11-web_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=lytic11-web_python-project-83)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=lytic11-web_python-project-83&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=lytic11-web_python-project-83)


## Демо

[Page Analyzer on Render](https://page-analyzer-rv3j.onrender.com)

## Описание

Page Analyzer — веб-приложение для проверки сайтов на SEO-пригодность.
Позволяет добавлять URL, проверять их доступность и извлекать мета-теги (h1, title, description).
Используемые инструменты: uv, Flask, Gunicorn, python-dotenv, Bootstrap, Psycopg, validators, Requests, Beautifulsoup.

## Установка и запуск

```bash
make install
make dev

