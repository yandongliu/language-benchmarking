from tornado import gen
import tornado.ioloop
import tornado.web

LISTEN_PORT = 8080


class StatusCheckHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def do_work(self, num):
        sum = 0
        for i in xrange(num):
            sum += i
        return sum

    @gen.coroutine
    def get(self):
        statuses = {}
        nums= [
            10000,
            100000,
            1000000,
        ]
        status_futures = {
            str(num): self.do_work(num) for num in nums
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
