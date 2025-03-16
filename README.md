![Python 3.12.3](https://img.shields.io/badge/Python-3.12.3-blue)
# evo-containerapp-telegrambot-webhook-python-sample

## Пример развертывания telegram бота на python на Evolution Container Apps

Телеграм бот написан на python 3.12.3 с использование aiogram и aiohttp, telegram webhook

Для запуска телеграм бота через Container Apps необходимо:
- Получить токен для телеграм бота - написать @BotFather
- Собрать и запушать docker образ в Artifact Registry
- Создать Container Apps
- Добавить webhook в telegram  

## Получение telegram bot token
1. Создать телеграм бота через [@BotFather](https://telegram.me/BotFather)
2. Получить токен

## Сборка и пуш docker образа в Artifact Registry
Необходимо собрать docker образ и запушать его в Artifact Registry. [Документация](https://cloud.ru/ru/docs/artifact-registry-evolution/ug/topics/quickstart.html)

Шаги:
```bash
# 1. Авторизация
docker login <registry_name>.cr.cloud.ru -u <key_id> -p <key_secret>
# 2. Сборка Docker образа
docker build . -t <registry_name>.cr.cloud.ru/telegrambot:latest --platform linux/amd64
# 3. Пуш образа в Artifact Registry
docker push <registry_name>.cr.cloud.ru/telegrambot:latest
```

## Создание Container Apps
При создании Container App необходимо:
1. Включить создание публичного адреса (будет использоваться для webhook)
2. Выбрать docker образ с телеграм ботом
3. Ввести порт (можно любой, рекомендуем 8000)
3. В разделе `Переменные` добавить: BOT_TOKEN=`токен_из_bot_father` 
4. В разделе `Конфигурация` выбрать 0.5 vCPU, чтобы cold start был меньше 
5. `Мин кол-во экземпляров` поставить в 0 (cold start)

## Добавление webhook в telegram 
Чтобы bot получал сообщения из telegram, нужно добавить webhook.
Можно открыть ссылку в браузере.

Шаги:
1. Проверить существуют ли webhook: `https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo`
2. Удалить существующие webhook: `https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook`
3. Добавить новый webhook: `https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={PUBLIC_URL}/{BOT_TOKEN}`

Заменить:
- Вместо `{BOT_TOKEN}` - поставить токен телеграм бота (BotFather)
- Вместо `{PUBLIC_URL}` - поставить публичный адрес (Container Apps)
