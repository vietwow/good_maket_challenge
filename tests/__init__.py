import unittest

from webtest import TestApp
from app import app
from preggy import expect

class ClientTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ClientTest, self).__init__(*args, **kwargs)
        app.debug = True
        self.client = TestApp(app)

    def get(self, url, params=None, headers=None, extra_environ=None, status=[200, 201, 400, 401, 403, 404], expect_errors=False, xhr=False):
        self.resp = self.client.get(url, params, headers, extra_environ, status, expect_errors, xhr)
        return self.resp

    def post(self, url, params=u'', headers=None, extra_environ=None, status=[200, 201, 400, 401, 403, 404], upload_files=None, expect_errors=False, content_type=None, xhr=False):
        self.resp = self.client.post(url, params, headers, extra_environ, status, upload_files, expect_errors, content_type, xhr)
        return self.resp

    def put(self, url, params=u'', headers=None, extra_environ=None, status=[200, 201, 400, 401, 403, 404], upload_files=None, expect_errors=False, content_type=None, xhr=False):
        self.resp = self.client.put(url, params, headers, extra_environ, status, upload_files, expect_errors, content_type, xhr)
        return self.resp
    def delete(self,url ,params=u'', headers=None, extra_environ=None, status=[200, 201, 400, 401, 403, 404], expect_errors=False, content_type=None, xhr=False):
        self.resp = self.client.delete(url, params, headers, extra_environ, status, expect_errors, content_type, xhr)
