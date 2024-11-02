# Payroll App

### Description

At the company, there is an accountant who must be able to register new users in the system (login, password) with the provision of general information about the user (full name, phone number, photo, position) and set their salary. Each employee who receives a login/password from the accountant must be able to log in to the system. Each user logged into the system must be able to view the list of users and general information about them (full name, phone number, photo, position) and additionally view information about their (only their) salary. Information about the salaries of all users should be accessible only to the accountant.

Additionally, the application includes functionality for task management, allowing users to create, update, and delete tasks, as well as view a list of all tasks. Users cant make an task for admin user, user can delete only tasks that he or she created  but the admin can delete all tasks

### Technologies

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Alembic](https://img.shields.io/badge/Alembic-4B4B4B?style=flat&logo=python&logoColor=white)](https://alembic.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![asyncpg](https://img.shields.io/badge/asyncpg-3B2B2B?style=flat&logo=python&logoColor=white)](https://github.com/MagicStack/asyncpg)
[![Pytest](https://img.shields.io/badge/Pytest-DAA520?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org/en/stable/)
[![Vue.js](https://img.shields.io/badge/Vue.js-42b883?style=flat&logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)

### Installation and Launch

Before starting u should create virtual environment with 
```
poetry shell
```

after that install all requirements by: 
```
poetry install
```

Now u can launch the app with:
```
./start.sh
```

This command will create .env file from .env.template and launch the app on the ports:
- backend
```http://0.0.0.0:8000/```

- frontend
```http://localhost:8080/```


```./loopback_full``` *if some ports are unavailabe*

## Testing
to start tests:
```
pytest -x
```

## Admin

You can create superuser in the console:
```
python src/utils/csu.py
```

*if u have problems with imports*:
paste ```export PYTHONPATH=src``` in your console

### Endpoints
## Payroll
Create user
```POST /payroll/```

Get users list
```GET /payroll/users/```

Update user data
```PUT /payroll/users/```

Get current user's data
```GET /payroll/profile/```

Get user's data
```GET /payroll/users/{user_id}/```

## Auth
Login to Obtain Access Token
```POST /login/```

Logout
```DELETE /logout/```

## Tasks
List tasks
```GET /tasks/```

Create task
```POST /tasks/```


Get Task
```GET /tasks/{task_id}/```


Update Task
```PATCH /tasks/{task_id}/```


Delete Task
```DELETE /tasks/{task_id}/```

*:)*
