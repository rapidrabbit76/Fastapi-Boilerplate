# Fastapi-Boilerplate

this repo based on teamhide's [fastapi-boilerplate](https://github.com/teamhide/fastapi-boilerplate)



# Install

```bash
pip install cookiecutter
```
```bash
cookiecutter https://github.com/rapidrabbit76/Fastapi-Boilerplate.git [--checkout branch: is option]
```


# Features
 - [X] cookicutter 
 - [X] cache-control middleware
 - [X] cache
 - [X] containerize
 - [ ] middleware logging
 - [X] SQLAlchemy Multiple database
 - [ ] starlette-admin


## Cache-control
TODO 

## cache
cache depends on [aiocache](https://github.com/aio-libs/aiocache)


## SQLAlchemy Multiple database

check ```core/db/session.py``` and ```core/settings/settings.py```
- set ```DB_AUTH_DB_URL```


```python
engines = {
    "writer": create_async_engine(
        env.DB_WRITER_DB_URL,
        pool_recycle=env.DB_POOL_RECYCLE,
        echo=env.DB_ECHO,
    ),
    "reader": create_async_engine(
        env.DB_READER_DB_URL,
        pool_recycle=env.DB_POOL_RECYCLE,
        echo=env.DB_ECHO,
    ),
    "auth": create_async_engine(
        env.DB_AUTH_DB_URL,
        pool_recycle=env.DB_POOL_RECYCLE,
        echo=env.DB_ECHO,
    ),
}
```

add ```__bind_key__ ``` metadata in orm models to identify databases.

```python
class Model(Base):
    __tablename__ = "TABLE_NAME"
    __bind_key__ = "auth" 
```
DB routing is performed according to the bind_key information in the ```get_bind()``` method of ```RoutingSession```. If additional logic is needed, refer to RoutingSession in ```core/db/session.py``` and modify it.



## starlette-admin
refer the repo of [starlette-admin](https://github.com/jowilf/starlette-admin)




# References
- [teamhide/fastapi-boilerplate](https://github.com/teamhide/fastapi-boilerplate)
- [arthurhenrique/cookiecutter-fastapi](https://github.com/arthurhenrique/cookiecutter-fastapi)
- [aiocache](https://github.com/aio-libs/aiocache)
- [starlette-admin](https://github.com/jowilf/starlette-admin)