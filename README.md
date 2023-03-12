# Githance backend

##### Run local server with docker-compose
You will need a **.env** file in **infra/deploy_local/** directory.
See the **/infra/deploy_local/.env.local.example** file.

Сontainers will be up:
1. postgresql
2. nginx, which listen 80 port
3. backend, which rebuilding with actual code
```
make up
```

Make migrations + collect static files:
```
make migrate
```

Create superuser:
```
make createsuperuser
```