import requests

import tornado.ioloop
import tornado.web

LISTEN_PORT = 8080


def urls_to_check():
    return [
        'http://google.com',
        'http://yahoo.com',
        'http://amazon.com'
    ]


def check_status(url):
    try:
        return requests.get(url).status_code
    except Exception as e:
        return ('error', str(e))


class StatusCheckHandler(tornado.web.RequestHandler):

    def get(self):
        statuses = {}
        for url in urls_to_check():
            statuses[url] = check_status(url)
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
