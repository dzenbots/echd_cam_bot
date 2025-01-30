# Бот для получения изображений с IP-камер, установленных в кабинетах информатики для диагностик

## Запуск бота

1. Переименовываем файл ```.env.dist``` в ```.env``` или создаем новый файл ```.env``` и копируем содержимое файла ```.env.dist```.
2. Создаем бота в Telegram с помощью [BotFather](https://t.me/BotFather)
3. В файле ```.env``` задаем значение переменной ```BOT_TOKEN``` (токен берем из шага 2)
4. Получаем ваш ID в Telegram, например, у [Get My ID](https://t.me/getmyid_bot). Копируем этот ID в переменную ```ADMINS```. Через запятую можно указать все ID пользователей, которым нужно дать разрешение на использование бота.
5. Все готово! Дальше либо создаем виртуальное окружение, либо нет, устанавливаем библиотеки с помощью ```pip install -r requirements.txt``` и запускаем бота с помощью ```python app.py```.

В боте есть команды для добавления и удаления камер. Заполняем аккуратно все что просит бот. Эти настройки сохранятся в файле ```config.ini``` для последующих перезагрузок. Можно добавить пару камер руками через бота а остальные по аналогии добавить уже в сам файл и перезапустить бот, если камер много.
