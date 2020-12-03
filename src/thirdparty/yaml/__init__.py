from collections import OrderedDict
import re

import thirdparty.yaml.include
import thirdparty.yaml.operation


def register_default_compositions(cls):

    thirdparty.yaml.include.register_include(cls)

    thirdparty.yaml.include.register_defaults(cls)

    thirdparty.yaml.operation.register_defaults(cls)


def register_default_constructors(yaml, constructor_cls):
    yaml.constructor.add_constructor(
        "tag:yaml.org,2002:map", constructor_cls.construct_yaml_map
    )

    yaml.constructor.add_constructor(
        "tag:yaml.org,2002:omap", constructor_cls.construct_yaml_omap
    )

    yaml.constructor.add_constructor(
        "tag:yaml.org,2002:set", constructor_cls.construct_yaml_set
    )

    yaml.constructor.add_constructor(
        "tag:yaml.org,2002:pairs", constructor_cls.construct_yaml_pairs
    )

    yaml.constructor.add_constructor(
        "tag:yaml.org,2002:seq", constructor_cls.construct_yaml_sequence
    )

    yaml.constructor.add_multi_constructor("!include", constructor_cls.include)

    yaml.constructor.add_multi_constructor(
        "-!include", constructor_cls.include_if_exists
    )


def register_default_representers(yaml, representer_cls):

    # yaml.representer.add_representer(
    #     _oldtypes[list],
    #     representer_cls.represent_list,
    # )

    yaml.representer.add_representer(
        OrderedDict,
        representer_cls.represent_omap,
    )


def register_default_resolvers(yaml):

    yaml.resolver.add_implicit_resolver(
        "!merge",
        re.compile("^" + re.escape("<<<<") + "$"),
        ["<"],
    )

    yaml.resolver.add_implicit_resolver(
        "!recursive_merge",
        re.compile("^" + re.escape("<<<") + "$"),
        ["<"],
    )

    return yaml
