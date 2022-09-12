from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

from config import get_settings
from handlers import *

settings = get_settings()

application = Application(
    [
        (r'/api/(?P<param>[^\/]+)', ApiHandler),
        (r'/', ClientWsHandler),
        (r'/runner', RunnerWsHandler),
        (r'/tasks', TasksWsHandler),
    ]
)

if __name__ == "__main__":
    http_server = HTTPServer(application)
    http_server.listen(settings.PORT)

    print(f'Websocket/API Server Started on port: {settings.PORT}')
    IOLoop.instance().start()
