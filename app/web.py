# # import os
# import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash, jsonify

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
        self.port = getattr(config, "web_port")
        logger.debug(f"Web module started on {self.host} :{self.port}")
        self.flsk.run(host=self.host, port=self.port, debug=self.debug)   
        pass
