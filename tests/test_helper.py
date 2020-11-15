import pytest
from octoparse import _get_request, _post_request


class TestHelper:
    """
    Test Helper Functions
    """

    def setup(self):
        """
        Test Setup
        """
        self.base_url = 'https://httpbin.org/'
        self.token = 'dfafasfasfsafafsdsdsdwwedfsgfdsg'

    def test_get_with_params(self):
        """
        Test _get_request with params
        :return:
        """
        params = {
            'arg1': 'val1',
            'arg2': 'val2'
        }

        resp = _get_request(self.base_url + 'get', token=self.token, params=params)
        assert resp['args'] == params

    def test_get_without_params(self):
        """
        Test _get_request without params
        :return:
        """

        resp = _get_request(self.base_url + 'get', token=self.token)
        assert resp['args'] == {}

    def test_post_with_body_with_params(self):
        """
        Test _post_request with body
        :return:
        """
        params = {
            'arg1': 'val1',
            'arg2': 'val2'
        }

        body = {
            'abc': '123',
            'def': '456'
        }

        resp = _post_request(self.base_url + 'post', token=self.token, params=params, body=body)
        assert resp['args'] == params
        assert resp['form'] == body
        assert resp['data'] == ''
        assert resp['files'] == {}

    def test_post_with_body_without_params(self):
        """
        Test _post_request with body
        :return:
        """

        body = {
            'abc': '123',
            'def': '456'
        }
        resp = _post_request(self.base_url + 'post', token=self.token, body=body)
        assert resp['args'] == {}
        assert resp['form'] == body
        assert resp['data'] == ''
        assert resp['files'] == {}

    def test_post_without_body_with_params(self):
        """
        Test _post_request with body
        :return:
        """
        params = {
            'arg1': 'val1',
            'arg2': 'val2'
        }

        resp = _post_request(self.base_url + 'post', token=self.token, params=params)
        assert resp['args'] == params
        assert resp['form'] == {}
        assert resp['data'] == ''
        assert resp['files'] == {}

    def test_post_without_body_without_params(self):
        """
        Test _post_request without body
        :return:
        """

        resp = _post_request(self.base_url + 'post', token=self.token)
        assert resp['args'] == {}
        assert resp['form'] == {}
        assert resp['data'] == ''
        assert resp['files'] == {}
