# githance_backend

## Developer environment

You can run simple server or run docker-compose dev stand.

##### Run dev server with sqlite db:
```
python manage.py runserver
```

##### Run docker-compose dev stand 
You will need a **.env** file in **infra/deploy_local/** directory.
See the **/infra/deploy_local/.env.local.example** file.

Сontainers will be up:
1. postgresql
2. nginx, which listen 80 port
3. backend, which rebuilding with actual code
```
make up_local
```

Making migrations + loading static files + creating superuser:
```
make fill_local
```