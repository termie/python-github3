import unittest
import urllib2
import StringIO

from github3 import request


class OpenerInterceptor(object):
  """Pretty close to a mock opener."""

  def __init__(self, opener):
    self.opener = opener
    self._pre = []
    self._raises = None
    self._returns = None

  def pre(self, f, *args, **kw):
    """Run some function before processing the request."""
    self._pre.append((f, args, kw))

  def returns(self, body, headers=None, status=200):
    self._returns = dict(body=body, headers=headers, status=status)

  def raises(self, exc):
    self._raises = exc

  def errors(self, body, url=None, headers=None, status=403):
    fp = StringIO.StringIO(body)
    exc = urllib2.HTTPError(url, status, msg, headers, fp)

  def open(self, req):
    for f, args, kw in self._pre:
      f(req, *args, **kw)

    if self._raises:
      raise self._raises
    return self._returns


class RequestTestCase(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def _intercept(self, req):
    opener = OpenerInterceptor(req._opener)
    req._opener = opener
    return opener

  def test_basic_auth(self):
    req = request.Request('foo', 'bar')

    b64_userpass = request.basic_auth('foo', 'bar')

    opener = self._intercept(req)

    def check_auth(req):
      self.assertEqual(req.headers['Authorization'], 'Basic %s' % b64_userpass)

    opener.pre(check_auth)

    req.post('some_url')
