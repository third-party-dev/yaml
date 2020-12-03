from future.utils import listitems

import ruamel.yaml
from ruamel.yaml.nodes import SequenceNode
from collections import OrderedDict

from thirdparty.yaml.include import IncludeHandler
from thirdparty.yaml.operation import OperationsHandler


class Representer(ruamel.yaml.representer.Representer):
    def represent_sequence_of_pairs(self, tag, sequence):
        value = []
        for item_key, item_value in sequence:
            item_node = self.represent_mapping(
                "tag:yaml.org,2002:map",
                [(item_key, item_value)],
            )
            value.append(item_node)
        return SequenceNode(tag, value, flow_style=False)

    def represent_omap(self, data):
        return self.represent_sequence_of_pairs(
            "tag:yaml.org,2002:omap",
            listitems(data),
        )

    def represent_list(self, data):
        # pairs = type(data) is _oldtypes[list] and len(data) > 0
        pairs = type(data) is list and len(data) > 0
        if pairs:
            for item in data:
                if not (type(item) is tuple and len(item) == 2):
                    pairs = False
                    break
        if pairs:
            return self.represent_sequence_of_pairs(
                "tag:yaml.org,2002:pairs",
                data,
            )
        else:
            return super().represent_list(data)


class YamlOverlay(object):
    def __init__(self):
        self._default_yaml = self.create()
        self.constructor = self._default_yaml.constructor
        self.ops_handler = OperationsHandler(self.constructor)
        self.inc_handler = IncludeHandler(self.constructor)

        self.ops_handler.register_defaults(self.constructor,
                                           self._default_yaml.resolver)

        self.inc_handler.register_defaults(self.constructor)

        # yaml.representer.add_representer(
        #     _oldtypes[list],
        #     representer_cls.represent_list,
        # )

        self._default_yaml.representer.add_representer(
            OrderedDict,
            Representer.represent_omap,
        )

    def create(self):
        yaml = ruamel.yaml.YAML()
        yaml.version = (1, 2)
        yaml.indent(mapping=3, sequence=2, offset=0)
        yaml.allow_duplicate_keys = False

        return yaml

    def load(self, stream):
        return self._default_yaml.load(stream)

    def dump(self, data, stream=None, **kwds):
        return self._default_yaml.dump(data, stream=stream, **kwds)
