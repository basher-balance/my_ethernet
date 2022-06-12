# my_ethernet

## Development

1. Clone this git repository to your local machine.

2. Install ```docker``` and ```docker-compose``` using official documentation.

3. Add user to the docker group to run commands without sudo:
```
  sudo usermod -aG docker $USER
```
4. Create and fill settings in `.env` and `youtube.json`.

5. Go to the project root and run:
```
  docker-compose build
```

```
  docker-compose up
```

6. Create/Apply database migrations:
```
  docker-compose exec web python manage.py makemigrations
```

```
  docker-compose exec web python manage.py migrate
```

7. Create Django superuser in the container (in the second shell):
```
  docker-compose exec web python manage.py createsuperuser
```

8. Run tests (optional):
```
  docker-compose exec web python manage.py test
```

9. Navigate to web `http://localhost:8000` and database panel `http://localhost:5050`.
