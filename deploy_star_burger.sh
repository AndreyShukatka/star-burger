#!/bin/bash
git pull
echo 'Git код обновлен'
pip install -r requirements.txt
echo 'Библиотеки для Python установлены'
npm ci --dev
echo 'Пакет JS собран'
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
echo 'запустили сборку фронтенда'
python3 manage.py collectstatic
echo 'Статика собрана'
python3 manage.py makemigrations
python3 manage.py migrate
echo 'Миграция выполнена'
systemctl stop nginx
systemctl stop starburger
systemctl start nginx
systemctl start starburger
echo "Деплой завершен"
