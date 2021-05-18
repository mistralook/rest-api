from aiohttp import web
import json
import aioredis

async def convert(request: web.Request):
    response_obj = await converter(request)
    return web.json_response(response_obj)


async def converter(request: web.Request):
    redis = request.app['redis']

    from_currency = request.query['from']
    to_currency = request.query['to']
    amount = request.query['amount']

    keys = await redis.mget(from_currency, to_currency)

    response_obj = check_for_key(keys)
    if response_obj:
        return response_obj

    response_obj = check_for_amount(amount)
    if response_obj:
        return response_obj

    amount = int(amount)
    from_currency = float(keys[0])
    to_currency = float(keys[1])

    if to_currency == 'USD':
        converted_amount = amount / from_currency
        return {'amount': float(f'{converted_amount:.2f}'), 'status': 200}
    if from_currency == 'USD':
        converted_amount = amount * to_currency
        return {'amount': float(f'{converted_amount:.2f}'), 'status': 200}
    converted_amount = amount / from_currency * to_currency
    return {'amount': float(f'{converted_amount:.2f}'), 'status': 200}


def check_for_key(keys):
    if keys[0] is None or keys[1] is None:
        return {'status': 400, 'reason': 'unknown currency'}


def check_for_amount(amount):
    try:
        int(amount)
    except ValueError:
        return {'status': 400, 'reason': 'amount need to be a number'}


async def database(request):
    response_obj = await fulfill_database(request)
    return web.json_response(response_obj)


async def fulfill_database(request: web.Request):
    redis = request.app['redis']
    print(redis, flush=True)
    is_merge = int(request.query['merge'])
    if is_merge == 1:
        try:
            data = await request.json()
        except json.decoder.JSONDecodeError as e:
            return {'status': 400, 'reason': 'malformed json', 'problem': str(e)}
        await redis.mset(data)
        return {'status': 200}
    elif is_merge == 0:
        await redis.flushdb()
        await redis.set('USD', 1)
        return {'status': 200}
    else:
        return {'status': 400, 'reason': 'merge should be 1 or 0'}


async def app_initialize():
    app = web.Application()
    app.add_routes(
        [web.get('/convert', convert), web.post('/database', database)])
    redis = await aioredis.create_redis(('redis', 6379))
    await redis.set('USD', 1)
    app['redis'] = redis
    return app


web.run_app(app_initialize())
