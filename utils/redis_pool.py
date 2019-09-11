import redis

# 抽取封装成模块，全局使用（单例模式，redis_pool.py）
POOL = redis.ConnectionPool(host='localhost', port=6379, max_connections=1000)
