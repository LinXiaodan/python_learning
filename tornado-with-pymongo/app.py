#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-22
# Author: LXD

from tornado import httpserver, ioloop, web
import os
import pymongo
import logging
logging.basicConfig(level=logging.INFO)

# 监听端口定义
# define("port", default=8000, help="run on the given port", type=int)


class Application(web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/blog", BlogHandler),
            (r".*", OtherHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )

        conn = pymongo.MongoClient("localhost", 27017)
        self.db = conn.demodb
        web.Application.__init__(self, handlers, **settings)


class MainHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")


class BlogHandler(web.RequestHandler):
    def get(self):
        coll = self.application.db.blog
        blog = coll.find_one()
        if blog:
            self.render(
                "blog.html",
                page_title=blog['title'],
                blog=blog,
            )
        else:
            self.redirect('/')


class OtherHandler(web.RequestHandler):
    def get(self):
        self.write("404")

    def post(self, *args, **kwargs):
        self.write("404")


def main():
    server = httpserver.HTTPServer(Application())
    server.listen(9000)
    logging.info('server is listening at 9000...')
    ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()