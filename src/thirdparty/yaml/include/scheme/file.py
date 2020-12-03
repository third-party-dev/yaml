import contextlib
import os
import posixpath

from errno import ENOENT


def _convert_path(self, path):

    # convert the path to a native path
    path = path.replace(posixpath.sep, os.path.sep)

    # if path is relative, prepend the current file's directory
    if (
        not isinstance(self.loader.reader.stream, (bytes, str))
        and not os.path.isabs(path)
        and path.partition(os.path.sep)[0] != os.path.curdir
    ):
        # prepend the current file's directory to the path
        path = os.path.join(
            os.path.dirname(self.loader.reader.stream.name), path
        )

    return path


#! BUG: This code assumes that the currently processes yaml
#!      is being read from a file when it could come from a
#!      hard coded string in python code. In the latter case
#!......this will cause the code to throw an unhandled exception.
# * Included as implicit scheme
@contextlib.contextmanager
def _open_file(self, path, must_exist):
    # convert to actual path

    path = _convert_path(self.yaml, path)

    try:
        # open the file
        with open(path, "rb") as f:
            yield f
    # catch any IO or OS errors
    except EnvironmentError as e:
        # if it must exist, re-raise the exception
        if must_exist:
            raise

        # if this was not a "file does not exist" error, re-raise exception
        if e.errno != ENOENT:
            raise

        yield None
