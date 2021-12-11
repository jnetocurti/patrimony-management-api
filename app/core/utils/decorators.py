import functools

from app.core import connection


def transactional(func):

    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with connection.instance.session() as session:
            async with session.start_transaction():
                return await func(self, *args, **kwargs)

    return wrapper
