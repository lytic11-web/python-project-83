import os

import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from requests.exceptions import RequestException

from page_analyzer.db import (
    add_url,
    add_url_check,
    get_url,
    get_url_by_name,
    get_url_checks,
    get_urls,
)
from page_analyzer.parser import parse_page, truncate
from page_analyzer.validator import normalize_url, validate_url

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_url_handler():
    url_input = request.form.get('url', '')

    error = validate_url(url_input)
    if error:
        flash(error, 'danger')
        return render_template('index.html'), 422

    normalized_url = normalize_url(url_input)

    existing = get_url_by_name(normalized_url)
    if existing:
        flash('Страница уже существует', 'info')
        return redirect(url_for('url_detail', id=existing['id']))

    url_id = add_url(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_detail', id=url_id))


@app.get('/urls')
def urls_list():
    urls = get_urls()
    return render_template('urls.html', urls=urls)


@app.post('/urls/<int:id>/checks')
def check_url(id):
    url = get_url(id)
    if not url:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('urls_list')), 404

    try:
        response = requests.get(url['name'], timeout=5)
        response.raise_for_status()
        status_code = response.status_code

        h1, title, description = parse_page(response.text)

        h1 = truncate(h1)
        title = truncate(title)
        description = truncate(description)

        add_url_check(id, status_code, h1, title, description)
        flash('Страница успешно проверена', 'success')

    except RequestException:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('url_detail', id=id))


@app.get('/urls/<int:id>')
def url_detail(id):
    url = get_url(id)
    if not url:
        return render_template('404.html'), 404
    checks = get_url_checks(id)
    return render_template('url.html', url=url, checks=checks)
