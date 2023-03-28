from datetime import datetime

from aiohttp import web

from models import User, db, Transaction


async def hello(request):
    return web.Response(text='Hello, world!')


async def get_user(request):
    data = await request.json()
    name = data['name']

    user_exists = await User.query.where(User.name == name).gino.first()

    if user_exists:
        user = user_exists
    else:
        user = await User.create(name=name, balance=0)

    return web.json_response({
        'id': user.id,
        'name': user.name,
        'balance': str(user.balance),
    }, status=201)


async def get_balance(request):
    date_str = request.rel_url.query.get('date', '')
    user_id = int(request.match_info['id'])
    if not date_str:
        user = await User.query.where(User.id == user_id).gino.first()

        if user is None:
            raise web.HTTPNotFound()

        return web.json_response({'balance': str(user.balance)}, status=200)
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
        print(date)
        balance = await Transaction.select('current_balance').where(
            (Transaction.user_id == user_id) & (Transaction.created_at <= date)).order_by(
            Transaction.created_at.desc()).limit(
            1).gino.scalar()
        print(balance)
        return web.json_response({'balance': str(balance)}, status=200)


async def get_transaction(request):
    uid = request.match_info['id']
    transaction = await Transaction.query.where(uid == uid).gino.first()
    if transaction is None:
        raise web.HTTPNotFound()
    return web.json_response({'type': transaction.type, 'amount': str(transaction.amount)}, status=200)


async def add_transaction(request):
    async with db.transaction():
        data = await request.json()
        user = await User.query.where(User.id == data['user_id']).with_for_update().gino.first()

        amount = abs(float(data['amount']))
        users_balance = float(user.balance)
        trans_type = data['type']
        uid = data['uid']
        new_balance = None

        if trans_type == 'WITHDRAW' and users_balance < amount:
            return web.Response(status=402, text='Insufficient funds')
        if trans_type == 'WITHDRAW':
            new_balance = users_balance - amount
        if trans_type == 'DEPOSIT':
            new_balance = users_balance + amount

        transaction = Transaction(user_id=user.id, type=trans_type, amount=amount, uid=uid, current_balance=new_balance)
        await user.update(balance=new_balance).apply()
        await transaction.create()

        return web.Response(status=200, text=str(user.balance))


app = web.Application()
app.add_routes([web.get('/users/{user_id}/balance/{date}', get_balance)])


def setup_routes(app):
    app.add_routes([
        web.get('/', hello),
        web.post('/v1/user', get_user),
        web.get(r'/v1/user/{id}/balance', get_balance),
        web.post(r'/v1/transaction', add_transaction),
        web.get(r'/v1/transaction/{id}', get_transaction),
    ])
