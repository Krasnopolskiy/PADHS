# НИЯУ МИФИ. Лабораторная работа №4. Краснопольский Иван, Б21-525. 2023

## Предметная область

Система получения данных с Etherscan, предназначенная для загрузки исходного кода смарт-контракта на основе адреса
контракта.

### Процесс взаимодействия

1. Взаимодействие начинается с отправки пользователем запроса на API сервер, включающего адрес контракта
2. Сервер регистрирует запрос, записывая контракт в базу данных и назначая ему статус `CREATED`, после чего контракт
   перенаправляется в очередь для обработки
3. Модуль парсинга последовательно обрабатывает контракты из очереди. Модуль присваивает контракту статус `PROCESS` и,
   завершив работу, обновляет статус контракта в базе данных на `SUCCESS`. Если в процессе обработки произошла ошибка,
   статус контракта устанавливается `ERROR`
4. Пользователь имеет возможность отправить запрос на API для получения информации о статусе обработки. После завершения
   обработки доступна загрузка кода контракта

### Параметры работы системы

- Стандартная интенсивность трафика составляет 100 RPS
- В периоды пиковых нагрузок интенсивность может достигать 1000 RPS

### Технологический стек

- FastAPI - бэкенд
- MySQL - СУБД
- RabbitMQ - брокер сообщений

Выбор RabbitMQ обусловлен его способностью эффективно управлять очередями обработки без избыточной сложности,
необходимой для масштабирования системы в Kafka, чье применение в данном контексте представляется излишним.