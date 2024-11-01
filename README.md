# Payroll Management Web Application

## Тестовое задание

Разработать web-приложение для учета заработной платы на предприятии ООО «Р&К».

### Описание

На предприятии есть бухгалтер, который должен иметь возможность регистрировать в системе новых пользователей (логин, пароль) с указанием общей информации о пользователе (ФИО, телефон, фотография, должность) и устанавливать им З/П. Каждый работник, получивший логин/пароль от бухгалтера, должен иметь возможность авторизоваться в системе. Каждый пользователь, авторизованный в системе, должен иметь возможность просмотреть список пользователей и общую информацию о них (ФИО, телефон, фотография, должность) и дополнительно информацию о своей (только своей) З/П. Информация о З/П всех пользователей должна быть доступна только бухгалтеру.

### Технологии

- **Фреймворк**: FastAPI
- **Системы миграций**: Alembic
- **СУБД**: PostgreSQL
- **Драйвер для подключения к БД**: asyncpg
- **Тестирование**: Pytest
- **Клиентская часть**: Vue.js (реализовать по возможности)

### Установка и запуск

Before starting u should create virtual environment with ```poetry shell```

after that install all requirements by: ```poetry install```

- You can launch the app with:
```./start.sh  ```

This command will create an .env file from .env.template and launch app on the ports:
- backend
```http://0.0.0.0:8000/```

- frontend
```http://localhost:8080/```

### Эндпоинты
## Payroll
Создать пользователя
```POST /payroll/```

Получить список пользователей
```GET /payroll/users/```

Обновить пользователя
```PUT /payroll/users/```

Получить информацию о пользователе
```GET /payroll/profile/```

Получить информацию о конкретном пользователе
```GET /payroll/users/{user_id}/```

## Auth
Вход для получения токена доступа
```POST /login/```

Выход из системы
```DELETE /logout/```

## Tasks
List tasks
```GET /tasks/```

Post task
```POST /tasks/```


Get Task
```GET /tasks/{task_id}/```


Update Task
```PATCH /tasks/{task_id}/```


Delete Task
```DELETE /tasks/{task_id}/```





