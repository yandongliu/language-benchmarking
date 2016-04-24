from tornado import gen
from tornado.httpclient import AsyncHTTPClient
import tornado.ioloop
import tornado.web

LISTEN_PORT = 8080


def urls_to_check():
    return [
        'http://google.com',
        'http://yahoo.com',
        'http://amazon.com',
    ]


class StatusCheckHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def check_status(self, url):
        client = AsyncHTTPClient()
        try:
            response = yield client.fetch(url)
        except Exception as e:
            raise gen.Return(('error', str(e)))
        raise gen.Return(response.code)

    @gen.coroutine
    def get(self):
        statuses = {}
        status_futures = {
            url: self.check_status(url) for url in urls_to_check()
        }
        statuses = yield status_futures
        self.write(statuses)


def get_app():
    return tornado.web.Application([
        (r'/', StatusCheckHandler),
    ], debug=True, autoreload=True)

if __name__ == '__main__':
    app = get_app()
    app.listen(LISTEN_PORT)
    print('Listening on port {}'.format(LISTEN_PORT))
    tornado.ioloop.IOLoop.current().start()
