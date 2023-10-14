# Запуск приложения

Для запуска приложения необходимо 
1) В папке api/data создать файл .env

```
db_host = 
db_port = 
db_login = 
db_password =
db_name =

jwt_secret = random_string
jwt_algorithm = HS256

hash_salt = random_string
```

Желательно использовать postgres в качестве БД
jwt_secret должен совпадать с jwt_secret, который в auth api и deliveryman api

2) Установить docker
3) Ввести команду
`docker compose up --build -d`

После этого приложение поднимется на порту 8000