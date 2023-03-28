from aiohttp import web

from models import db, DB_URI
from routes import setup_routes


async def init_app(app):
    await db.set_bind(DB_URI)
    await db.gino.create_all()
    app['db'] = db


app = web.Application()
app.on_startup.append(init_app)
setup_routes(app)

if __name__ == '__main__':
    web.run_app(app, port=8000)
