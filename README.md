# Загрузка фотографий в телеграм чат

Набор скриптов для скачивания фотографии с сайтов NASA и SpaceX, и публикации в телеграм канал.
### Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
Необходимо создать файл с секретными данными - `.env`
```
API_KEY=<api_key>
TG_BOT_TOKEN=<tg_bot_token>
TG_CHAT_ID=<tg_chat_id>
```
Для загрузки фотографий воспользуйтесь командой:
```
python photo_upload.py [-h] [-s {spacex,apod,epic}] [-id ID_LAUNCH] [-qa QUANTITY_APOD] [-qe QUANTITY_EPIC]
```
Для публикации фотографий воспользуйтесь командой:
```
python start_publishing.py [-h] [-p PERIODICITY]
```