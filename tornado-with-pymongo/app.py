#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-22
# Author: LXD

import time
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

    def post(self, *args, **kwargs):
        title = self.get_argument('title', None)
        content = self.get_argument('content', None)
        if title and content:
            blog = {
                'title': title,
                'content': content,
                'date': int(time.time())
            }
            coll = self.application.db.blog
            coll.insert(blog)
            self.redirect('/blog')
        self.redirect('/')


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
    server.listen(8080)
    logging.info('server is listening at 8080...')
    ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()