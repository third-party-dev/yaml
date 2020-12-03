import contextlib

try:
    # python 3
    from urllib.request import urlopen, URLError
except ModuleNotFoundError:
    # python 2
    from urllib2 import urlopen, URLError

from errno import ENOENT


@contextlib.contextmanager
def _open_url(self, url, must_exist):
    try:
        # open the url
        with contextlib.closing(urlopen(url)) as f:
            yield f

    except URLError as e:
        # if it must exist, re-raise the exception
        if must_exist:
            raise

        # get the reason
        e = e.reason

        # if this was not a "file does not exist" error
        # re-raise exception
        if not (isinstance(e, EnvironmentError) and e.errno == ENOENT):
            raise

        yield None
