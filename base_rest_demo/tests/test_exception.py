# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json

import openerp.tests.common
import openerp.tools
from openerp.addons.base_rest.tests.common import RegistryMixin
from openerp.tests import HttpCase


@openerp.tests.common.at_install(False)
@openerp.tests.common.post_install(True)
class TestException(HttpCase, RegistryMixin):

    @classmethod
    def setUpClass(cls):
        super(TestException, cls).setUpClass()
        cls.setUpRegistry()
        host = '127.0.0.1'
        port = openerp.tools.config['xmlrpc_port']
        cls.url = 'http://%s:%d/base_rest_demo_api/public/exception' % (
            host, port)

    def setUp(self):
        super(TestException, self).setUp()
        self.opener.addheaders.append(('Content-Type', 'application/json'))

    @openerp.tools.mute_logger('openerp.addons.base_rest.http')
    def test_user_error(self):
        response = self.url_open('%s/user_error' % self.url, "{}")
        self.assertEqual(response.code, 400)
        self.assertEqual(response.headers['content-type'], 'application/json')
        body = json.loads(response.fp.read())
        self.assertDictEqual(
            body,
            {"code": 400,
             "name": "Bad Request",
             "description": "<p>UserError message</p>"}
        )

    @openerp.tools.mute_logger('openerp.addons.base_rest.http')
    def test_validation_error(self):
        response = self.url_open('%s/validation_error' % self.url, "{}")
        self.assertEqual(response.code, 400)
        self.assertEqual(response.headers['content-type'], 'application/json')
        body = json.loads(response.fp.read())
        self.assertDictEqual(
            body,
            {"code": 400,
             "name": "Bad Request",
             "description": "<p>ValidationError message</p>"}
        )

    @openerp.tools.mute_logger('openerp.addons.base_rest.http')
    def test_session_expired(self):
        response = self.url_open('%s/session_expired' % self.url, "{}")
        self.assertEqual(response.code, 401)
        self.assertEqual(response.headers['content-type'], 'application/json')
        body = json.loads(response.fp.read())
        self.assertDictEqual(
            body,
            {"code": 401,
             "name": "Unauthorized"}
        )

    @openerp.tools.mute_logger('openerp.addons.base_rest.http')
    def test_missing_error(self):
        response = self.url_open('%s/missing_error' % self.url, "{}")
        self.assertEqual(response.code, 404)
        self.assertEqual(response.headers['content-type'], 'application/json')
        body = json.loads(response.fp.read())
        self.assertDictEqual(
            body,
            {"code": 404,
             "name": "Not Found"}
        )

    @openerp.tools.mute_logger('openerp.addons.base_rest.http')
    def test_access_error(self):
        response = self.url_open('%s/access_error' % self.url, "{}")
        self.assertEqual(response.code, 403)
        self.assertEqual(response.headers['content-type'], 'application/json')
        body = json.loads(response.fp.read())
        self.assertDictEqual(
            body,
            {"code": 403,
             "name": "Forbidden"}
        )

    @openerp.tools.mute_logger('openerp.addons.base_rest.http')
    def test_access_denied(self):
        response = self.url_open('%s/access_denied' % self.url, "{}")
        self.assertEqual(response.code, 403)
        self.assertEqual(response.headers['content-type'], 'application/json')
        body = json.loads(response.fp.read())
        self.assertDictEqual(
            body,
            {"code": 403,
             "name": "Forbidden"}
        )

    @openerp.tools.mute_logger('openerp.addons.base_rest.http')
    def test_http_exception(self):
        response = self.url_open('%s/http_exception' % self.url, "{}")
        self.assertEqual(response.code, 405)
        self.assertEqual(response.headers['content-type'], 'text/html')
        body = response.fp.read()
        self.assertIn('Method Not Allowed', body)

    @openerp.tools.mute_logger('openerp.addons.base_rest.http')
    def test_bare_exception(self):
        response = self.url_open('%s/bare_exception' % self.url, "{}")
        self.assertEqual(response.code, 500)
        self.assertEqual(response.headers['content-type'], 'application/json')
        body = json.loads(response.fp.read())
        self.assertDictEqual(
            body,
            {"code": 500,
             "name": "Internal Server Error"}
        )
