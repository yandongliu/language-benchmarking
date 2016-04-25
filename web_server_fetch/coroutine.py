import requests

from tornado import gen
import tornado.ioloop
import tornado.web

LISTEN_PORT = 8080


def urls_to_check():
    return [
        'http://google.com',
        'http://wikipedia.org',
        'http://amazon.com',
    ]


@gen.coroutine
def check_status(url):
    try:
        raise gen.Return(requests.get(url).status_code)
    except gen.Return:
        raise
    except Exception as e:
        raise gen.Return(('error', str(e)))


class StatusCheckHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        statuses = {}
        for url in urls_to_check():
            statuses[url] = yield check_status(url)
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
