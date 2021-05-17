from aiohttp import web
import json


# routes = web.RouteTableDef()

redis = {'USD': 1}
# @routes.get('/сonvert')
async def convert(request: web.Request):
    response_obj = converter(request)
    return web.json_response(response_obj)


def converter(request: web.Request):
    from_currency = request.query['from']
    to_currency = request.query['to']
    amount = request.query['amount']

    response_obj = check_for_key([from_currency, to_currency])
    if response_obj:
        return response_obj

    response_obj = check_for_amount(amount)
    if response_obj:
        return response_obj

    amount = int(amount)

    if to_currency == 'USD':
        converted_amount = amount / redis[from_currency]
        return {'amount': converted_amount, 'status': 200}
    if from_currency == 'USD':
        converted_amount = amount * redis[to_currency]
        return {'amount': converted_amount, 'status': 200}
    converted_amount = amount / redis[from_currency] * redis[to_currency]
    return {'amount': converted_amount, 'status': 200}

def check_for_key(keys):
    if keys[0] not in redis.keys() or keys[1] not in redis.keys():
        return {'status': 400, 'reason': 'unknown currency'}

def check_for_amount(amount):
    try:
        int(amount)
    except ValueError:
        return {'status': 400, 'reason': 'amount need to be a number'}

# @routes.post('/database')

async def database(request):
    response_obj = await fulfill_database(request)
    return web.json_response(response_obj)

async def fulfill_database(request: web.Request):
    is_merge = int(request.query['merge'])
    if is_merge == 1:
        try:
            data = await request.json()
        except json.decoder.JSONDecodeError as e:
            return {'status': 400, 'reason': str(e)}
        redis.update(data)
        return {'status': 200}
    elif is_merge == 0:
        redis.clear()
        redis.update({'USD': 1})
        return {'status': 200}
    else:
        return {'status': 400, 'reason': 'merge should be 1 or 0'}

app = web.Application()
app.add_routes([web.get('/convert', convert), web.post('/database', database)])
web.run_app(app)