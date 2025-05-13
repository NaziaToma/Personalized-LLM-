# Command Reference

Create Django project with Docker Compose:

```sh
docker compose run --rm backend sh -c "django-admin startproject backend ."
```

Start the development server:

```sh
docker compose up --watch --build
```
