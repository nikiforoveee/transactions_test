# questions
1)учесть, что архитектура должна гарантировать обработку транзакции ровно 1 раз. Какие требования это накладывает на сам сервис и соседние сервисы?

2)описать (можно не реализовывать), как можно реализовать уведомление других сервисов о транзакциях. Например, уведомить рекламный движок, который работает при наличии средств на счету.

3)тезисно перечислить, какие инструменты можно применить для контроля качества работы сервиса

4)гарантировать, что баланс пользователя не может быть отрицательным

# answers
1).with_for_update() (routes.py 62 строка) этот код гарантирует обработку транзакции только 1 раз, тк блокирует
строку содержащую баланс пользователя для команд (select,update,delete) в других запросах , в других сервисах нужно учесть, 
что в момент проведения транзакции все запросы касающиеся этой строки будут невозможны

2)можно использовать rabbitmq , или просто писать логи в базу, которую мониторить рекламный движок

3)добавить валидацию входных данных и обработку все-возможных ошибок, тесты под нагрузкой

4)(routes.py 71 строка) стоит проверка

# commands
docker build -t my_app .
docker-compose up
http://0.0.0.0:8000
