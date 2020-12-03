# * Included as implicit format
import re
from ruamel.yaml.constructor import ConstructorError
import os
from future.utils import raise_from

import thirdparty.yaml.include.format.yaml
import thirdparty.yaml.include.format.verbatim

import thirdparty.yaml.include.scheme.file
import thirdparty.yaml.include.scheme.url

# This should be treated as a constant.
_include_suffix_re = re.compile(
    "^(-(?P<scheme>[\\w-]+))?(:(?P<format>[\\w-]+))?$"
)


class IncludeHandler(object):
    def __init__(self, yaml):
        self.yaml = yaml
        self._include_formats = {}
        self._include_schemes = {
            # "file": _open_file,
            # 'pyenv': _open_pyenv,
            # 'url': _open_url,
        }

    def register_include_format(self, format, handler):
        self._include_formats[format] = handler

    def register_include_scheme(self, scheme, handler):
        self._include_schemes[scheme] = handler

    def _include(self, constructor, suffix, node, must_exist):
        # parse the suffix
        suffix_match = _include_suffix_re.match(suffix)
        if suffix_match is None:
            raise ConstructorError(
                problem='invalid include tag suffix "%s"' % suffix,
                problem_mark=node.start_mark,
            )

        # get the scheme
        scheme = suffix_match.group("scheme")
        if scheme is None:
            scheme = "file"
        elif scheme not in self._include_schemes:
            raise ConstructorError(
                problem='unsupported include scheme "%s"' % scheme,
                problem_mark=node.start_mark,
            )

        # get the opener
        open = self._include_schemes[scheme]

        # get the format
        format = suffix_match.group("format")
        if format is None:
            format = "yaml"
        elif format not in self._include_formats:
            raise ConstructorError(
                problem='unsupported include format "%s"' % format,
                problem_mark=node.start_mark,
            )

        # get the loader
        load = self._include_formats[format]

        # get the argument
        value = constructor.construct_scalar(node)

        # expand environment variables
        value = os.path.expandvars(value)

        try:
            # open the document
            with open(self, value, must_exist) as f:
                # if None, then it doesn't exist
                if f is None:
                    return None

                # load the document
                return load(self, f)
        # catch errors
        except Exception as e:
            raise_from(
                ConstructorError(
                    context='while including %s %s "%s"' %
                    (format, scheme, value),
                    context_mark=node.start_mark,
                ),
                e,
            )

    def include(self):
        def _include(constructor, prefix, node):
            return self._include(constructor, prefix, node, True)
        return _include

    def include_if_exists(self):
        def _include_if_exists(constructor, prefix, node):
            return self._include(constructor, prefix, node, False)
        return _include_if_exists

    def register_defaults(self, constructor):
        self.register_include_format(
            "yaml", thirdparty.yaml.include.format.yaml._load_yaml
        )

        self.register_include_format(
            "verbatim", thirdparty.yaml.include.format.verbatim._load_verbatim
        )

        self.register_include_scheme(
            "file", thirdparty.yaml.include.scheme.file._open_file
        )

        self.register_include_scheme(
            "url", thirdparty.yaml.include.scheme.url._open_url
        )

        constructor.add_multi_constructor("!include", self.include())

        constructor.add_multi_constructor(
            "-!include", self.include_if_exists()
        )


# def register_include(cls):

#     cls.overlay_add_include_scheme = (
#         overlay_add_include_scheme
#     )
#     cls.overlay_add_include_format = (
#         overlay_add_include_format
#     )


def register_defaults(cls):
    cls.overlay_add_include_format(
        "yaml", thirdparty.yaml.include.format.yaml._load_yaml
    )

    cls.overlay_add_include_format(
        "verbatim", thirdparty.yaml.include.format.verbatim._load_verbatim
    )

    cls.overlay_add_include_scheme(
        "file", thirdparty.yaml.include.scheme.file._open_file
    )

    cls.overlay_add_include_scheme(
        "url", thirdparty.yaml.include.scheme.url._open_url
    )

    cls.include = thirdparty.yaml.include.include
    cls.include_if_exists = thirdparty.yaml.include.include_if_exists

    thirdparty.yaml.operation.register_defaults(cls)
