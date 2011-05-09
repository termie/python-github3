import json
import UserDict

from github3 import request
from github3 import resource


def _resource_factory(client, data):
  """Helper function for mapping responses into Resources."""
  return resource.Resource(client, data.get('url'), data)


class Client(request.Request):
  def repo(self, user, repo_):
    return Repo(client=self, user=user, repo=repo_)


class Repo(object):
  BASE_URL = "https://api.github.com/repos"

  def __init__(self, client, user, repo):
    self.client = client
    self.user = user
    self.repo = repo

  def issues(self, **kw):
    """Return a PaginatedResourceList of issues."""
    url = '%s/%s/%s/issues' % (self.BASE_URL, self.user, self.repo)
    resp = self.client.get(url, **kw)
    return resource.PaginatedResourceList.FromResponse(self.client, resp)

  def issue(self, id_):
    """Return a Resource of an issue."""
    url = '%s/%s/%s/issues/%s' % (self.BASE_URL, self.user, self.repo, id_)
    resp = self.client.get(url)
    return resource.Resource(self.client, url, json.loads(resp.read()))

  def milestones(self, **kw):
    """Return a PaginatedResourceList of milestones."""
    url = '%s/%s/%s/milestones' % (self.BASE_URL, self.user, self.repo)
    resp = self.client.get(url, **kw)
    return resource.PaginatedResourceList.FromResponse(self.client, resp)

  def labels(self, **kw):
    """Return a PaginatedResourceList of labels."""
    url = '%s/%s/%s/labels' % (self.BASE_URL, self.user, self.repo)
    resp = self.client.get(url, **kw)
    return resource.PaginatedResourceList.FromResponse(self.client, resp)

  def comments(self, issue, **kw):
    """Return a PaginatedResourceList of comments for an issue."""
    url = '%s/%s/%s/issues/%s/comments' % (
        self.BASE_URL, self.user, self.repo, issue)
    resp = self.client.get(url, **kw)
    return resource.PaginatedResourceList.FromResponse(self.client, resp)


