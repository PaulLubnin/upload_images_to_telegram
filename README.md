# Загрузка фотографий в телеграм чат
Набор скриптов для скачивания фотографии с сайтов NASA и SpaceX, и публикации в телеграм канал.

### Как установить:
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
Необходимо создать файл с секретными данными - `.env`
```
NASA_API_KEY=<nasa_api_key>
TG_BOT_TOKEN=<tg_bot_token>
TG_CHAT_ID=<tg_chat_id>
```

### Как запустить:
- Для загрузки APOD, где QUANTITY_APOD количество фотографий:
```
python load_apod.py -qa [QUANTITY_APOD]
```
- Для загрузки EPIC, где QUANTITY_EPIC количество фотографий:
```
python load_epic.py -qe [QUANTITY_EPIC]
```
- Для загрузки SPACEX, где ID_LAUNCH идентификатор пуска, например `6243adcaaf52800c6e919254`, без идентификатора загружается случайный пуск:
```
python load_spacex.py -id [ID_LAUNCH]
```
- Для публикации, где PERIODICITY интервал публикации:
```
python start_publishing.py -p [PERIODICITY]
```