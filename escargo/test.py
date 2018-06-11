#!/usr/bin/env python3

"""
The unittests for the API should be set up to closely simulate two email
servers and an email client. Each sender server should be configured to use
different email configurations.

"""

import unittest

from subprocess import call

import os


class MultiDockerTestCase(unittest.TestCase):

    def get_docker_mailserver():
        # Start by setting up a docker mail server
        # https://hub.docker.com/r/tvial/docker-mailserver/
        os.makedirs('/tmp/escargo_tests')
        os.call([])

    def setUp(self):
        self.get_docker_mailserver()


class TestApi(MultiDockerTestCase):

    def setUp(self):
        super(TestApi, self).setUp()
