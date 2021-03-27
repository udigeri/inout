# # import os
import sqlite3
import requests
from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash, jsonify
from .api.pgs import Pgs

class Web():
    # configuration
    DATABASE = 'flaskr.db'
    SECRET_KEY = 'my_precious'
    USERNAME = 'admin'
    PASSWORD = 'admin'

    def __init__(self, host='0.0.0.0', port=5000, debug=False):
        self.host = host    
        self.port = port
        self.debug = debug
        # scriptdir=os.path.dirname(os.path.abspath(__file__))
        self.flsk = Flask(__name__)
        self.flsk.config.from_object(self)

    def run(self, config, logger):
        self.config = config
        self.logger = logger
        self.pgs = Pgs(self.config)
        self.port = getattr(self.config, "web_port")
        logger.info(f"Web module started on {self.host} :{self.port}")
        self.flsk.run(host=self.host, port=self.port, debug=self.debug)

    def get_cart(self, pp, lpn, amount):
        self.logger.info(f"Get shopping cart for {pp} {lpn} amount {amount}")
        response = self.pgs.get_shopping_cart(pp, lpn, amount)
        self.logger.info(f'get_cart response status code {response.status_code}')
        if response.status_code == 200:
            for cart_item in response.json():
                try:
                    self.logger.info(f'Provided shopping cart {cart_item["cartid"]}')
                except KeyError as err:
                    self.logger.error(err)
        return response

        # task = {"summary": "Take out trash", "description": "" }
        # resp = requests.post('http://localhost:3000/', data=json.dumps(task), )
        # if resp.status_code != 201:
        #     raise ApiError('POST /posts/ {}'.format(resp.status_code))
        # print('Created task. ID: {}'.format(resp.json()["id"]))
