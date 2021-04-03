# # import os
import sqlite3
import requests
from requests.auth import HTTPBasicAuth
import json
from flask import Flask
from .api.pgs import Pgs
from .api.transaction import Transaction

class Web():
    SECRET_KEY = 'my_precious'

    def __init__(self, host='0.0.0.0', port=80, debug=False):
        self.host = host
        self.port = port
        self.debug = debug
        self.username = None
        self.password = None
        self.flsk = Flask(__name__)
        self.flsk.config.from_object(self)
        self.trxs = []

    def run(self, config, logger):
        self.config = config
        self.logger = logger
        self.pgs = Pgs(self.config, self.logger)
        self.port = getattr(self.config, "web_port")
        logger.info(f"Web module started on {self.host} :{self.port}")
        # http
        self.flsk.run(host=self.host, port=self.port, debug=self.debug)
        # https
        # self.flsk.run(host=self.host, port=self.port, debug=self.debug, ssl_context='adhoc')

    def _getAuthenticationURL(self):
        return self.pgs._getHost()

    def getAuthentication(self, usr, pwd):
        self.username = usr
        self.password = pwd

        error = None
        self.pgs.setAuth(HTTPBasicAuth(usr, pwd))
        try:
            rsp = requests.get(self._getAuthenticationURL(), auth=HTTPBasicAuth(usr, pwd))
        except Exception as err:
            error = "Authentication failed {}".format(err)
            self.logger.error(error)
        if rsp.status_code != 404:
            error = "Authentication failed Status code {} {}".format(rsp.status_code, self._getAuthenticationURL())
            self.logger.warning(error)
        else:
            self.logger.info("Web Authentication success")
        return error

    def get_cart(self, pp, lpn, amount):
        self.logger.info(f"Web shopping cart for {pp} {lpn} amount {amount}")
        trx = Transaction(pp, lpn, amount)
        trx = self.pgs.get_shopping_cart(trx)
        data = json.loads(trx.rsp_text)
        if trx.rsp_status_code == 200:
            for key in data:
                if key == 'cartId':
                    trx.shoppingCartUuid = data[key]
                    self.logger.info('Provided shopping cart {cartId}'.format(cartId=data[key])) 
                    self.trxs.append(trx)
        else:
            for key in data:
                if key == 'code':
                    trx.rsp_code = data[key]
                elif key == 'status':
                    trx.rsp_status = data[key]
        return trx

    def get_pay_methods(self, trx):
        self.logger.info(f"Web pay methods for {trx.shoppingCartUuid}")
        trx = self.pgs.get_payment_methods(trx)

        if trx.rsp_status_code == 200:
            data = json.loads(trx.rsp_text)
            trx.trx_methods = [y[z] for x in data for y in data[x] for z in y if x=='offeredPaymentTypes' if z=='name']
            trx.trx_urls = [y[z] for x in data for y in data[x] for z in y if x=='offeredPaymentTypes' if z=='formUrl']
            trx.trx_fees = [y[z] for x in data for y in data[x] for z in y if x=='offeredPaymentTypes' if z=='fee']
            for id in range(len(trx.trx_methods)):
                self.logger.info(f'{trx.trx_methods[id]} {trx.trx_fees[id]} {trx.trx_urls[id]}')
        return trx
