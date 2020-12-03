# import pytest
from thirdparty.yaml.overlay import YamlOverlay
# from pkg_resources import resource_filename
# import inspect
# from ruamel.yaml.compat import ordereddict

# https://yaml.org/spec/1.2/spec.html

TESTPKG = "thirdparty.yaml.tests"

yaml_overlay = YamlOverlay()

# from io import StringIO
# with StringIO() as string_stream:
#     obj = xyaml.load(source)
#     xyaml.dump(obj, string_stream)

#     pprint(obj)
#     print(string_stream.getvalue())


def test_empty_yaml_load():
    obj = yaml_overlay.load("")
    assert obj is None
