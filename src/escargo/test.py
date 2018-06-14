#!/usr/bin/env python3

import os
import unittest
import json
import logging

from escargo.main import app

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
ASSETS = os.path.join(ROOT, 'assets')
TEST_ASSETS = os.path.join(ASSETS, 'tests')
EXAMPLE_JSON = os.path.join(TEST_ASSETS, 'example.json')
CONFIG_JSON = os.path.join(TEST_ASSETS, 'config.json')


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TestApi(unittest.TestCase):
    """ Test case for the API. """

    def setUp(self): # NOQA
        """
        Check for existence of `../../assets/test/config.json` and create flask
        test client.
        """
        if not os.path.exists(CONFIG_JSON):
            msg = '{} not found. Please copy {} to {} and modify.'.format(
                CONFIG_JSON, EXAMPLE_JSON, CONFIG_JSON,
            )
            raise OSError(msg)
        with open(CONFIG_JSON) as config_json:
            self.config = json.load(config_json)
        logger.debug("{} bytes read from json config".format(
            len(str(self.config))
        ))
        logger.debug(self.config)

        self.client = app.test_client()

    def test_api(self):
        with app.app_context():
            resp = self.client.post('/', data=json.dumps(self.config),
                                    content_type='application/json')
            logger.info(resp.json)
            self.assertEqual(resp.status_code, 200)
