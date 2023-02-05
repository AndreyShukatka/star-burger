# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)


[Пример рабочего сайта](https://www.russiansword.ru)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## Как запустить dev-версию сайта

Для запуска сайта нужно запустить **одновременно** бэкенд и фронтенд, в двух терминалах.

### Как собрать бэкенд

Скачайте код:
```sh
git clone https://github.com/devmanorg/star-burger.git
```

Перейдите в каталог проекта:
```sh
cd star-burger
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии.

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Получить токен API Яндекс-геокодера
[Инструкция к API](https://dvmn.org/encyclopedia/api-docs/yandex-geocoder-api/)

Определите переменную окружения `SECRET_KEY`. Создать файл `.env` в каталоге `star_burger/` и положите туда такой код:
```sh
SECRET_KEY=django-insecure-0if40nf4nf93n4
YA_GEO_API_KEY=Ваш токен Яндекс-геокодера
```

Создайте файл базы данных SQLite и отмигрируйте её следующей командой:

```sh
python manage.py migrate
```

Запустите сервер:

```sh
python manage.py runserver
```

Откройте сайт в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Если вы увидели пустую белую страницу, то не пугайтесь, выдохните. Просто фронтенд пока ещё не собран. Переходите к следующему разделу README.

### Собрать фронтенд

**Откройте новый терминал**. Для работы сайта в dev-режиме необходима одновременная работа сразу двух программ `runserver` и `parcel`. Каждая требует себе отдельного терминала. Чтобы не выключать `runserver` откройте для фронтенда новый терминал и все нижеследующие инструкции выполняйте там.

[Установите Node.js](https://nodejs.org/en/), если у вас его ещё нет.

Проверьте, что Node.js и его пакетный менеджер корректно установлены. Если всё исправно, то терминал выведет их версии:

```sh
nodejs --version
# v12.18.2
# Если ошибка, попробуйте node:
node --version
# v12.18.2

npm --version
# 6.14.5
```

Версия `nodejs` должна быть не младше 10.0. Версия `npm` не важна. Как обновить Node.js читайте в статье: [How to Update Node.js](https://phoenixnap.com/kb/update-node-js-version).

Перейдите в каталог проекта и установите пакеты Node.js:

```sh
cd star-burger
npm ci --dev
```

Команда `npm ci` создаст каталог `node_modules` и установит туда пакеты Node.js. Получится аналог виртуального окружения как для Python, но для Node.js.

Помимо прочего будет установлен [Parcel](https://parceljs.org/) — это упаковщик веб-приложений, похожий на [Webpack](https://webpack.js.org/). В отличии от Webpack он прост в использовании и совсем не требует настроек.

Теперь запустите сборку фронтенда и не выключайте. Parcel будет работать в фоне и следить за изменениями в JS-коде:

```sh
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Если вы на Windows, то вам нужна та же команда, только с другими слешами в путях:

```sh
.\node_modules\.bin\parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Дождитесь завершения первичной сборки. Это вполне может занять 10 и более секунд. О готовности вы узнаете по сообщению в консоли:

```
✨  Built in 10.89s
```

Parcel будет следить за файлами в каталоге `bundles-src`. Сначала он прочитает содержимое `index.js` и узнает какие другие файлы он импортирует. Затем Parcel перейдёт в каждый из этих подключенных файлов и узнает что импортируют они. И так далее, пока не закончатся файлы. В итоге Parcel получит полный список зависимостей. Дальше он соберёт все эти сотни мелких файлов в большие бандлы `bundles/index.js` и `bundles/index.css`. Они полностью самодостаточно и потому пригодны для запуска в браузере. Именно эти бандлы сервер отправит клиенту.

Теперь если зайти на страницу  [http://127.0.0.1:8000/](http://127.0.0.1:8000/), то вместо пустой страницы вы увидите:

![](https://dvmn.org/filer/canonical/1594651900/687/)

Каталог `bundles` в репозитории особенный — туда Parcel складывает результаты своей работы. Эта директория предназначена исключительно для результатов сборки фронтенда и потому исключёна из репозитория с помощью `.gitignore`.

**Сбросьте кэш браузера <kbd>Ctrl-F5</kbd>.** Браузер при любой возможности старается кэшировать файлы статики: CSS, картинки и js-код. Порой это приводит к странному поведению сайта, когда код уже давно изменился, но браузер этого не замечает и продолжает использовать старую закэшированную версию. В норме Parcel решает эту проблему самостоятельно. Он следит за пересборкой фронтенда и предупреждает JS-код в браузере о необходимости подтянуть свежий код. Но если вдруг что-то у вас идёт не так, то начните ремонт со сброса браузерного кэша, жмите <kbd>Ctrl-F5</kbd>.


## Как запустить prod-версию сайта

#### Арендуйте удаленный сервер и установите на нем последнюю версию OS Ubuntu

Установите Postgresql, git, pip, venv, nginx:
```shell
sudo apt update
sudo apt -y install git
sudo apt -y install postgresql
sudo apt -y install python3-pip
sudo apt -y install python3-venv
sudo apt -y install nginx
```
#### Создайте базу данных Postgres и пользователя для работы с ней, выполнив последовательно следующие команды:
```shell
sudo su - postgres
psql
CREATE DATABASE <имя базы данных>;
CREATE USER <пользователь postgres> WITH PASSWORD '<пароль для пользователя>';
ALTER ROLE <имя пользователя> SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE <имя базы данных> TO <имя пользователя>;
```

#### Скачайте код проекта в каталог `/opt` корневого каталога сервера:
```shell
cd ..
cd opt
git clone https://github.com/Sergryap/star-burger.git
```
#### Перейдите в каталог проекта:

```shell
cd ../opt/star-burger
```
###### В каталоге проекта создайте виртуальное окружение:
```shell
python3 -m venv venv
```
###### Активируйте его:

```shell
source venv/bin/activate
```
###### Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```
#### Установите gunicorn в виртуальное окружение:
```sh
pip install gunicorn
```
#### В каталоге проекта и установите пакеты Node.js:

```sh
npm ci --dev
```
#### Соберите фронтенд:
```sh
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
```
#### Создайте файл `.env` с переменными окружения в каталоге `star_burger/`:
```
SECRET_KEY=django-insecure-0if40nf4nf93n4
YANDEX_GEO_TOKEN=<Ваш API ключ от геокодера Яндекса>
ROLLBAR_ACCESS_TOKEN=<Ваш токен от сервиса rollbar.com>
ENVIRONMENT=<Название среды разработки для отслеживания ошибок в rollbar.com>
DB_NAME=<Название БД>
DB_USER=<Пользователь БД>
DB_PASSWORD=<Пароль БД>
DB_HOST=<Хост БД>
DB_PORT=<Порт БД>
```

Подробнее о `ROLLBAR_ACCESS_TOKEN` см здесь: [rollbar.com](https://rollbar.com)

#### Выполните миграцию базы данных Postgresql следующей командой:

```shell
python3 manage.py migrate
```
#### Создайте суперпользователя:
```shell
python3 manage.py createsuperuser
```
#### Соберите статику для prod-версии:
```shell
python3 manage.py collectstatic
```

#### Создайте файл `starburger.service` в каталоге `/etc/systemd/system` следующего содержания:
```markdown
[Unit]
Description=GetIP site
Requires=postgresql.service

[Service]
Type=simple
WorkingDirectory=/opt/star-burger
ExecStart=gunicorn -w 3 -b 127.0.0.1:8000 star_burger.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```
#### Настройте автоматическое обновление сертификатов
###### Создайте файл `certbot-renewal.service` в каталоге `/etc/systemd/system`:
```markdown
[Unit]
Description=Certbot Renewal

[Service]
ExecStart=/snap/bin/certbot renew --force-renewal --post-hook "systemctl reload nginx.service"
```
###### Создайте файл `certbot-renewal.timer` в каталоге `/etc/systemd/system`:
```markdown
# Файл /etc/systemd/system/certbot-renewal.timer
[Unit]
Description=Timer for Certbot Renewal

[Timer]
OnBootSec=600000
OnUnitActiveSec=1w

[Install]
WantedBy=multi-user.target
```
#### Настройте автоматическую очистку сессий пользователей
###### Создайте файл `clearsessions.service` в каталоге `/etc/systemd/system`:
```markdown
[Service]
WorkingDirectory=/opt/star-burger
ExecStart=python3 manage.py clearsessions
Restart=on-failure
RestartSec=86400s

[Install]
WantedBy=multi-user.target
```
###### Создайте файл `clearsessions.timer` в каталоге `/etc/systemd/system`:
```markdown
[Unit]
Description=Очистить сессию

[Timer]
OnBootSec=86400
OnUnitActiveSec=1w

[Install]
WantedBy=multi-user.target
```

#### Настройте Nginx
###### Перейдите в каталог /etc/nginx/sites-enabled:
```shell
cd ../etc/nginx/sites-enabled
```
###### Удалите в этом каталоге все файлы и создайте файл `starburger` следующего содержания:

```markdown
server {

location / {
include '/etc/nginx/proxy_params';
proxy_pass http://127.0.0.1:8000;
}

location /media/ {
alias /opt/star-burger/media/;
}

location /static/ {
alias /opt/star-burger/staticfiles/;
}
server_name Ваш домен www.Ваш домен;
}

```

## Получаем сертификат для протокола HTTPS
#### Установить Certbot
```shell
sudo snap install --classic certbot
```
#### Запустите эту команду, чтобы получить сертификат.
```shell
sudo certbot --nginx
```
#### Выполните команды для запуска демонов:
```shell
systemctl start nginx
systemctl start starburger
systemctl enable starburger
systemctl start certbot-renewal
systemctl enable certbot-renewal.timer
systemctl start clearsessions
systemctl enable clearsessions.timer
nginx -s reload
```
После успешного выполнения указанных действий сайт будет доступен по ссылке:
```
http://<HOST вашего сервера>
```
## Как быстро применить изменения из репозитория для вашего сайта

Для того чтобы изменения в вашем репозитории быстро отобразились на сайте выполните команду, находясь в корневом каталоге проекта:

```sh
./deploy_star_burger.sh
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).

Где используется репозиторий:

- Второй и третий урок [учебного курса Django](https://dvmn.org/modules/django/)
