import os
from urllib.parse import urlparse
from dotenv import load_dotenv
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)
import validators
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

from page_analyzer.db import add_url, get_url, get_url_by_name, get_urls, add_url_check, get_url_checks

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_url_handler():
    url_input = request.form.get('url', '').strip()

    if not url_input:
        flash('URL обязателен', 'danger')
        return render_template('index.html'), 422

    if len(url_input) > 255:
        flash('URL превышает 255 символов', 'danger')
        return render_template('index.html'), 422

    if not validators.url(url_input):
        flash('Некорректный URL', 'danger')
        return render_template('index.html'), 422

    # Нормализация: оставляем только scheme + netloc
    parsed = urlparse(url_input)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}"

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

        # Парсинг HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        h1 = soup.h1.get_text(strip=True) if soup.h1 else None
        title = soup.title.string.strip() if soup.title and soup.title.string else None

        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc['content'].strip() if meta_desc and meta_desc.get('content') else None

        # Обрезка до 200 символов
        h1 = h1[:200] if h1 else None
        title = title[:200] if title else None
        description = description[:200] if description else None

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
