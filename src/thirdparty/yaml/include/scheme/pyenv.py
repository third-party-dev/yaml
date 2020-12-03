# @contextlib.contextmanager
# def _open_pyenv(self, pkg_resource, must_exist):
#     try:
#         # get the package and resource names
#         pkg_name, resource_name = pkg_resource.split(':', 1)

#     except ValueError:
#         raise ValueError(
#             'expected <pkg>:<resource>, but found %r' % pkg_resource)

#     try:
#         # open the resource
#         with pkg_resources.resource_stream(pkg_name, resource_name) as f:
#             yield f

#     except EnvironmentError as e:
#         # if it must exist, re-raise the exception
#         if must_exist:
#             raise

#         if e.errno != ENOENT:
#             raise

#         yield None

# TODO: Get this in its own module.
# @contextlib.contextmanager
# def _venv_context(self, node):
#     from venvsandbox import virtualenv

#     # get path
#     path = self.construct_scalar(node)

#     # convert to actual path
#     path = self._convert_path(path)

#     # activate virtualenv
#     with virtualenv(path):
#         yield
