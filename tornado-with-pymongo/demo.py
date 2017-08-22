#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-22
# Author: LXD

import json
import logging

import pymongo
from pymongo import MongoClient
from tornado import ioloop, web

logging.basicConfig(level=logging.INFO)


class MainHandler(web.RequestHandler):
    def get(self):
        body = 'Hello world!'
        # self.write("Hello world!<br>")
        conn = MongoClient(host="localhost", port=27017)
        db = conn.demodb
        find_result = db.demotable.find()
        if find_result.count() == 0:
            body = '\n'.join([body, 'count is 0'])
            # self.write('count is 0')
            db.demotable.insert({'name': 'a', 'id': 1})
        else:
            for item in find_result.sort('id', pymongo.DESCENDING):
                item.pop('_id')
                logging.info(item)
                body = '\n'.join([body, json.dumps(item, indent=4)])
                # self.write(json.dumps(item, indent=4).replace('\n', '<br>'))
                # self.write('<br>')
            body = body.replace('\n', '<br>').replace(' ', '&nbsp')
            self.write(body)
        conn.close()


if __name__ == '__main__':
    app = web.Application([(r"/", MainHandler)])
    app.listen(9000)
    logging.info('app is listening at 9000...')
    ioloop.IOLoop.current().start()
    # a = {
    #     'a': '1',
    #     'b': '2'
    # }
    # logging.info(type(a))
    # b = json.dumps(a)
    # logging.info(type(b))