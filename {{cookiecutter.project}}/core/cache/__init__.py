from aiocache import caches, Cache,cached
from aiocache.serializers import PickleSerializer
from core.settings import env

import yaml

with open(env.CACHE_CONFIG_FILE_PATH) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    if env.CACHE_ALIAS == "redis_local":
        config[env.CACHE_ALIAS]["endpoint"] = env.CACHE_REDIS_HOST
        config[env.CACHE_ALIAS]["port"] = env.CACHE_REDIS_PORT
    caches.set_config(config)
