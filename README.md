# sjvacansy

папка проекта: /superjob/sjvacansy
папка venv: /superjob/superjob
скрипт паука: /superjob/sjvacancy/spiders/SJvacansy.py
скрипт запуска: /superjob/runner.py
результат в файле:/superjob/items.json

Запуск из командной строки:
pythoh runner.py

или

из /superjob:
scrapy crawl SJvacancy

Результат сохраняется в items.json

можно контролировать:
в SJvacansy.py

to_model=True -  сохраняем результат в вашу модель
to_model=False -  сохраняем результат в стандартный item scrapy

[ссылка на Docker](https://hub.docker.com/layers/144735871/alsavva/myfirst/sjspider2/images/sha256-612776500fa23815055648b7edb37c9d6cd030d4713e8abf885a41880359019c?context=explore)
