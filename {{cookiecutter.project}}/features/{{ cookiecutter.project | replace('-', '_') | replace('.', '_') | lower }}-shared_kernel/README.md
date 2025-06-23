# {{ cookiecutter.project | replace('-', '_') | replace('.', '_') | lower }} Shared Kernel #

``` bash
.
├── __init__.py
├── domain OK
│   ├── __init__.py
│   ├── entity.py
│   ├── enum
│   ├── exception.py
│   ├── mixins
│   ├── types
│   ├── user.py
│   └── value_object.py
├── infra
│   ├── cache OK
│   ├── camel_model OK
│   ├── database OK
│   ├── gateway OK
│   ├── mail OK
│   ├── mq OK
│   ├── object_storage OK
│   ├── redis OK
│   ├── settings OK
├── presentation
    ├── __init__.py
    └── rest
```
