# githance_backend

## Developer environment

You can run simple server or run docker-compose dev stand.

##### Run dev server with sqlite db:
```
python manage.py runserver
```

##### Run docker-compose dev stand 
You will need a **.env** file in **infra/** directory.
See the **/infra/.env.example** file.

Сontainers will be launched:
1. postgresql
2. nginx, which listen 80 port
3. backend, which rebuilding with actual code
```
1. cd infra
2. docker-compose -f docker-compose_dev.yaml up -d --build
```
###### Useful commands

Making migrations:
```
 docker-compose -f docker-compose_dev.yaml exec backend python manage.py migrate
 ```

Unloading static files:
```
 docker-compose -f docker-compose_dev.yaml exec backend python manage.py collectstatic --no-input
```

Creating superuser:
```
infra macbookpro$ docker-compose -f docker-compose_dev.yaml exec backend python manage.py createsuperuser
```